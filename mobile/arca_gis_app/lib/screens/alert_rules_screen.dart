import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

class AlertRulesScreen extends StatefulWidget {
  const AlertRulesScreen({super.key});
  @override
  State<AlertRulesScreen> createState() => _AlertRulesScreenState();
}

class _AlertRulesScreenState extends State<AlertRulesScreen> {
  final _api = ApiService();
  List<dynamic> _rules = [];

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    try {
      final data = await _api.get('/alerts/rules/');
      setState(() => _rules = parseApiList(data));
    } catch (_) {}
  }

  Future<void> _evaluate() async {
    final r = await _api.post('/alerts/rules/evaluate/', {});
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('${(r as Map)['count'] ?? 0} règle(s) déclenchée(s)')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Règles d\'alertes'), backgroundColor: AppTheme.primaryGreen,
        actions: [IconButton(icon: const Icon(Icons.play_arrow), onPressed: _evaluate)]),
      body: ListView.builder(
        itemCount: _rules.length,
        itemBuilder: (_, i) {
          final r = _rules[i] as Map<String, dynamic>;
          return ListTile(
            title: Text(r['name']?.toString() ?? ''),
            subtitle: Text('${r['metric']} ${r['operator']} ${r['threshold']}'),
            trailing: Switch(value: r['is_active'] == true, onChanged: null),
          );
        },
      ),
    );
  }
}
