import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

class TasksScreen extends StatefulWidget {
  const TasksScreen({super.key});
  @override
  State<TasksScreen> createState() => _TasksScreenState();
}

class _TasksScreenState extends State<TasksScreen> {
  final _api = ApiService();
  List<dynamic> _tasks = [];

  Future<void> _load() async {
    try {
      final data = await _api.get('/farm/tasks/');
      setState(() => _tasks = parseApiList(data));
    } catch (_) {}
  }

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _complete(int id) async {
    await _api.post('/farm/tasks/$id/complete/', {});
    _load();
  }

  Future<void> _generate() async {
    await _api.post('/farm/tasks/generate/', {});
    _load();
    if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Tâches générées')));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Planificateur'), backgroundColor: AppTheme.primaryGreen,
        actions: [IconButton(icon: const Icon(Icons.auto_awesome), onPressed: _generate)]),
      body: ListView.builder(
        itemCount: _tasks.length,
        itemBuilder: (_, i) {
          final t = _tasks[i] as Map<String, dynamic>;
          final done = t['status'] == 'done';
          return CheckboxListTile(
            value: done,
            onChanged: done ? null : (_) => _complete(t['id'] as int),
            title: Text(t['title']?.toString() ?? ''),
            subtitle: Text('Échéance: ${t['due_date']}'),
          );
        },
      ),
    );
  }
}
