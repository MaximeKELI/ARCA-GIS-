import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

class ActivityFeedScreen extends StatefulWidget {
  const ActivityFeedScreen({super.key});

  @override
  State<ActivityFeedScreen> createState() => _ActivityFeedScreenState();
}

class _ActivityFeedScreenState extends State<ActivityFeedScreen> {
  final _api = ApiService();
  List<dynamic> _items = [];

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final data = await _api.get('/core/activity/');
      setState(() => _items = parseApiList(data));
    } catch (_) {}
  }

  IconData _icon(String type) => switch (type) {
    'harvest' => Icons.agriculture,
    'journal' => Icons.menu_book,
    'task' => Icons.task_alt,
    'parcel_change' => Icons.edit_location_alt,
    _ => Icons.circle,
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Activité récente'), backgroundColor: AppTheme.primaryGreen),
      body: RefreshIndicator(
        onRefresh: _load,
        child: ListView.builder(
          itemCount: _items.length,
          itemBuilder: (_, i) {
            final item = _items[i] as Map<String, dynamic>;
            return ListTile(
              leading: Icon(_icon(item['type']?.toString() ?? ''), color: AppTheme.primaryGreen),
              title: Text(item['title']?.toString() ?? ''),
              subtitle: Text(item['date']?.toString() ?? ''),
            );
          },
        ),
      ),
    );
  }
}
