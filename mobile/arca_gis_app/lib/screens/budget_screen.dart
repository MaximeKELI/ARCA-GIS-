import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';
import '../widgets/modern_charts.dart';

class BudgetScreen extends StatefulWidget {
  const BudgetScreen({super.key});
  @override
  State<BudgetScreen> createState() => _BudgetScreenState();
}

class _BudgetScreenState extends State<BudgetScreen> {
  final _api = ApiService();
  Map<String, dynamic> _summary = {};
  Map<String, dynamic> _visual = {};
  Map<String, dynamic>? _loanResult;

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    try {
      final s = await _api.get('/farm/budget/summary/');
      final v = await _api.get('/analytics/visual/');
      setState(() {
        _summary = parseApiMap(s);
        _visual = parseApiMap(v);
      });
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
    final series = (_visual['series'] as Map<String, dynamic>?) ?? {};
    final dist = (_visual['distributions'] as Map<String, dynamic>?) ?? {};
    return Scaffold(
      appBar: AppBar(title: const Text('Budget fermier'), backgroundColor: AppTheme.primaryGreen,
        actions: [IconButton(icon: const Icon(Icons.calculate), onPressed: _calcLoan)]),
      body: RefreshIndicator(
        onRefresh: _load,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Row(children: [
              Expanded(child: ModernCharts.kpiCard(
                label: 'Revenus', value: '${_summary['income'] ?? 0}',
                unit: 'XOF', color: Colors.green, icon: Icons.arrow_upward,
              )),
              const SizedBox(width: 12),
              Expanded(child: ModernCharts.kpiCard(
                label: 'Dépenses', value: '${_summary['expense'] ?? 0}',
                unit: 'XOF', color: AppTheme.sosRed, icon: Icons.arrow_downward,
              )),
            ]),
            const SizedBox(height: 12),
            ModernCharts.kpiCard(
              label: 'Solde net', value: '${_summary['balance'] ?? 0}',
              unit: 'XOF', color: AppTheme.primaryGreen, icon: Icons.account_balance_wallet,
            ),
            const SizedBox(height: 8),
            ModernCharts.groupedBarChart(
              title: 'Revenus vs Dépenses',
              income: (series['budget_income'] as List?)?.cast<Map<String, dynamic>>() ?? [],
              expense: (series['budget_expense'] as List?)?.cast<Map<String, dynamic>>() ?? [],
            ),
            ModernCharts.donutChart(
              title: 'Répartition dépenses',
              data: (dist['budget_categories'] as List?)?.cast<Map<String, dynamic>>() ?? [],
            ),
            if (_loanResult != null) Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  const Text('Simulation prêt', style: TextStyle(fontWeight: FontWeight.bold)),
                  Text('Mensualité: ${_loanResult!['monthly_payment']} XOF'),
                  Text('Total remboursé: ${_loanResult!['total_paid']} XOF'),
                  Text('Intérêts: ${_loanResult!['total_interest']} XOF'),
                ]),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
