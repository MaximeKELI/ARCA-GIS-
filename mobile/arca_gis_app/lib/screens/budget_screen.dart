import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

class BudgetScreen extends StatefulWidget {
  const BudgetScreen({super.key});
  @override
  State<BudgetScreen> createState() => _BudgetScreenState();
}

class _BudgetScreenState extends State<BudgetScreen> {
  final _api = ApiService();
  Map<String, dynamic> _summary = {};
  Map<String, dynamic>? _loanResult;

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    try {
      final s = await _api.get('/farm/budget/summary/');
      setState(() => _summary = parseApiMap(s));
    } catch (_) {}
  }

  Future<void> _calcLoan() async {
    final principal = TextEditingController(text: '100000');
    final months = TextEditingController(text: '12');
    final ok = await showDialog<bool>(context: context, builder: (ctx) => AlertDialog(
      title: const Text('Calculateur de prêt'),
      content: Column(mainAxisSize: MainAxisSize.min, children: [
        TextField(controller: principal, decoration: const InputDecoration(labelText: 'Montant (XOF)'), keyboardType: TextInputType.number),
        TextField(controller: months, decoration: const InputDecoration(labelText: 'Mois'), keyboardType: TextInputType.number),
      ]),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Annuler')),
        TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Calculer')),
      ],
    ));
    if (ok != true) return;
    final r = await _api.post('/farm/loan-calculator/', {
      'principal': double.tryParse(principal.text) ?? 100000,
      'months': int.tryParse(months.text) ?? 12,
    });
    setState(() => _loanResult = parseApiMap(r));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Budget fermier'), backgroundColor: AppTheme.primaryGreen,
        actions: [IconButton(icon: const Icon(Icons.calculate), onPressed: _calcLoan)]),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(children: [
          _card('Revenus', _summary['income'], Colors.green),
          _card('Dépenses', _summary['expense'], Colors.red),
          _card('Solde', _summary['balance'], AppTheme.primaryGreen),
          if (_loanResult != null) ...[
            const SizedBox(height: 16),
            Text('Mensualité: ${_loanResult!['monthly_payment']} XOF'),
            Text('Total: ${_loanResult!['total_paid']} XOF'),
          ],
        ]),
      ),
    );
  }

  Widget _card(String label, dynamic value, Color color) => Card(
    child: ListTile(title: Text(label), trailing: Text('${value ?? 0} XOF', style: TextStyle(fontWeight: FontWeight.bold, color: color))),
  );
}
