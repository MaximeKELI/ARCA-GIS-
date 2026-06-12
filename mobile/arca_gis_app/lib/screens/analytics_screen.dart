import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';
import '../widgets/modern_charts.dart';

class AnalyticsScreen extends StatefulWidget {
  const AnalyticsScreen({super.key});

  @override
  State<AnalyticsScreen> createState() => _AnalyticsScreenState();
}

class _AnalyticsScreenState extends State<AnalyticsScreen> with SingleTickerProviderStateMixin {
  final _api = ApiService();
  Map<String, dynamic> _data = {};
  bool _loading = true;
  late TabController _tabs;

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
      final data = await _api.get('/analytics/visual/');
      setState(() { _data = parseApiMap(data); _loading = false; });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  List<Map<String, dynamic>> _list(dynamic key) =>
      (_data[key] as List?)?.cast<Map<String, dynamic>>() ?? [];

  Map<String, dynamic> _map(dynamic key) => (_data[key] as Map<String, dynamic>?) ?? {};

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _loading
          ? const Center(child: CircularProgressIndicator(color: AppTheme.primaryGreen))
          : NestedScrollView(
              headerSliverBuilder: (context, _) => [
                SliverAppBar(
                  expandedHeight: 180,
                  pinned: true,
                  flexibleSpace: FlexibleSpaceBar(
                    title: const Text('Statistiques', style: TextStyle(fontWeight: FontWeight.bold)),
                    background: Container(
                      decoration: const BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                          colors: [Color(0xFF1B5E20), Color(0xFF2E7D32), Color(0xFF43A047)],
                        ),
                      ),
                      child: Stack(children: [
                        Positioned(right: -30, top: -30, child: _glowCircle(120, 0.08)),
                        Positioned(left: -20, bottom: 20, child: _glowCircle(80, 0.06)),
                        if (_data.isNotEmpty)
                          Positioned(
                            left: 16, bottom: 16, right: 16,
                            child: Text(
                              'Superficie totale: ${_map('summary')['total_area_ha'] ?? 0} ha',
                              style: TextStyle(color: Colors.white.withValues(alpha: 0.85), fontSize: 13),
                            ),
                          ),
                      ]),
                    ),
                  ),
                  bottom: TabBar(
                    controller: _tabs,
                    isScrollable: true,
                    indicatorColor: Colors.white,
                    labelColor: Colors.white,
                    unselectedLabelColor: Colors.white70,
                    tabs: const [
                      Tab(text: 'Vue d\'ensemble'),
                      Tab(text: 'Agriculture'),
                      Tab(text: 'Finance'),
                      Tab(text: 'Climat'),
                    ],
                  ),
                ),
              ],
              body: RefreshIndicator(
                onRefresh: _load,
                child: TabBarView(
                  controller: _tabs,
                  children: [
                    _overviewTab(),
                    _agricultureTab(),
                    _financeTab(),
                    _climateTab(),
                  ],
                ),
              ),
            ),
    );
  }

  Widget _glowCircle(double size, double opacity) => Container(
    width: size, height: size,
    decoration: BoxDecoration(shape: BoxShape.circle, color: Colors.white.withValues(alpha: opacity)),
  );

  Widget _overviewTab() {
    final kpis = _list('kpis');
    final radar = _map('radar');
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          mainAxisSpacing: 12,
          crossAxisSpacing: 12,
          childAspectRatio: 1.35,
          children: kpis.map((k) => ModernCharts.kpiCard(
            label: k['label']?.toString() ?? '',
            value: '${k['value']}',
            unit: k['unit']?.toString() ?? '',
            color: ModernCharts.colorFromHex(k['color']?.toString()),
            icon: ModernCharts.iconFromName(k['icon']?.toString()),
            delta: (k['delta'] as num?)?.toDouble(),
            sparkline: k['key'] == 'moisture'
                ? (_map('sparklines')['moisture'] as List?)?.cast<num>().map((e) => e.toDouble()).toList()
                : null,
          )).toList(),
        ),
        const SizedBox(height: 8),
        if (radar.isNotEmpty)
          ModernCharts.radarChart(
            title: 'Score santé fermière',
            labels: (radar['labels'] as List?)?.cast<String>() ?? [],
            values: (radar['values'] as List?)?.cast<num>().map((e) => e.toDouble()).toList() ?? [],
          ),
        ModernCharts.donutChart(
          title: 'Répartition cultures',
          data: (_map('distributions')['crop_types'] as List?)?.cast<Map<String, dynamic>>() ?? [],
        ),
        ModernCharts.donutChart(
          title: 'État sanitaire parcelles',
          data: (_map('distributions')['health_status'] as List?)?.cast<Map<String, dynamic>>() ?? [],
        ),
      ],
    );
  }

  Widget _agricultureTab() {
    final series = _map('series');
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        ModernCharts.gradientLineChart(
          title: 'Humidité du sol (6 mois)',
          data: (series['moisture_trend'] as List?)?.cast<Map<String, dynamic>>() ?? [],
          color: AppTheme.climateBlue,
          valueSuffix: '%',
        ),
        ModernCharts.gradientLineChart(
          title: 'Indice NDVI',
          data: (series['ndvi_trend'] as List?)?.cast<Map<String, dynamic>>() ?? [],
          color: AppTheme.primaryGreen,
        ),
        ModernCharts.barChart(
          title: 'Récoltes mensuelles (kg)',
          data: (series['harvest_monthly'] as List?)?.cast<Map<String, dynamic>>() ?? [],
          color: AppTheme.accentOrange,
        ),
        ModernCharts.donutChart(
          title: 'Statut des tâches',
          data: (_map('distributions')['task_status'] as List?)?.cast<Map<String, dynamic>>() ?? [],
        ),
      ],
    );
  }

  Widget _financeTab() {
    final series = _map('series');
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        ModernCharts.groupedBarChart(
          title: 'Revenus vs Dépenses (6 mois)',
          income: (series['budget_income'] as List?)?.cast<Map<String, dynamic>>() ?? [],
          expense: (series['budget_expense'] as List?)?.cast<Map<String, dynamic>>() ?? [],
        ),
        ModernCharts.donutChart(
          title: 'Dépenses par catégorie',
          data: (_map('distributions')['budget_categories'] as List?)?.cast<Map<String, dynamic>>() ?? [],
        ),
        _marketPricesCard(),
      ],
    );
  }

  Widget _climateTab() {
    final series = _map('series');
    final summary = _map('summary');
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Row(children: [
          Expanded(child: _miniStat('SOS actifs', '${summary['active_sos'] ?? 0}', AppTheme.sosRed, Icons.emergency)),
          const SizedBox(width: 12),
          Expanded(child: _miniStat('Événements climat', '${summary['climate_events'] ?? 0}', AppTheme.climateBlue, Icons.cloud)),
        ]),
        const SizedBox(height: 16),
        ModernCharts.barChart(
          title: 'Pluviométrie mensuelle (mm)',
          data: (series['rainfall'] as List?)?.cast<Map<String, dynamic>>() ?? [],
          color: AppTheme.climateBlue,
        ),
        ModernCharts.gradientLineChart(
          title: 'Tendance humidité',
          data: (series['moisture_trend'] as List?)?.cast<Map<String, dynamic>>() ?? [],
          color: const Color(0xFF00838F),
          valueSuffix: '%',
        ),
      ],
    );
  }

  Widget _miniStat(String label, String value, Color color, IconData icon) => Container(
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(
      color: color.withValues(alpha: 0.1),
      borderRadius: BorderRadius.circular(16),
      border: Border.all(color: color.withValues(alpha: 0.2)),
    ),
    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Icon(icon, color: color, size: 22),
      const SizedBox(height: 8),
      Text(value, style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: color)),
      Text(label, style: TextStyle(fontSize: 11, color: Colors.grey.shade600)),
    ]),
  );

  Widget _marketPricesCard() {
    final prices = _list('market_prices');
    if (prices.isEmpty) return const SizedBox();
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.06), blurRadius: 16, offset: const Offset(0, 4))],
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Padding(
          padding: EdgeInsets.fromLTRB(16, 16, 16, 0),
          child: Text('Prix marché', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
        ),
        ...prices.map((p) => ListTile(
          dense: true,
          leading: const Icon(Icons.sell, color: AppTheme.accentOrange, size: 20),
          title: Text('${p['crop']} — ${p['region']}'),
          trailing: Text('${p['price']} XOF/kg', style: const TextStyle(fontWeight: FontWeight.bold)),
        )),
      ]),
    );
  }
}
