import 'dart:math';
import 'package:flutter/foundation.dart';
import 'package:latlong2/latlong.dart';
import '../models/alert.dart';
import '../models/climate_event.dart';
import '../models/incident.dart';
import '../models/parcel.dart';
import '../services/api_service.dart';
import '../services/geofence_service.dart';
import '../services/gps_tracking_service.dart';
import '../services/location_service.dart';
import '../services/offline_service.dart';
import '../services/offline_tile_service.dart';
import '../services/websocket_service.dart';

class MapProvider extends ChangeNotifier {
  final ApiService _api = ApiService();
  final LocationService _location = LocationService();
  final WebSocketService _ws = WebSocketService();
  final OfflineService _offline = OfflineService();
  final GeofenceService _geofence = GeofenceService();
  final GPSTrackingService _gps = GPSTrackingService();
  final OfflineTileService _tiles = OfflineTileService();
  bool _offlineTilesReady = false;
  List<Map<String, dynamic>> _choroplethCells = [];
  bool _showChoropleth = false;
  String _choroplethMetric = 'moisture';

  List<Map<String, dynamic>> get choroplethCells => _choroplethCells;
  bool get showChoropleth => _showChoropleth;

  void setChoropleth(List<dynamic> cells, String metric) {
    _choroplethCells = cells.cast<Map<String, dynamic>>();
    _choroplethMetric = metric;
    _showChoropleth = true;
    notifyListeners();
  }

  void toggleChoropleth() {
    _showChoropleth = !_showChoropleth;
    notifyListeners();
  }

  List<Parcel> _parcels = [];
  List<ClimateEvent> _climateEvents = [];
  List<Incident> _incidents = [];
  List<AlertModel> _alerts = [];
  List<RescuePosition> _rescuePositions = [];
  LatLng? _userPosition;
  bool _isLoading = false;
  bool _isOffline = false;
  String? _error;
  Map<String, dynamic>? _aiAnalysis;

  List<Parcel> get parcels => _parcels;
  List<ClimateEvent> get climateEvents => _climateEvents;
  List<Incident> get incidents => _incidents;
  List<AlertModel> get alerts => _alerts;
  List<RescuePosition> get rescuePositions => _rescuePositions;
  LatLng? get userPosition => _userPosition;
  bool get isLoading => _isLoading;
  bool get isOffline => _isOffline;
  String? get error => _error;
  Map<String, dynamic>? get aiAnalysis => _aiAnalysis;
  bool get offlineTilesReady => _offlineTilesReady;
  List<Map<String, dynamic>> get heatmapCells => _heatmapCells;
  bool get showHeatmap => _showHeatmap;

  void toggleHeatmap() {
    _showHeatmap = !_showHeatmap;
    notifyListeners();
  }

  Future<void> loadHeatmap() async {
    try {
      final data = await _api.get('/analytics/heatmap/');
      _heatmapCells = (data['cells'] as List?)?.cast<Map<String, dynamic>>() ?? [];
      notifyListeners();
    } catch (_) {}
  }

  Future<void> downloadOfflineTiles({int zoom = 13}) async {
    final pos = _userPosition;
    if (pos == null) return;
    await _tiles.init();
    final x = _lon2tile(pos.longitude, zoom);
    final y = _lat2tile(pos.latitude, zoom);
    await _tiles.downloadRegion(zoom: zoom, xMin: x - 1, xMax: x + 1, yMin: y - 1, yMax: y + 1);
    _offlineTilesReady = true;
    notifyListeners();
  }

  int _lon2tile(double lon, int z) => ((lon + 180) / 360 * pow(2, z)).floor();
  int _lat2tile(double lat, int z) {
    final r = lat * pi / 180;
    return ((1 - log(tan(r) + 1 / cos(r)) / pi) / 2 * pow(2, z)).floor();
  }

  String? get offlineTileCacheDir => _tiles.cacheDirPath;

  Future<void> initialize() async {
    _ws.alertStream.listen((alert) {
      _alerts.insert(0, alert);
      notifyListeners();
    });
    await _ws.connect();
    await _gps.connect();
    _gps.positionsStream.listen((positions) {
      _rescuePositions = positions;
      notifyListeners();
    });
    await loadAllData();
    _startGeofenceMonitoring();
  }

