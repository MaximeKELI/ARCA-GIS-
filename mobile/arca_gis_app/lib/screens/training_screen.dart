import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class TrainingScreen extends StatefulWidget {
  const TrainingScreen({super.key});

  @override
  State<TrainingScreen> createState() => _TrainingScreenState();
}

class _TrainingScreenState extends State<TrainingScreen> {
  final _api = ApiService();
  List<dynamic> _courses = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final data = await _api.get('/training/courses/');
      setState(() { _courses = data is List ? data : []; _loading = false; });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Formation agricole'), backgroundColor: AppTheme.primaryGreen),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: _courses.length,
              itemBuilder: (_, i) {
                final c = _courses[i] as Map<String, dynamic>;
                final progress = (c['progress_percent'] as num?)?.toDouble() ?? 0;
                return Card(
                  margin: const EdgeInsets.all(12),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(c['title']?.toString() ?? '', style: const TextStyle(fontWeight: FontWeight.bold)),
                        const SizedBox(height: 4),
                        Text(c['description']?.toString() ?? '', maxLines: 2, overflow: TextOverflow.ellipsis),
                        const SizedBox(height: 8),
                        LinearProgressIndicator(value: progress / 100, color: AppTheme.primaryGreen),
                        Text('${progress.toInt()}% complété'),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
