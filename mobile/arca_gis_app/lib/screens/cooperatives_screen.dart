import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class CooperativesScreen extends StatefulWidget {
  const CooperativesScreen({super.key});
  @override
  State<CooperativesScreen> createState() => _CooperativesScreenState();
}

class _CooperativesScreenState extends State<CooperativesScreen> {
  final ApiService _api = ApiService();
  List<dynamic> _coops = [];
  bool _loading = true;

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    final data = await _api.get('/cooperatives/');
    setState(() {
      _coops = data['results'] ?? data ?? [];
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Coopératives')),
      body: _loading ? const Center(child: CircularProgressIndicator())
        : ListView.builder(
            itemCount: _coops.length,
            itemBuilder: (_, i) {
              final c = _coops[i];
              return Card(
                margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                child: ListTile(
                  leading: const Icon(Icons.groups, color: AppTheme.primaryGreen),
                  title: Text(c['name'] ?? ''),
                  subtitle: Text('${c['region'] ?? ''} — ${c['member_count'] ?? 0} membres'),
                  trailing: Text('${c['total_hectares'] ?? 0} ha'),
                  onTap: () => _api.post('/cooperatives/${c['id']}/join/', {}),
                ),
              );
            },
          ),
    );
  }
}
