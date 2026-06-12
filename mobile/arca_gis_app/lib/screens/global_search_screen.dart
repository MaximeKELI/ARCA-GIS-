import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';
import 'harvest_screen.dart';
import 'coop_hub_screen.dart';
import 'parcels_screen.dart';
import 'tasks_screen.dart';
import 'training_screen.dart';

class GlobalSearchScreen extends StatefulWidget {
  const GlobalSearchScreen({super.key});

  @override
  State<GlobalSearchScreen> createState() => _GlobalSearchScreenState();
}

class _GlobalSearchScreenState extends State<GlobalSearchScreen> {
  final _api = ApiService();
  final _controller = TextEditingController();
  List<dynamic> _results = [];
  bool _searching = false;

  Future<void> _search(String q) async {
    if (q.length < 2) {
      setState(() => _results = []);
      return;
    }
    setState(() => _searching = true);
    try {
      final data = await _api.get('/core/search/?q=${Uri.encodeComponent(q)}');
      setState(() {
        _results = parseApiList(data['results']);
        _searching = false;
      });
    } catch (_) {
      setState(() => _searching = false);
    }
  }

  IconData _icon(String type) => switch (type) {
    'parcel' => Icons.agriculture,
    'task' => Icons.task_alt,
    'harvest' => Icons.grass,
    'cooperative' => Icons.groups,
    'course' => Icons.school,
    'forum' => Icons.forum,
    _ => Icons.search,
  };

  void _openResult(Map<String, dynamic> r) {
    final type = r['type']?.toString() ?? '';
    Widget screen = switch (type) {
      'parcel' => const ParcelsScreen(),
      'task' => const TasksScreen(),
      'harvest' => const HarvestScreen(),
      'cooperative' => const CoopHubScreen(),
      'course' => const TrainingScreen(),
      _ => const SizedBox(),
    };
    if (type == 'forum') return;
    Navigator.push(context, MaterialPageRoute(builder: (_) => screen));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: AppTheme.primaryGreen,
        title: TextField(
          controller: _controller,
          autofocus: true,
          style: const TextStyle(color: Colors.white),
          decoration: InputDecoration(
            hintText: 'Parcelles, tâches, coop, cours…',
            hintStyle: TextStyle(color: Colors.white.withValues(alpha: 0.7)),
            border: InputBorder.none,
            suffixIcon: IconButton(
              icon: const Icon(Icons.clear, color: Colors.white),
              onPressed: () { _controller.clear(); setState(() => _results = []); },
            ),
          ),
          onChanged: (v) => _search(v),
        ),
      ),
      body: _searching
          ? const Center(child: CircularProgressIndicator())
          : _results.isEmpty
              ? Center(child: Text(
                  _controller.text.length < 2 ? 'Tapez au moins 2 caractères' : 'Aucun résultat',
                  style: TextStyle(color: Colors.grey.shade600),
                ))
              : ListView.builder(
                  itemCount: _results.length,
                  itemBuilder: (_, i) {
                    final r = _results[i] as Map<String, dynamic>;
                    return ListTile(
                      leading: CircleAvatar(
                        backgroundColor: AppTheme.primaryGreen.withValues(alpha: 0.15),
                        child: Icon(_icon(r['type']?.toString() ?? ''), color: AppTheme.primaryGreen, size: 20),
                      ),
                      title: Text(r['title']?.toString() ?? ''),
                      subtitle: Text(r['subtitle']?.toString() ?? ''),
                      onTap: () => _openResult(r),
                    );
                  },
                ),
    );
  }
}
