import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class InsuranceScreen extends StatefulWidget {
  const InsuranceScreen({super.key});

  @override
  State<InsuranceScreen> createState() => _InsuranceScreenState();
}

class _InsuranceScreenState extends State<InsuranceScreen> {
  final _api = ApiService();
  List<dynamic> _policies = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final data = await _api.get('/insurance/policies/');
      setState(() { _policies = data is List ? data : []; _loading = false; });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Assurance paramétrique'), backgroundColor: AppTheme.primaryGreen),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _policies.isEmpty
              ? const Center(child: Text('Aucune police active'))
              : ListView.builder(
                  itemCount: _policies.length,
                  itemBuilder: (_, i) {
                    final p = _policies[i] as Map<String, dynamic>;
                    return Card(
                      margin: const EdgeInsets.all(12),
                      child: ListTile(
                        leading: const Icon(Icons.shield, color: AppTheme.primaryGreen),
                        title: Text(p['policy_type_display']?.toString() ?? p['policy_type']?.toString() ?? ''),
                        subtitle: Text('Couverture: ${p['coverage_amount'] ?? 0} XOF'),
                        trailing: Chip(
                          label: Text(p['is_active'] == true ? 'active' : 'inactive'),
                          backgroundColor: p['is_active'] == true ? Colors.green.shade100 : Colors.grey.shade200,
                        ),
                      ),
                    );
                  },
                ),
    );
  }
}
