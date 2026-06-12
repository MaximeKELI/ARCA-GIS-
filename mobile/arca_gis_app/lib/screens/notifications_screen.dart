import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

class NotificationsScreen extends StatefulWidget {
  const NotificationsScreen({super.key});

  @override
  State<NotificationsScreen> createState() => _NotificationsScreenState();
}

class _NotificationsScreenState extends State<NotificationsScreen> {
  final _api = ApiService();
  List<dynamic> _notifications = [];
  Map<String, dynamic> _prefs = {};

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final n = await _api.get('/notifications/history/');
      final p = await _api.get('/alerts/preferences/');
      setState(() {
        _notifications = parseApiList(n);
        _prefs = parseApiMap(p);
      });
    } catch (_) {}
  }

  Future<void> _togglePref(String key, bool value) async {
    await _api.patch('/alerts/preferences/', {key: value});
    setState(() => _prefs[key] = value);
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Notifications'),
          backgroundColor: AppTheme.primaryGreen,
          bottom: const TabBar(tabs: [Tab(text: 'Historique'), Tab(text: 'Préférences')]),
        ),
        body: TabBarView(children: [
          ListView.builder(
            itemCount: _notifications.length,
            itemBuilder: (_, i) {
              final n = _notifications[i] as Map<String, dynamic>;
              return ListTile(
                leading: const Icon(Icons.notifications),
                title: Text(n['title']?.toString() ?? ''),
                subtitle: Text(n['body']?.toString() ?? ''),
              );
            },
          ),
          ListView(
            children: ['climate', 'crop', 'sos', 'market'].map((key) {
              return SwitchListTile(
                title: Text(key),
                value: _prefs[key] == true,
                onChanged: (v) => _togglePref(key, v),
              );
            }).toList(),
          ),
        ]),
      ),
    );
  }
}
