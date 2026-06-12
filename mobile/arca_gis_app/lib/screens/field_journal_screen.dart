import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

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
      setState(() => _entries = data is List ? data : []);
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Journal de champ'), backgroundColor: AppTheme.primaryGreen),
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
