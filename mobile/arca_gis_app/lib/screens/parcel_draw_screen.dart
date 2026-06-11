import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import '../config/app_config.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class ParcelDrawScreen extends StatefulWidget {
  const ParcelDrawScreen({super.key});

  @override
  State<ParcelDrawScreen> createState() => _ParcelDrawScreenState();
}

class _ParcelDrawScreenState extends State<ParcelDrawScreen> {
  final MapController _mapController = MapController();
  final List<LatLng> _points = [];
  final _nameController = TextEditingController();
  String _cropType = 'maize';
  bool _saving = false;

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    if (_points.length < 3) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Ajoutez au moins 3 points')),
      );
      return;
    }
    if (_nameController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Nom de parcelle requis')),
      );
      return;
    }

    setState(() => _saving = true);
    final coords = [..._points.map((p) => [p.longitude, p.latitude]), [_points.first.longitude, _points.first.latitude]];

    try {
      final api = ApiService();
      await api.post('/parcels/', {
        'name': _nameController.text,
        'crop_type': _cropType,
        'geometry': {'type': 'Polygon', 'coordinates': [coords]},
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Parcelle créée !'), backgroundColor: AppTheme.primaryGreen),
        );
        Navigator.pop(context, true);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Erreur: $e')));
      }
    } finally {
      setState(() => _saving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dessiner une parcelle'),
        actions: [
          if (_points.isNotEmpty)
            IconButton(icon: const Icon(Icons.undo), onPressed: () => setState(() => _points.removeLast())),
          IconButton(icon: const Icon(Icons.save), onPressed: _saving ? null : _save),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                Expanded(child: TextField(
                  controller: _nameController,
                  decoration: const InputDecoration(labelText: 'Nom', isDense: true),
                )),
                const SizedBox(width: 8),
                DropdownButton<String>(
                  value: _cropType,
                  items: const [
                    DropdownMenuItem(value: 'maize', child: Text('Maïs')),
                    DropdownMenuItem(value: 'rice', child: Text('Riz')),
                    DropdownMenuItem(value: 'cassava', child: Text('Manioc')),
                    DropdownMenuItem(value: 'cocoa', child: Text('Cacao')),
                  ],
                  onChanged: (v) => setState(() => _cropType = v!),
                ),
              ],
            ),
          ),
          Expanded(
            child: FlutterMap(
              mapController: _mapController,
              options: MapOptions(
                initialCenter: LatLng(AppConfig.defaultLat, AppConfig.defaultLng),
                initialZoom: 14,
                onTap: (_, point) => setState(() => _points.add(point)),
              ),
              children: [
                TileLayer(
                  urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                  userAgentPackageName: 'africa.arca.arca_gis_app',
                ),
                if (_points.length >= 2)
                  PolygonLayer(polygons: [
                    Polygon(
                      points: _points,
                      color: AppTheme.primaryGreen.withValues(alpha: 0.3),
                      borderColor: AppTheme.primaryGreen,
                      borderStrokeWidth: 2,
                    ),
                  ]),
                MarkerLayer(
                  markers: _points.map((p) => Marker(
                    point: p,
                    width: 20,
                    height: 20,
                    child: const Icon(Icons.circle, color: AppTheme.primaryGreen, size: 14),
                  )).toList(),
                ),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.all(12),
            color: Colors.white,
            child: Text('${_points.length} points — Touchez la carte pour ajouter des sommets',
                textAlign: TextAlign.center),
          ),
        ],
      ),
    );
  }
}
