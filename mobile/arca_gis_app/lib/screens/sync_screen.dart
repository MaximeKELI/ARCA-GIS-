import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../services/offline_db.dart';

class SyncScreen extends StatefulWidget {
  const SyncScreen({super.key});
  @override
  State<SyncScreen> createState() => _SyncScreenState();
}

class _SyncScreenState extends State<SyncScreen> {
  final _db = OfflineDB();
  final _api = ApiService();
  List<Map<String, dynamic>> _pending = [];
  String? _status;

  @override
  void initState() { super.initState(); _refresh(); }

  Future<void> _refresh() async {
    final pending = await _db.pendingSOS();
    setState(() => _pending = pending);
  }

  Future<void> _syncAll() async {
    setState(() => _status = 'Synchronisation...');
    try {
      for (final item in _pending) {
        await _api.post('/core/offline/sync/', {
          'action_type': 'sos', 'payload': item,
        });
      }
      await _api.post('/core/offline/process/', {});
      setState(() => _status = 'Sync terminée');
      await _refresh();
    } catch (e) {
      setState(() => _status = 'Erreur: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Sync offline'), backgroundColor: AppTheme.primaryGreen),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Text('${_pending.length} élément(s) en attente', style: const TextStyle(fontSize: 16)),
          if (_status != null) Text(_status!, style: TextStyle(color: AppTheme.primaryGreen)),
          const SizedBox(height: 16),
          ElevatedButton(onPressed: _syncAll, child: const Text('Synchroniser maintenant')),
        ]),
      ),
    );
  }
}
