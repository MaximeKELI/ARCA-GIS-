import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class BudgetScreen extends StatefulWidget {
  const BudgetScreen({super.key});
  @override
  State<BudgetScreen> createState() => _BudgetScreenState();
}

class _BudgetScreenState extends State<BudgetScreen> {
  final _api = ApiService();
  Map<String, dynamic> _summary = {};

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    try {
      final s = await _api.get('/farm/budget/summary/');
      setState(() => _summary = s is Map<String, dynamic> ? s : {});
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Budget fermier'), backgroundColor: AppTheme.primaryGreen),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(children: [
          _card('Revenus', _summary['income'], Colors.green),
          _card('Dépenses', _summary['expense'], Colors.red),
          _card('Solde', _summary['balance'], AppTheme.primaryGreen),
        ]),
      ),
    );
  }

  Widget _card(String label, dynamic value, Color color) => Card(
    child: ListTile(title: Text(label), trailing: Text('${value ?? 0} XOF', style: TextStyle(fontWeight: FontWeight.bold, color: color))),
  );
}
