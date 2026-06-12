import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';
import '../widgets/modern_charts.dart';

class CarbonScreen extends StatefulWidget {
  const CarbonScreen({super.key});

  @override
  State<CarbonScreen> createState() => _CarbonScreenState();
}

class _CarbonScreenState extends State<CarbonScreen> {
  final _api = ApiService();
  List<dynamic> _credits = [];
  Map<String, dynamic>? _estimate;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final data = await _api.get('/carbon/credits/');
      setState(() {
        _credits = parseApiList(data);
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  Future<void> _runEstimate() async {
    final area = TextEditingController(text: '2.5');
    final crop = TextEditingController(text: 'maize');
    final ok = await showDialog<bool>(context: context, builder: (ctx) => AlertDialog(
      title: const Text('Estimer crédits carbone'),
      content: Column(mainAxisSize: MainAxisSize.min, children: [
        TextField(controller: area, decoration: const InputDecoration(labelText: 'Surface (ha)'), keyboardType: TextInputType.number),
        TextField(controller: crop, decoration: const InputDecoration(labelText: 'Culture')),
      ]),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Annuler')),
        TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Estimer')),
      ],
    ));
    if (ok != true) return;
    final r = await _api.post('/carbon/estimate/', {
      'area_hectares': double.tryParse(area.text) ?? 2.5,
      'crop_type': crop.text,
    });
    setState(() => _estimate = parseApiMap(r));
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final totalCo2 = _credits.fold<double>(0, (s, c) => s + ((c['co2_tons_sequestered'] as num?)?.toDouble() ?? 0));
    final totalUsd = _credits.fold<double>(0, (s, c) => s + ((c['credit_value_usd'] as num?)?.toDouble() ?? 0));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Crédits carbone'),
        backgroundColor: const Color(0xFF2E7D32),
        actions: [IconButton(icon: const Icon(Icons.calculate), onPressed: _runEstimate)],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _load,
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  Row(children: [
                    Expanded(child: ModernCharts.kpiCard(
                      label: 'CO₂ séquestré', value: totalCo2.toStringAsFixed(1),
                      unit: 't', color: const Color(0xFF2E7D32), icon: Icons.eco, isDark: isDark,
                    )),
                    const SizedBox(width: 12),
                    Expanded(child: ModernCharts.kpiCard(
                      label: 'Valeur crédits', value: totalUsd.toStringAsFixed(0),
                      unit: 'USD', color: const Color(0xFF00838F), icon: Icons.attach_money, isDark: isDark,
                    )),
                  ]),
                  if (_estimate != null) Card(
                    margin: const EdgeInsets.symmetric(vertical: 12),
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        const Text('Estimation', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                        Text('CO₂/an: ${_estimate!['co2_tons_year']} tonnes'),
                        Text('Valeur: ${_estimate!['credit_value_usd']} USD'),
                        Text('Méthode: ${_estimate!['methodology'] ?? 'ARCA-GIS'}'),
                      ]),
                    ),
                  ),
                  const Text('Mes crédits', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                  const SizedBox(height: 8),
                  ..._credits.map((c) {
                    final m = c as Map<String, dynamic>;
                    return Card(
                      child: ListTile(
                        leading: Icon(Icons.eco, color: m['verified'] == true ? Colors.green : Colors.grey),
                        title: Text(m['parcel_name']?.toString() ?? 'Parcelle'),
                        subtitle: Text('${m['co2_tons_sequestered']} t CO₂ · ${m['period_start']} → ${m['period_end']}'),
                        trailing: Text('\$${m['credit_value_usd']}', style: const TextStyle(fontWeight: FontWeight.bold)),
                      ),
                    );
                  }),
                ],
              ),
            ),
    );
  }
}
