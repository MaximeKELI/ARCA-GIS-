import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

/// Hub agriculture étendue : apiculture, aquaculture, semencier, agroforesterie, compost.
class AgroHubScreen extends StatefulWidget {
  const AgroHubScreen({super.key});

  @override
  State<AgroHubScreen> createState() => _AgroHubScreenState();
}

class _AgroHubScreenState extends State<AgroHubScreen> with SingleTickerProviderStateMixin {
  final _api = ApiService();
  late TabController _tabs;
  List<dynamic> _hives = [];
  List<dynamic> _ponds = [];
  List<dynamic> _seeds = [];
  List<dynamic> _plots = [];
  List<dynamic> _compost = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _tabs = TabController(length: 5, vsync: this);
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
      final results = await Future.wait([
        _api.get('/agro/beekeeping/hives/'),
        _api.get('/agro/aquaculture/ponds/'),
        _api.get('/agro/seedbank/'),
        _api.get('/agro/agroforestry/plots/'),
        _api.get('/agro/compost/'),
      ]);
      setState(() {
        _hives = parseApiList(results[0]);
        _ponds = parseApiList(results[1]);
        _seeds = parseApiList(results[2]);
        _plots = parseApiList(results[3]);
        _compost = parseApiList(results[4]);
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  Future<void> _rotationPlan() async {
    final r = await _api.post('/agro/rotation-plan/', {'parcel_id': 1, 'current_crop': 'maize'});
    if (!mounted) return;
    final years = (r['plan_years'] as List?) ?? [];
    showDialog(context: context, builder: (ctx) => AlertDialog(
      title: const Text('Plan rotation 3 ans'),
      content: Column(mainAxisSize: MainAxisSize.min, children: years.map((y) {
        final m = y as Map<String, dynamic>;
        return ListTile(
          dense: true,
          title: Text('An ${m['year']}: ${m['crop']}'),
          subtitle: Text(m['reason']?.toString() ?? ''),
        );
      }).toList()),
      actions: [TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('OK'))],
    ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Agriculture étendue'),
        backgroundColor: AppTheme.primaryGreen,
        actions: [IconButton(icon: const Icon(Icons.autorenew), onPressed: _rotationPlan, tooltip: 'Rotation IA')],
        bottom: TabBar(
          controller: _tabs,
          isScrollable: true,
          indicatorColor: Colors.white,
          labelColor: Colors.white,
          unselectedLabelColor: Colors.white70,
          tabs: const [
            Tab(icon: Icon(Icons.hive), text: 'Apiculture'),
            Tab(icon: Icon(Icons.water), text: 'Aquaculture'),
            Tab(icon: Icon(Icons.grain), text: 'Semencier'),
            Tab(icon: Icon(Icons.park), text: 'Agroforêt'),
            Tab(icon: Icon(Icons.recycling), text: 'Compost'),
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
                  _listTab(_hives, Icons.hive, (h) => [
                    Text(h['name']?.toString() ?? '', style: const TextStyle(fontWeight: FontWeight.w600)),
                    Text('Miel: ${h['honey_production_kg'] ?? 0} kg · Force: ${h['colony_strength'] ?? ''}'),
                    if (h['swarm_alert'] == true) const Chip(label: Text('Essaim!', backgroundColor: Colors.orange)),
                  ]),
                  _listTab(_ponds, Icons.water, (p) => [
                    Text(p['name']?.toString() ?? '', style: const TextStyle(fontWeight: FontWeight.w600)),
                    Text('${p['fish_species']} · ${p['stock_count']} poissons · ${p['water_quality']}'),
                    Text('Mortalité: ${p['mortality_rate'] ?? 0}%'),
                  ]),
                  _listTab(_seeds, Icons.grain, (s) => [
                    Text('${s['crop_type']} — ${s['variety']}', style: const TextStyle(fontWeight: FontWeight.w600)),
                    Text('${s['quantity_kg']} kg · ${s['region']} · ${s['harvest_year']}'),
                  ]),
                  _listTab(_plots, Icons.park, (p) => [
                    Text(p['name']?.toString() ?? '', style: const TextStyle(fontWeight: FontWeight.w600)),
                    Text('${p['tree_count']} arbres · ${p['crop_association'] ?? ''}'),
                    Text('Bonus carbone: ${p['carbon_bonus'] ?? 0} t'),
                  ]),
                  _listTab(_compost, Icons.recycling, (c) => [
                    Text(c['name']?.toString() ?? '', style: const TextStyle(fontWeight: FontWeight.w600)),
                    Text('${c['volume_m3']} m³ · Maturité ${c['maturity_pct'] ?? 0}%'),
                    LinearProgressIndicator(value: ((c['maturity_pct'] as num?) ?? 0) / 100, color: AppTheme.primaryGreen),
                  ]),
                ],
              ),
            ),
    );
  }

  Widget _listTab(List<dynamic> items, IconData icon, List<Widget> Function(Map<String, dynamic>) builder) {
    if (items.isEmpty) {
      return ListView(children: const [SizedBox(height: 80), Center(child: Text('Aucune donnée'))]);
    }
    return ListView.builder(
      padding: const EdgeInsets.all(12),
      itemCount: items.length,
      itemBuilder: (_, i) {
        final item = items[i] as Map<String, dynamic>;
        return Card(
          margin: const EdgeInsets.only(bottom: 10),
          child: ListTile(
            leading: CircleAvatar(backgroundColor: AppTheme.primaryGreen.withValues(alpha: 0.15), child: Icon(icon, color: AppTheme.primaryGreen)),
            title: Column(crossAxisAlignment: CrossAxisAlignment.start, children: builder(item)),
          ),
        );
      },
    );
  }
}
