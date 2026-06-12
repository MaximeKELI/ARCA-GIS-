import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class RoleDashboardScreen extends StatefulWidget {
  const RoleDashboardScreen({super.key});
  @override
  State<RoleDashboardScreen> createState() => _RoleDashboardScreenState();
}

class _RoleDashboardScreenState extends State<RoleDashboardScreen> {
  final _api = ApiService();
  Map<String, dynamic> _data = {};

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    try {
      final data = await _api.get('/analytics/role-dashboard/');
      setState(() => _data = data is Map<String, dynamic> ? data : {});
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    final role = _data['role']?.toString() ?? '—';
    final stats = (_data['stats'] as Map<String, dynamic>?) ?? {};
    return Scaffold(
      appBar: AppBar(title: Text('Dashboard ($role)'), backgroundColor: AppTheme.primaryGreen),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: stats.entries.map((e) => Card(
          child: ListTile(title: Text(e.key), trailing: Text('${e.value}')),
        )).toList(),
      ),
    );
  }
}
