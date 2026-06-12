import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class PictogramScreen extends StatefulWidget {
  const PictogramScreen({super.key});

  @override
  State<PictogramScreen> createState() => _PictogramScreenState();
}

class _PictogramScreenState extends State<PictogramScreen> {
  final _api = ApiService();
  List<dynamic> _items = [];

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final data = await _api.get('/inclusion/pictogram-menu/');
      setState(() => _items = (data['items'] as List?) ?? []);
    } catch (_) {}
  }

  IconData _icon(String id) {
    switch (id) {
      case 'sos': return Icons.warning;
      case 'weather': return Icons.cloud;
      case 'parcels': return Icons.grass;
      case 'market': return Icons.store;
      case 'water': return Icons.water_drop;
      default: return Icons.phone;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(title: const Text('Menu simple'), backgroundColor: AppTheme.primaryGreen),
      body: GridView.builder(
        padding: const EdgeInsets.all(16),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 2, mainAxisSpacing: 16, crossAxisSpacing: 16),
        itemCount: _items.length,
        itemBuilder: (_, i) {
          final item = _items[i] as Map<String, dynamic>;
          return Material(
            color: AppTheme.primaryGreen.withValues(alpha: 0.1),
            borderRadius: BorderRadius.circular(16),
            child: InkWell(
              onTap: () => ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text(item['audio']?.toString() ?? '')),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(_icon(item['id']?.toString() ?? ''), size: 64, color: AppTheme.primaryGreen),
                  const SizedBox(height: 12),
                  Text(item['label']?.toString() ?? '', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
