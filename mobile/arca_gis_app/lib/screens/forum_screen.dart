import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class ForumScreen extends StatefulWidget {
  const ForumScreen({super.key});

  @override
  State<ForumScreen> createState() => _ForumScreenState();
}

class _ForumScreenState extends State<ForumScreen> {
  final _api = ApiService();
  List<dynamic> _posts = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final data = await _api.get('/forum/posts/');
      setState(() { _posts = data is List ? data : []; _loading = false; });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Forum communautaire'), backgroundColor: AppTheme.primaryGreen),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _posts.isEmpty
              ? const Center(child: Text('Aucun post pour le moment'))
              : ListView.builder(
                  itemCount: _posts.length,
                  itemBuilder: (_, i) {
                    final p = _posts[i] as Map<String, dynamic>;
                    return Card(
                      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      child: ListTile(
                        title: Text(p['title']?.toString() ?? ''),
                        subtitle: Text('${p['author_name'] ?? ''} · ${p['comment_count'] ?? 0} commentaires'),
                        trailing: Text('${p['likes'] ?? 0} ❤'),
                      ),
                    );
                  },
                ),
    );
  }
}
