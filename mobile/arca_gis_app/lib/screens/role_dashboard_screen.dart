import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';
import '../widgets/modern_charts.dart';

class RoleDashboardScreen extends StatefulWidget {
  const RoleDashboardScreen({super.key});
  @override
  State<RoleDashboardScreen> createState() => _RoleDashboardScreenState();
}

class _RoleDashboardScreenState extends State<RoleDashboardScreen> {
  final _api = ApiService();
  Map<String, dynamic> _role = {};
  Map<String, dynamic> _visual = {};

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    try {
      final role = await _api.get('/analytics/role-dashboard/');
      final visual = await _api.get('/analytics/visual/');
      setState(() {
        _role = parseApiMap(role);
        _visual = parseApiMap(visual);
      });
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    final role = _role['role']?.toString() ?? '—';
    final series = (_visual['series'] as Map<String, dynamic>?) ?? {};
    final radar = (_visual['radar'] as Map<String, dynamic>?) ?? {};
    return Scaffold(
      appBar: AppBar(title: Text('Dashboard ($role)'), backgroundColor: AppTheme.primaryGreen),
      body: RefreshIndicator(
        onRefresh: _load,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Wrap(spacing: 12, runSpacing: 12, children: _role.entries.where((e) => e.key != 'role').map((e) {
              return SizedBox(
                width: (MediaQuery.of(context).size.width - 44) / 2,
                child: ModernCharts.kpiCard(
                  label: e.key.replaceAll('_', ' '),
                  value: '${e.value}',
                  unit: '',
                  color: AppTheme.primaryGreen,
                  icon: Icons.analytics,
                ),
              );
            }).toList()),
            if (radar.isNotEmpty) ModernCharts.radarChart(
              title: 'Performance globale',
              labels: (radar['labels'] as List?)?.cast<String>() ?? [],
              values: (radar['values'] as List?)?.cast<num>().map((v) => v.toDouble()).toList() ?? [],
            ),
            ModernCharts.gradientLineChart(
              title: 'Humidité',
              data: (series['moisture_trend'] as List?)?.cast<Map<String, dynamic>>() ?? [],
              color: AppTheme.climateBlue,
              valueSuffix: '%',
            ),
          ],
        ),
      ),
    );
  }
}
