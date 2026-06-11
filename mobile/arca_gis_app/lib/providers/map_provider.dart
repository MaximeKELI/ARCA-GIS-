import 'package:flutter/foundation.dart';
import 'package:latlong2/latlong.dart';
import '../models/alert.dart';
import '../models/climate_event.dart';
import '../models/incident.dart';
import '../models/parcel.dart';
import '../services/api_service.dart';
import '../services/location_service.dart';
import '../services/websocket_service.dart';

class MapProvider extends ChangeNotifier {
  final ApiService _api = ApiService();
  final LocationService _location = LocationService();
  final WebSocketService _ws = WebSocketService();

  List<Parcel> _parcels = [];
  List<ClimateEvent> _climateEvents = [];
  List<Incident> _incidents = [];
  List<AlertModel> _alerts = [];
  LatLng? _userPosition;
  bool _isLoading = false;
  String? _error;
  Map<String, dynamic>? _aiAnalysis;

  List<Parcel> get parcels => _parcels;
  List<ClimateEvent> get climateEvents => _climateEvents;
  List<Incident> get incidents => _incidents;
  List<AlertModel> get alerts => _alerts;
  LatLng? get userPosition => _userPosition;
  bool get isLoading => _isLoading;
  String? get error => _error;
  Map<String, dynamic>? get aiAnalysis => _aiAnalysis;

  Future<void> initialize() async {
    _ws.alertStream.listen((alert) {
      _alerts.insert(0, alert);
      notifyListeners();
    });
    await _ws.connect();
    await loadAllData();
  }

  Future<void> loadAllData() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final position = await _location.getCurrentPosition();
      if (position != null) {
        _userPosition = LatLng(position.latitude, position.longitude);
      }

      await Future.wait([
        _loadParcels(),
        _loadClimateEvents(),
        _loadIncidents(),
        _loadAlerts(),
      ]);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> _loadParcels() async {
    final data = await _api.get('/parcels/');
    final results = data['results'] ?? data;
    if (results is List) {
      _parcels = results.map((j) => Parcel.fromJson(j)).toList();
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
    }
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

    try {
      await _api.post('/incidents/sos/', {
        'lat': _userPosition!.latitude,
        'lng': _userPosition!.longitude,
        'description': description,
        'people_affected': 1,
      });
      await _loadIncidents();
      return true;
    } catch (e) {
      _error = e.toString();
      notifyListeners();
      return false;
    }
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
    super.dispose();
  }
}
