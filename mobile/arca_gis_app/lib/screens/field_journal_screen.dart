import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

class FieldJournalScreen extends StatefulWidget {
  const FieldJournalScreen({super.key});
  @override
  State<FieldJournalScreen> createState() => _FieldJournalScreenState();
}

class _FieldJournalScreenState extends State<FieldJournalScreen> {
  final _api = ApiService();
  List<dynamic> _entries = [];

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    try {
      final data = await _api.get('/farm/journal/');
      setState(() => _entries = parseApiList(data));
    } catch (_) {}
  }

  Future<void> _add() async {
    final obs = TextEditingController();
    final weather = TextEditingController();
    final ok = await showDialog<bool>(context: context, builder: (ctx) => AlertDialog(
      title: const Text('Nouvelle observation'),
      content: Column(mainAxisSize: MainAxisSize.min, children: [
        TextField(controller: obs, decoration: const InputDecoration(labelText: 'Observation'), maxLines: 3),
        TextField(controller: weather, decoration: const InputDecoration(labelText: 'Météo')),
      ]),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Annuler')),
        TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Enregistrer')),
      ],
    ));
    if (ok != true || obs.text.isEmpty) return;
    await _api.post('/farm/journal/', {
      'observation': obs.text, 'weather_note': weather.text,
      'entry_date': DateTime.now().toIso8601String().substring(0, 10),
    });
    _load();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Journal de champ'), backgroundColor: AppTheme.primaryGreen),
      floatingActionButton: FloatingActionButton(onPressed: _add, child: const Icon(Icons.add)),
      body: ListView.builder(
        itemCount: _entries.length,
        itemBuilder: (_, i) {
          final e = _entries[i] as Map<String, dynamic>;
          return Card(
            margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            child: ListTile(
              title: Text(e['observation']?.toString() ?? ''),
              subtitle: Text('${e['entry_date']} · ${e['weather_note'] ?? ''}'),
            ),
          );
        },
      ),
    );
  }
}
