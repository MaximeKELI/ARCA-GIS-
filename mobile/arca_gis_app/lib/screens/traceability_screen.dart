import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class TraceabilityScreen extends StatefulWidget {
  const TraceabilityScreen({super.key});
  @override
  State<TraceabilityScreen> createState() => _TraceabilityScreenState();
}

class _TraceabilityScreenState extends State<TraceabilityScreen> {
  final ApiService _api = ApiService();
  List<dynamic> _harvests = [];

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    final data = await _api.get('/traceability/harvests/');
    setState(() => _harvests = data['results'] ?? data ?? []);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Traçabilité Blockchain')),
      body: ListView.builder(
        itemCount: _harvests.length,
        itemBuilder: (_, i) {
          final h = _harvests[i];
          return Card(
            margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
            child: ListTile(
              leading: const Icon(Icons.verified, color: AppTheme.primaryGreen),
              title: Text(h['certificate_id'] ?? ''),
              subtitle: Text('${h['crop_type']} — ${h['quantity_kg']} kg\nHash: ${(h['blockchain_hash'] ?? '').toString().substring(0, 16)}...'),
              isThreeLine: true,
            ),
          );
        },
      ),
    );
  }
}
