import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';
import '../widgets/modern_charts.dart';

class HarvestScreen extends StatefulWidget {
  const HarvestScreen({super.key});
  @override
  State<HarvestScreen> createState() => _HarvestScreenState();
}

class _HarvestScreenState extends State<HarvestScreen> {
  final _api = ApiService();
  List<dynamic> _harvests = [];
  Map<String, dynamic> _stats = {};
  Map<String, dynamic> _visual = {};

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    try {
      final h = await _api.get('/farm/harvests/');
      final s = await _api.get('/farm/harvests/stats/');
      final v = await _api.get('/analytics/visual/');
      setState(() {
        _harvests = parseApiList(h);
        _stats = parseApiMap(s);
        _visual = parseApiMap(v);
      });
    } catch (_) {}
  }

  Future<void> _add() async {
    final qty = TextEditingController();
    final crop = TextEditingController(text: 'maize');
    final ok = await showDialog<bool>(context: context, builder: (ctx) => AlertDialog(
      title: const Text('Nouvelle récolte'),
      content: Column(mainAxisSize: MainAxisSize.min, children: [
        TextField(controller: crop, decoration: const InputDecoration(labelText: 'Culture')),
        TextField(controller: qty, decoration: const InputDecoration(labelText: 'Quantité (kg)'), keyboardType: TextInputType.number),
      ]),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Annuler')),
        TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Enregistrer')),
      ],
    ));
    if (ok != true) return;
    await _api.post('/farm/harvests/', {
      'crop_type': crop.text, 'quantity_kg': double.tryParse(qty.text) ?? 0,
      'harvest_date': DateTime.now().toIso8601String().substring(0, 10),
    });
    _load();
  }

  @override
  Widget build(BuildContext context) {
    final series = (_visual['series'] as Map<String, dynamic>?) ?? {};
    final byCrop = (_stats['by_crop'] as Map<String, dynamic>?) ?? {};
    final cropDist = byCrop.entries.map((e) => {'name': e.key, 'value': e.value}).toList();

    return Scaffold(
      appBar: AppBar(title: const Text('Carnet de récolte'), backgroundColor: AppTheme.primaryGreen),
      floatingActionButton: FloatingActionButton(onPressed: _add, child: const Icon(Icons.add)),
      body: RefreshIndicator(
        onRefresh: _load,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Row(children: [
              Expanded(child: ModernCharts.kpiCard(
                label: 'Total récolté', value: '${_stats['total_kg'] ?? 0}',
                unit: 'kg', color: AppTheme.accentOrange, icon: Icons.grass,
              )),
              const SizedBox(width: 12),
              Expanded(child: ModernCharts.kpiCard(
                label: 'Entrées', value: '${_harvests.length}',
                unit: 'records', color: AppTheme.primaryGreen, icon: Icons.list_alt,
              )),
            ]),
            const SizedBox(height: 8),
            if (cropDist.isNotEmpty)
              ModernCharts.donutChart(title: 'Récoltes par culture', data: cropDist),
            ModernCharts.barChart(
              title: 'Récoltes mensuelles',
              data: (series['harvest_monthly'] as List?)?.cast<Map<String, dynamic>>() ?? [],
              color: AppTheme.accentOrange,
            ),
            const Text('Historique', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
            ..._harvests.map((h) {
              final item = h as Map<String, dynamic>;
              return ListTile(
                leading: const Icon(Icons.agriculture),
                title: Text('${item['quantity_kg']} kg — ${item['crop_type']}'),
                subtitle: Text('${item['parcel_name'] ?? ''} · ${item['harvest_date']}'),
              );
            }),
          ],
        ),
      ),
    );
  }
}
