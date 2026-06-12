import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

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
      setState(() => _items = data is List ? data : []);
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Stock intrants'), backgroundColor: AppTheme.primaryGreen),
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
