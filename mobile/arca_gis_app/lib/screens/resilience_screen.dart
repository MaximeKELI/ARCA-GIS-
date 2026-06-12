import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

class ResilienceScreen extends StatefulWidget {
  const ResilienceScreen({super.key});

  @override
  State<ResilienceScreen> createState() => _ResilienceScreenState();
}

class _ResilienceScreenState extends State<ResilienceScreen> with SingleTickerProviderStateMixin {
  final _api = ApiService();
  late TabController _tabs;
  List<dynamic> _refuges = [];
  List<dynamic> _warnings = [];
  Map<String, dynamic> _drought = {};
  List<dynamic> _radio = [];
  Map<String, dynamic>? _floodResult;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _tabs = TabController(length: 4, vsync: this);
    _load();
  }

  @override
  void dispose() {
    _tabs.dispose();
    super.dispose();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final refuges = await _api.get('/resilience/refuges/');
      final warnings = await _api.get('/resilience/early-warnings/');
      final drought = await _api.get('/resilience/drought-ews/?region=Bouaké');
      final radio = await _api.get('/resilience/radio-hf/');
      setState(() {
        _refuges = parseApiList(refuges);
        _warnings = parseApiList(warnings);
        _drought = parseApiMap(drought);
        _radio = parseApiList(radio);
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  Future<void> _simulateFlood() async {
    final rain = TextEditingController(text: '120');
    final elev = TextEditingController(text: '150');
    final ok = await showDialog<bool>(context: context, builder: (ctx) => AlertDialog(
      title: const Text('Simulation inondation'),
      content: Column(mainAxisSize: MainAxisSize.min, children: [
        TextField(controller: rain, decoration: const InputDecoration(labelText: 'Pluie (mm)'), keyboardType: TextInputType.number),
        TextField(controller: elev, decoration: const InputDecoration(labelText: 'Altitude (m)'), keyboardType: TextInputType.number),
      ]),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Annuler')),
        TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Simuler')),
      ],
    ));
    if (ok != true) return;
    final r = await _api.post('/resilience/flood-simulate/', {
      'rainfall_mm': double.tryParse(rain.text) ?? 120,
      'elevation_m': double.tryParse(elev.text) ?? 150,
    });
    setState(() => _floodResult = parseApiMap(r));
  }

  Color _levelColor(String? level) => switch (level) {
    'critical' || 'high' => AppTheme.sosRed,
    'moderate' || 'medium' || 'warning' => AppTheme.accentOrange,
    _ => AppTheme.climateBlue,
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Résilience & urgences'),
        backgroundColor: AppTheme.sosRed,
        actions: [IconButton(icon: const Icon(Icons.water), onPressed: _simulateFlood, tooltip: 'Simuler inondation')],
        bottom: TabBar(
          controller: _tabs,
          indicatorColor: Colors.white,
          labelColor: Colors.white,
          unselectedLabelColor: Colors.white70,
          tabs: const [
            Tab(text: 'Refuges'),
            Tab(text: 'Alertes'),
            Tab(text: 'Sécheresse'),
            Tab(text: 'Radio HF'),
          ],
        ),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _load,
              child: TabBarView(
                controller: _tabs,
                children: [
                  _refugesTab(),
                  _warningsTab(),
                  _droughtTab(),
                  _radioTab(),
                ],
              ),
            ),
    );
  }

  Widget _refugesTab() {
    if (_refuges.isEmpty) return ListView(children: const [Center(child: Text('Aucun refuge'))]);
    return ListView.builder(
      padding: const EdgeInsets.all(12),
      itemCount: _refuges.length,
      itemBuilder: (_, i) {
        final r = _refuges[i] as Map<String, dynamic>;
        return Card(
          child: ListTile(
            leading: const Icon(Icons.home_work, color: AppTheme.climateBlue),
            title: Text(r['name']?.toString() ?? ''),
            subtitle: Text('${r['type']} · ${r['region']} · Capacité ${r['capacity']}'),
            trailing: const Icon(Icons.place),
          ),
        );
      },
    );
  }

  Widget _warningsTab() {
    return ListView(
      padding: const EdgeInsets.all(12),
      children: [
        if (_floodResult != null) Card(
          color: AppTheme.sosRed.withValues(alpha: 0.1),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const Text('Simulation inondation', style: TextStyle(fontWeight: FontWeight.bold)),
              Text('Risque: ${_floodResult!['flood_risk_pct']}%'),
              Text('Évacuation: ${_floodResult!['evacuation_recommended'] == true ? 'OUI' : 'Non'}'),
            ]),
          ),
        ),
        ..._warnings.map((w) {
          final m = w as Map<String, dynamic>;
          return Card(
            child: ListTile(
              leading: Icon(Icons.warning, color: _levelColor(m['level']?.toString())),
              title: Text(m['title']?.toString() ?? ''),
              subtitle: Text('${m['hazard']} · ${m['region']} · ${m['forecast_days']}j'),
            ),
          );
        }),
      ],
    );
  }

  Widget _droughtTab() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Card(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [
                Icon(Icons.wb_sunny, color: _levelColor(_drought['risk_level']?.toString()), size: 32),
                const SizedBox(width: 12),
                Text('EWS Sécheresse 90j', style: Theme.of(context).textTheme.titleLarge),
              ]),
              const SizedBox(height: 16),
              Text('Région: ${_drought['region'] ?? '—'}'),
              Text('Niveau: ${_drought['risk_level'] ?? '—'}'),
              Text('Probabilité: ${((_drought['probability_drought'] as num? ?? 0) * 100).toStringAsFixed(0)}%'),
              const SizedBox(height: 12),
              const Text('Recommandations:', style: TextStyle(fontWeight: FontWeight.bold)),
              ...(( _drought['recommendations'] as List?) ?? []).map((r) => Text('• $r')),
            ]),
          ),
        ),
      ],
    );
  }

  Widget _radioTab() {
    if (_radio.isEmpty) {
      return ListView(children: const [Center(child: Text('Aucune station HF'))]);
    }
    return ListView.builder(
      padding: const EdgeInsets.all(12),
      itemCount: _radio.length,
      itemBuilder: (_, i) {
        final s = _radio[i] as Map<String, dynamic>;
        return Card(
          child: ListTile(
            leading: const Icon(Icons.radio, color: AppTheme.accentOrange),
            title: Text(s['name']?.toString() ?? ''),
            subtitle: Text('${s['frequency']} · ${s['region']}'),
          ),
        );
      },
    );
  }
}
