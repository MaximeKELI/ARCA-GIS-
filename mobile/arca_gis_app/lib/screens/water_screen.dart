import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class WaterScreen extends StatefulWidget {
  const WaterScreen({super.key});

  @override
  State<WaterScreen> createState() => _WaterScreenState();
}

class _WaterScreenState extends State<WaterScreen> {
  final _api = ApiService();
  List<dynamic> _points = [];
  Map<String, dynamic>? _conflicts;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final points = await _api.get('/water/points/');
      final conflicts = await _api.get('/water/conflicts/');
      setState(() {
        _points = points is List ? points : (points['results'] as List?) ?? [];
        _conflicts = conflicts is Map<String, dynamic> ? conflicts : null;
      });
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Gestion de l\'eau'), backgroundColor: AppTheme.primaryGreen),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (_conflicts != null)
            Card(
              color: _conflicts!['conflict_risk'] == true ? Colors.orange.shade50 : Colors.green.shade50,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Text(_conflicts!['recommendation']?.toString() ?? ''),
              ),
            ),
          ..._points.map((p) {
            final pt = p as Map<String, dynamic>;
            return ListTile(
              leading: const Icon(Icons.water_drop, color: AppTheme.climateBlue),
              title: Text(pt['name']?.toString() ?? ''),
              subtitle: Text('${pt['point_type']} · ${pt['current_level_pct']}%'),
            );
          }),
        ],
      ),
    );
  }
}
