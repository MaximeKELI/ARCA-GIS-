import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

class InventoryScreen extends StatefulWidget {
  const InventoryScreen({super.key});
  @override
  State<InventoryScreen> createState() => _InventoryScreenState();
}

class _InventoryScreenState extends State<InventoryScreen> {
  final _api = ApiService();
  List<dynamic> _items = [];

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    try {
      final data = await _api.get('/farm/inventory/');
      setState(() => _items = parseApiList(data));
    } catch (_) {}
  }

  Future<void> _add() async {
    final name = TextEditingController();
    final qty = TextEditingController();
    final ok = await showDialog<bool>(context: context, builder: (ctx) => AlertDialog(
      title: const Text('Ajouter intrant'),
      content: Column(mainAxisSize: MainAxisSize.min, children: [
        TextField(controller: name, decoration: const InputDecoration(labelText: 'Produit')),
        TextField(controller: qty, decoration: const InputDecoration(labelText: 'Quantité'), keyboardType: TextInputType.number),
      ]),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Annuler')),
        TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Ajouter')),
      ],
    ));
    if (ok != true) return;
    await _api.post('/farm/inventory/', {
      'product_name': name.text, 'product_type': 'fertilizer',
      'quantity': double.tryParse(qty.text) ?? 0, 'unit': 'kg',
    });
    _load();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Stock intrants'), backgroundColor: AppTheme.primaryGreen),
      floatingActionButton: FloatingActionButton(onPressed: _add, child: const Icon(Icons.add)),
      body: ListView.builder(
        itemCount: _items.length,
        itemBuilder: (_, i) {
          final item = _items[i] as Map<String, dynamic>;
          final low = item['is_low'] == true;
          return ListTile(
            leading: Icon(Icons.inventory, color: low ? Colors.red : AppTheme.primaryGreen),
            title: Text(item['product_name']?.toString() ?? ''),
            subtitle: Text('${item['quantity']} ${item['unit']}'),
            trailing: low ? const Chip(label: Text('Bas', style: TextStyle(color: Colors.red))) : null,
          );
        },
      ),
    );
  }
}
