import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class SubscriptionsScreen extends StatefulWidget {
  const SubscriptionsScreen({super.key});

  @override
  State<SubscriptionsScreen> createState() => _SubscriptionsScreenState();
}

class _SubscriptionsScreenState extends State<SubscriptionsScreen> {
  final _api = ApiService();
  List<dynamic> _plans = [];
  Map<String, dynamic> _current = {};
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final plans = await _api.get('/subscriptions/plans/');
      final sub = await _api.get('/subscriptions/my/');
      setState(() {
        _plans = plans is List ? plans : [];
        _current = sub is Map<String, dynamic> ? sub : {};
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  Future<void> _subscribe(String tier) async {
    try {
      await _api.post('/payments/initiate/', {
        'provider': 'orange_money', 'amount': 5000, 'description': 'Abonnement $tier',
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Paiement initié')));
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Erreur: $e')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Abonnements'), backgroundColor: AppTheme.primaryGreen),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                if (_current.isNotEmpty)
                  Card(
                    color: AppTheme.primaryGreen,
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Text(
                        'Plan actuel: ${(_current['plan_detail'] as Map?)?['name'] ?? 'Gratuit'}',
                        style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                const SizedBox(height: 16),
                ..._plans.map((p) {
                  final plan = p as Map<String, dynamic>;
                  return Card(
                    margin: const EdgeInsets.only(bottom: 12),
                    child: ListTile(
                      title: Text(plan['name']?.toString() ?? '', style: const TextStyle(fontWeight: FontWeight.bold)),
                      subtitle: Text('${plan['price_monthly'] ?? 0} XOF/mois · ${plan['max_parcels'] ?? 3} parcelles'),
                      trailing: ElevatedButton(
                        onPressed: () => _subscribe(plan['tier']?.toString() ?? ''),
                        child: const Text('Choisir'),
                      ),
                    ),
                  );
                }),
              ],
            ),
    );
  }
}
