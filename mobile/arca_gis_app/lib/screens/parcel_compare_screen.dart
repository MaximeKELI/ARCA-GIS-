import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

class ParcelCompareScreen extends StatefulWidget {
  final List<int> parcelIds;
  const ParcelCompareScreen({super.key, required this.parcelIds});

  @override
  State<ParcelCompareScreen> createState() => _ParcelCompareScreenState();
}

class _ParcelCompareScreenState extends State<ParcelCompareScreen> {
  final _api = ApiService();
  List<dynamic> _parcels = [];

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    if (widget.parcelIds.isEmpty) return;
    try {
      final ids = widget.parcelIds.join(',');
      final data = await _api.get('/farm/parcels/compare/?ids=$ids');
      setState(() => _parcels = parseApiList(data));
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Comparer parcelles'), backgroundColor: AppTheme.primaryGreen),
      body: _parcels.isEmpty
          ? const Center(child: Text('Sélectionnez au moins 2 parcelles'))
          : ListView(
              children: _parcels.map((p) {
                final m = p as Map<String, dynamic>;
                return Card(
                  margin: const EdgeInsets.all(12),
                  child: ListTile(
                    title: Text(m['name']?.toString() ?? ''),
                    subtitle: Text('${m['crop']} · ${m['health']} · ${m['moisture']}% humidité'),
                    trailing: Text('${m['area_ha']} ha'),
                  ),
                );
              }).toList(),
            ),
    );
  }
}
