import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import '../config/app_config.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class MeasureMapScreen extends StatefulWidget {
  const MeasureMapScreen({super.key});

  @override
  State<MeasureMapScreen> createState() => _MeasureMapScreenState();
}

class _MeasureMapScreenState extends State<MeasureMapScreen> {
  final _api = ApiService();
  final _mapController = MapController();
  final List<LatLng> _points = [];
  String? _result;

  Future<void> _measure(String type) async {
    if (_points.length < (type == 'area' ? 3 : 2)) return;
    final coords = _points.map((p) => [p.longitude, p.latitude]).toList();
    final r = await _api.post('/parcels/measure/', {'type': type, 'coordinates': coords});
    setState(() {
      if (type == 'distance') {
        _result = 'Distance: ${r['km']} km (${r['m']} m)';
      } else {
        _result = 'Surface: ${r['hectares']} ha (${r['m2']} m²)';
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mesure carte'),
        backgroundColor: AppTheme.primaryGreen,
        actions: [
          IconButton(icon: const Icon(Icons.undo), onPressed: () => setState(() { _points.clear(); _result = null; })),
        ],
      ),
      body: Stack(children: [
        FlutterMap(
          mapController: _mapController,
          options: MapOptions(
            initialCenter: LatLng(AppConfig.defaultLat, AppConfig.defaultLng),
            initialZoom: AppConfig.defaultZoom,
            onTap: (_, point) => setState(() => _points.add(point)),
          ),
          children: [
            TileLayer(urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'africa.arca.arca_gis_app'),
            if (_points.isNotEmpty)
              MarkerLayer(markers: _points.map((p) => Marker(
                point: p, width: 20, height: 20,
                child: const Icon(Icons.place, color: AppTheme.primaryGreen, size: 20),
              )).toList()),
            if (_points.length >= 2)
              PolylineLayer(polylines: [Polyline(points: _points, color: AppTheme.primaryGreen, strokeWidth: 3)]),
          ],
        ),
        Positioned(
          bottom: 16, left: 16, right: 16,
          child: Card(
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                Text('${_points.length} point(s) — touchez la carte'),
                if (_result != null) Text(_result!, style: const TextStyle(fontWeight: FontWeight.bold)),
                Row(mainAxisAlignment: MainAxisAlignment.spaceEvenly, children: [
                  ElevatedButton(onPressed: () => _measure('distance'), child: const Text('Distance')),
                  ElevatedButton(onPressed: () => _measure('area'), child: const Text('Surface')),
                ]),
              ]),
            ),
          ),
        ),
      ]),
    );
  }
}
