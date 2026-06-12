import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class CoopHubScreen extends StatefulWidget {
  const CoopHubScreen({super.key});
  @override
  State<CoopHubScreen> createState() => _CoopHubScreenState();
}

class _CoopHubScreenState extends State<CoopHubScreen> {
  final _api = ApiService();
  List<dynamic> _votes = [];
  List<dynamic> _equipment = [];

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    try {
      final v = await _api.get('/cooperatives/votes/');
      final e = await _api.get('/cooperatives/equipment/');
      setState(() {
        _votes = v is List ? v : [];
        _equipment = e is List ? e : [];
      });
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Coopérative'),
          backgroundColor: AppTheme.primaryGreen,
          bottom: const TabBar(tabs: [Tab(text: 'Votes'), Tab(text: 'Équipement')]),
        ),
        body: TabBarView(children: [
          ListView.builder(itemCount: _votes.length, itemBuilder: (_, i) {
            final v = _votes[i] as Map<String, dynamic>;
            return ListTile(title: Text(v['title']?.toString() ?? ''), subtitle: Text(v['ends_at']?.toString() ?? ''));
          }),
          ListView.builder(itemCount: _equipment.length, itemBuilder: (_, i) {
            final e = _equipment[i] as Map<String, dynamic>;
            return ListTile(title: Text(e['equipment']?.toString() ?? ''), subtitle: Text('${e['start']} → ${e['end']}'));
          }),
        ]),
      ),
    );
  }
}
