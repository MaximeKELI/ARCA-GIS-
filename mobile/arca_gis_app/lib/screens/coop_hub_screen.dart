import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

class CoopHubScreen extends StatefulWidget {
  const CoopHubScreen({super.key});
  @override
  State<CoopHubScreen> createState() => _CoopHubScreenState();
}

class _CoopHubScreenState extends State<CoopHubScreen> {
  final _api = ApiService();
  List<dynamic> _votes = [];
  List<dynamic> _equipment = [];
  List<dynamic> _members = [];
  int? _coopId;

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    try {
      final coops = parseApiList(await _api.get('/cooperatives/'));
      if (coops.isNotEmpty) {
        _coopId = (coops.first as Map)['id'] as int?;
        if (_coopId != null) {
          _members = parseApiList(await _api.get('/cooperatives/$_coopId/members/'));
        }
      }
      final v = await _api.get('/cooperatives/votes/');
      final e = await _api.get('/cooperatives/equipment/');
      setState(() {
        _votes = parseApiList(v);
        _equipment = parseApiList(e);
      });
    } catch (_) {}
  }

  Future<void> _castVote(int voteId) async {
    final choice = await showDialog<String>(context: context, builder: (ctx) => SimpleDialog(
      title: const Text('Voter'),
      children: [
        SimpleDialogOption(onPressed: () => Navigator.pop(ctx, 'oui'), child: const Text('Oui')),
        SimpleDialogOption(onPressed: () => Navigator.pop(ctx, 'non'), child: const Text('Non')),
      ],
    ));
    if (choice == null) return;
    await _api.post('/cooperatives/votes/$voteId/cast/', {'choice': choice});
    if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Vote enregistré')));
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Coopérative'),
          backgroundColor: AppTheme.primaryGreen,
          bottom: const TabBar(tabs: [Tab(text: 'Votes'), Tab(text: 'Équipement'), Tab(text: 'Membres')]),
        ),
        body: TabBarView(children: [
          ListView.builder(itemCount: _votes.length, itemBuilder: (_, i) {
            final v = _votes[i] as Map<String, dynamic>;
            return ListTile(
              title: Text(v['title']?.toString() ?? ''),
              subtitle: Text(v['ends_at']?.toString() ?? ''),
              trailing: IconButton(icon: const Icon(Icons.how_to_vote), onPressed: () => _castVote(v['id'] as int)),
            );
          }),
          ListView.builder(itemCount: _equipment.length, itemBuilder: (_, i) {
            final e = _equipment[i] as Map<String, dynamic>;
            return ListTile(title: Text(e['equipment']?.toString() ?? ''), subtitle: Text('${e['start']} → ${e['end']}'));
          }),
          ListView.builder(itemCount: _members.length, itemBuilder: (_, i) {
            final m = _members[i] as Map<String, dynamic>;
            return ListTile(
              leading: Icon(Icons.person, color: m['is_president'] == true ? Colors.amber : null),
              title: Text(m['name']?.toString() ?? m['username']?.toString() ?? ''),
              subtitle: Text('${m['role']} · ${m['region'] ?? ''}'),
            );
          }),
        ]),
      ),
    );
  }
}
