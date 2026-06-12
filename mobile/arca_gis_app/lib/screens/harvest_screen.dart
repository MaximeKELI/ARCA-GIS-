import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

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
        _harvests = parseApiList(h);
        _stats = parseApiMap(s);
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
    return Scaffold(
      appBar: AppBar(title: const Text('Carnet de récolte'), backgroundColor: AppTheme.primaryGreen),
      floatingActionButton: FloatingActionButton(onPressed: _add, child: const Icon(Icons.add)),
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