  void _startGeofenceMonitoring() {
    Future.doWhile(() async {
      await Future.delayed(const Duration(minutes: 2));
      if (_userPosition != null && !await _offline.isOnline) return true;
      if (_userPosition != null) {
        try {
          await _geofence.checkPosition(_userPosition!.latitude, _userPosition!.longitude);
        } catch (_) {}
      }
      return true;
    });
  }

  Future<void> loadAllData() async {
    _isLoading = true;
    _error = null;
    _isOffline = !(await _offline.isOnline);
    notifyListeners();

    try {
      final position = await _location.getCurrentPosition();
      if (position != null) {
        _userPosition = LatLng(position.latitude, position.longitude);
      }

      if (_isOffline) {
        await _loadFromCache();
      } else {
        await Future.wait([
          _loadParcels(),
          _loadClimateEvents(),
          _loadIncidents(),
          _loadAlerts(),
          loadHeatmap(),
        ]);
        await _syncPendingSOS();
      }
    } catch (e) {
      _error = e.toString();
      await _loadFromCache();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> _loadFromCache() async {
    final parcels = await _offline.getCachedParcels();
    final alerts = await _offline.getCachedAlerts();
    final climate = await _offline.getCachedClimate();
    _parcels = parcels.map((j) => Parcel.fromJson(j)).toList();
    _alerts = alerts.map((j) => AlertModel.fromJson(j)).toList();
    _climateEvents = climate.map((j) => ClimateEvent.fromJson(j)).toList();
    _isOffline = true;
  }

  Future<void> _loadParcels() async {
    final data = await _api.get('/parcels/');
    final results = data['results'] ?? data;
    if (results is List) {
      _parcels = results.map((j) => Parcel.fromJson(j)).toList();
      await _offline.cacheParcels(results);
    }
  }

  Future<void> _loadClimateEvents() async {
    final lat = _userPosition?.latitude;
    final lng = _userPosition?.longitude;
    final endpoint = lat != null
        ? '/climate/events/nearby/?lat=$lat&lng=$lng&radius=200'
        : '/climate/events/';
    final data = await _api.get(endpoint);
    final results = data['results'] ?? data;
    if (results is List) {
      _climateEvents = results.map((j) => ClimateEvent.fromJson(j)).toList();
      await _offline.cacheClimate(results);
    }
  }

  Future<void> _loadIncidents() async {
    final data = await _api.get('/incidents/sos/active/');
    final results = data['results'] ?? data;
    if (results is List) {
      _incidents = results.map((j) => Incident.fromJson(j)).toList();
    }
  }

  Future<void> _loadAlerts() async {
    final data = await _api.get('/alerts/');
    final results = data['results'] ?? data;
    if (results is List) {
      _alerts = results.map((j) => AlertModel.fromJson(j)).toList();
      await _offline.cacheAlerts(results);
    }
  }

  Future<void> _syncPendingSOS() async {
    final pending = await _offline.getPendingSOS();
    for (final sos in pending) {
      try {
        await _api.post('/incidents/sos/', sos);
      } catch (_) {}
    }
    if (pending.isNotEmpty) await _offline.clearPendingSOS();
  }

  Future<bool> triggerSOS({String description = 'SOS - Urgence signalée'}) async {
    if (_userPosition == null) {
      final pos = await _location.getCurrentPosition();
      if (pos == null) {
        _error = 'Position GPS indisponible';
        notifyListeners();
        return false;
      }
      _userPosition = LatLng(pos.latitude, pos.longitude);
    }

    final payload = {
      'lat': _userPosition!.latitude,
      'lng': _userPosition!.longitude,
      'description': description,
      'people_affected': 1,
    };

    if (!(await _offline.isOnline)) {
      await _offline.queueSOS(payload);
      _isOffline = true;
      notifyListeners();
      return true;
    }

    try {
      await _api.post('/incidents/sos/', payload);
      await _loadIncidents();
      return true;
    } catch (e) {
      await _offline.queueSOS(payload);
      _error = e.toString();
      notifyListeners();
      return false;
    }
  }

  void updateRescuePosition(double lat, double lng) {
    _gps.sendPosition(lat, lng);
  }

  Future<void> requestAIAnalysis({String cropType = 'maize'}) async {
    if (_userPosition == null) return;
    try {
      _aiAnalysis = await _api.post('/climate/analyze/', {
        'lat': _userPosition!.latitude,
        'lng': _userPosition!.longitude,
        'crop_type': cropType,
      });
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    }
  }

  @override
  void dispose() {
    _ws.dispose();
    _gps.dispose();
    super.dispose();
  }
}
