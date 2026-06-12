import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class HarvestScreen extends StatefulWidget {
  const HarvestScreen({super.key});
  @override
  State<HarvestScreen> createState() => _HarvestScreenState();
}

class _HarvestScreenState extends State<HarvestScreen> {
  final _api = ApiService();
  List<dynamic> _harvests = [];
  Map<String, dynamic> _stats = {};

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    try {
      final h = await _api.get('/farm/harvests/');
      final s = await _api.get('/farm/harvests/stats/');
      setState(() {
        _harvests = h is List ? h : (h['results'] as List?) ?? [];
        _stats = s is Map<String, dynamic> ? s : {};
      });
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Carnet de récolte'), backgroundColor: AppTheme.primaryGreen),
      body: Column(children: [
        if (_stats.isNotEmpty) Card(margin: const EdgeInsets.all(12), child: Padding(
          padding: const EdgeInsets.all(16),
          child: Text('Total: ${_stats['total_kg'] ?? 0} kg', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        )),
        Expanded(child: ListView.builder(
          itemCount: _harvests.length,
          itemBuilder: (_, i) {
            final h = _harvests[i] as Map<String, dynamic>;
            return ListTile(
              leading: const Icon(Icons.agriculture),
              title: Text('${h['quantity_kg']} kg — ${h['crop_type']}'),
              subtitle: Text('${h['parcel_name'] ?? ''} · ${h['harvest_date']}'),
            );
          },
        )),
      ]),
    );
  }
}
