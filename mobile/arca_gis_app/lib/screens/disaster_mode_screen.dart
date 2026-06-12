import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../services/offline_db.dart';

class DisasterModeScreen extends StatefulWidget {
  const DisasterModeScreen({super.key});

  @override
  State<DisasterModeScreen> createState() => _DisasterModeScreenState();
}

class _DisasterModeScreenState extends State<DisasterModeScreen> {
  final _db = OfflineDB();
  final _api = ApiService();
  bool _enabled = false;
  List<String> _checklist = [];

  @override
  void initState() {
    super.initState();
    _init();
  }

  Future<void> _init() async {
    _enabled = await _db.isDisasterMode();
    try {
      final data = await _api.get('/incidents/evacuation-checklist/?type=flood');
      setState(() => _checklist = (data['steps'] as List?)?.cast<String>() ?? []);
    } catch (_) {
      setState(() => _checklist = ['Monter en hauteur', 'Couper électricité', 'Signaler position SOS']);
    }
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Mode catastrophe'), backgroundColor: AppTheme.sosRed),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            SwitchListTile(
              title: const Text('Activer mode catastrophe offline', style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: const Text('SOS et données stockées localement'),
              value: _enabled,
              onChanged: (v) async {
                await _db.setDisasterMode(v);
                setState(() => _enabled = v);
              },
            ),
            const SizedBox(height: 16),
            const Align(alignment: Alignment.centerLeft, child: Text('Checklist évacuation', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold))),
            ..._checklist.map((s) => ListTile(leading: const Icon(Icons.check_circle_outline), title: Text(s))),
            const Spacer(),
            ElevatedButton.icon(
              onPressed: () async {
                await _db.queueSOS({'type': 'flood', 'ts': DateTime.now().toIso8601String()});
                if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('SOS enregistré offline')));
              },
              icon: const Icon(Icons.warning),
              label: const Text('SOS OFFLINE'),
              style: ElevatedButton.styleFrom(backgroundColor: AppTheme.sosRed, minimumSize: const Size(double.infinity, 48)),
            ),
          ],
        ),
      ),
    );
  }
}
