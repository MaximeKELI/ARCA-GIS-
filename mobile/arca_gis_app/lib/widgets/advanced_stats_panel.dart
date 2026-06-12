import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';
import '../widgets/modern_charts.dart';
import '../providers/map_provider.dart';
import 'package:provider/provider.dart';

/// Panneau stats avancées (Bloc C) : choroplèthe, Sankey, timeline, saisons.
class AdvancedStatsPanel extends StatefulWidget {
  const AdvancedStatsPanel({super.key});

  @override
  State<AdvancedStatsPanel> createState() => _AdvancedStatsPanelState();
}

class _AdvancedStatsPanelState extends State<AdvancedStatsPanel> {
  final _api = ApiService();
  Map<String, dynamic> _data = {};
  bool _loading = true;
  int _months = 12;
  String _metric = 'moisture';

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final d = await _api.get('/analytics/advanced/?months=$_months&metric=$_metric');
      setState(() { _data = parseApiMap(d); _loading = false; });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    if (_loading) return const Center(child: CircularProgressIndicator());

    final choropleth = parseApiList(_data['choropleth']);
    final sankey = parseApiMap(_data['sankey']);
    final timeline = parseApiList(_data['timeline']);
    final season = parseApiMap(_data['season_compare']);
    final alertsWeekly = parseApiList(_data['alerts_weekly']);
    final coopRadar = parseApiMap(_data['coop_radar']);

    return RefreshIndicator(
      onRefresh: _load,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _filters(),
          const SizedBox(height: 12),
          if (choropleth.isNotEmpty) ...[
            ModernCharts.chartCard(title: 'Choroplèthe ($_metric)', accent: AppTheme.primaryGreen,
              child: _choroplethGrid(choropleth), isDark: isDark),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton.icon(
                icon: const Icon(Icons.map),
                label: const Text('Afficher sur la carte'),
                onPressed: () {
                  context.read<MapProvider>().setChoropleth(choropleth, _metric);
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Choroplèthe activée sur la carte')),
                  );
                },
              ),
            ),
          ],
          ModernCharts.sankeyChart(title: 'Flux budget (Sankey)', data: sankey, isDark: isDark),
          ModernCharts.seasonCompareChart(title: 'Comparaison saisons', data: season, isDark: isDark),
          ModernCharts.barChart(
            title: 'Alertes par semaine',
            data: alertsWeekly.cast<Map<String, dynamic>>(),
            color: AppTheme.sosRed,
            isDark: isDark,
          ),
          if ((coopRadar['labels'] as List?)?.isNotEmpty == true)
            ModernCharts.radarChart(
              title: 'Radar coop: ${coopRadar['coop_name']}',
              labels: (coopRadar['labels'] as List?)?.cast<String>() ?? [],
              values: (coopRadar['values'] as List?)?.cast<num>().map((e) => e.toDouble()).toList() ?? [],
              isDark: isDark,
            ),
          ModernCharts.chartCard(title: 'Timeline activité', accent: AppTheme.climateBlue,
            child: _timeline(timeline), isDark: isDark),
        ],
      ),
    );
  }

  Widget _filters() {
    return Row(children: [
      Expanded(child: DropdownButtonFormField<int>(
        initialValue: _months,
        decoration: const InputDecoration(labelText: 'Période', isDense: true),
        items: const [
          DropdownMenuItem(value: 6, child: Text('6 mois')),
          DropdownMenuItem(value: 12, child: Text('12 mois')),
          DropdownMenuItem(value: 24, child: Text('24 mois')),
        ],
        onChanged: (v) { if (v != null) { setState(() => _months = v); _load(); } },
      )),
      const SizedBox(width: 12),
      Expanded(child: DropdownButtonFormField<String>(
        initialValue: _metric,
        decoration: const InputDecoration(labelText: 'Métrique', isDense: true),
        items: const [
          DropdownMenuItem(value: 'moisture', child: Text('Humidité')),
          DropdownMenuItem(value: 'health', child: Text('Santé')),
        ],
        onChanged: (v) { if (v != null) { setState(() => _metric = v); _load(); } },
      )),
    ]);
  }

  Widget _choroplethGrid(List<dynamic> cells) {
    return Wrap(
      spacing: 8,
      runSpacing: 8,
      children: cells.map((c) {
        final m = c as Map<String, dynamic>;
        final color = ModernCharts.colorFromHex(m['color']?.toString());
        return Container(
          width: 100,
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: color.withValues(alpha: 0.3),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: color),
          ),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(m['name']?.toString() ?? '', style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold), overflow: TextOverflow.ellipsis),
            Text('${m['value']}%', style: TextStyle(fontSize: 13, color: color)),
          ]),
        );
      }).toList(),
    );
  }

  Widget _timeline(List<dynamic> items) {
    if (items.isEmpty) return const Padding(padding: EdgeInsets.all(16), child: Text('Aucun événement'));
    return Column(
      children: items.take(15).map((item) {
        final m = item as Map<String, dynamic>;
        return Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Column(children: [
            Container(width: 10, height: 10, decoration: const BoxDecoration(color: AppTheme.primaryGreen, shape: BoxShape.circle)),
            Container(width: 2, height: 32, color: Colors.grey.shade300),
          ]),
          const SizedBox(width: 12),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(m['title']?.toString() ?? '', style: const TextStyle(fontWeight: FontWeight.w500)),
            Text(m['date']?.toString() ?? '', style: TextStyle(fontSize: 11, color: Colors.grey.shade600)),
          ])),
        ]);
      }).toList(),
    );
  }
}
