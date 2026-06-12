import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class MentorshipScreen extends StatefulWidget {
  const MentorshipScreen({super.key});

  @override
  State<MentorshipScreen> createState() => _MentorshipScreenState();
}

class _MentorshipScreenState extends State<MentorshipScreen> {
  final _api = ApiService();
  List<dynamic> _mentorships = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final data = await _api.get('/mentorship/');
      setState(() { _mentorships = data is List ? data : []; _loading = false; });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Mentorat'), backgroundColor: AppTheme.primaryGreen),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _mentorships.isEmpty
              ? const Center(child: Text('Aucun mentorat actif'))
              : ListView.builder(
                  itemCount: _mentorships.length,
                  itemBuilder: (_, i) {
                    final m = _mentorships[i] as Map<String, dynamic>;
                    return Card(
                      margin: const EdgeInsets.all(12),
                      child: ListTile(
                        leading: const Icon(Icons.school, color: AppTheme.primaryGreen),
                        title: Text('${m['mentor_name'] ?? ''} → ${m['mentee_name'] ?? ''}'),
                        subtitle: Text('Culture: ${m['focus_crop'] ?? '—'} · ${m['status'] ?? ''}'),
                      ),
                    );
                  },
                ),
    );
  }
}
