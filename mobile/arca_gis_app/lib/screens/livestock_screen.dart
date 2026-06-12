import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class LivestockScreen extends StatefulWidget {
  const LivestockScreen({super.key});

  @override
  State<LivestockScreen> createState() => _LivestockScreenState();
}

class _LivestockScreenState extends State<LivestockScreen> {
  final _api = ApiService();
  List<dynamic> _herds = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final data = await _api.get('/livestock/herds/');
      setState(() { _herds = data is List ? data : (data['results'] as List?) ?? []; _loading = false; });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Élevage'), backgroundColor: AppTheme.primaryGreen),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: _herds.length,
              itemBuilder: (_, i) {
                final h = _herds[i] as Map<String, dynamic>;
                return ListTile(
                  leading: const Icon(Icons.pets),
                  title: Text(h['name']?.toString() ?? ''),
                  subtitle: Text('${h['animal_type']} · ${h['count']} têtes'),
                  trailing: Chip(label: Text(h['health_status']?.toString() ?? '')),
                );
              },
            ),
    );
  }
}
