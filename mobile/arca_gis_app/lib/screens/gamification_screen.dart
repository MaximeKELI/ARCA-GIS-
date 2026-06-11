import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class GamificationScreen extends StatefulWidget {
  const GamificationScreen({super.key});

  @override
  State<GamificationScreen> createState() => _GamificationScreenState();
}

class _GamificationScreenState extends State<GamificationScreen> {
  final _api = ApiService();
  Map<String, dynamic> _profile = {};
  List<dynamic> _leaderboard = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final profile = await _api.get('/gamification/me/');
      final board = await _api.get('/gamification/leaderboard/');
      setState(() {
        _profile = profile is Map<String, dynamic> ? profile : {};
        _leaderboard = board is List ? board : [];
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Badges & Points'), backgroundColor: AppTheme.primaryGreen),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                Card(
                  color: AppTheme.primaryGreen,
                  child: Padding(
                    padding: const EdgeInsets.all(20),
                    child: Row(
                      children: [
                        const Icon(Icons.emoji_events, color: Colors.amber, size: 48),
                        const SizedBox(width: 16),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('${_profile['total_points'] ?? 0} points',
                                style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
                            Text('Niveau ${_profile['level'] ?? 1}', style: const TextStyle(color: Colors.white70)),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                const Text('Classement', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                ..._leaderboard.take(10).map((e) {
                  final entry = e as Map<String, dynamic>;
                  return ListTile(
                    leading: CircleAvatar(child: Text('${i + 1}')),
                    title: Text(e['username']?.toString() ?? ''),
                    trailing: Text('${e['total_points'] ?? 0} pts'),
                  );
                }),
              ],
            ),
    );
  }
}
