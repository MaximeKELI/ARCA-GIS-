import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class AnalyticsScreen extends StatefulWidget {
  const AnalyticsScreen({super.key});

  @override
  State<AnalyticsScreen> createState() => _AnalyticsScreenState();
}

class _AnalyticsScreenState extends State<AnalyticsScreen> {
  final ApiService _api = ApiService();
  Map<String, dynamic>? _stats;
  List<dynamic> _history = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final stats = await _api.get('/analytics/dashboard/');
      final history = await _api.get('/analytics/crop-history/');
      setState(() {
        _stats = stats;
        _history = history['results'] ?? history ?? [];
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Analytiques')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _load,
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  if (_stats != null) ...[
                    _buildStatRow('Parcelles', '${_stats!['parcels']['total']}'),
                    _buildStatRow('SOS actifs', '${_stats!['incidents']['active_sos']}',
                        color: AppTheme.sosRed),
                    _buildStatRow('Événements climat', '${_stats!['climate']['active_events']}'),
                    _buildStatRow('Humidité moy.', 
                        '${(_stats!['parcels']['avg_moisture'] ?? 0).toStringAsFixed(0)}%'),
                    const SizedBox(height: 24),
                  ],
                  if (_history.isNotEmpty) ...[
                    Text('Historique cultures', style: Theme.of(context).textTheme.titleMedium),
                    const SizedBox(height: 12),
                    SizedBox(
                      height: 200,
                      child: LineChart(
                        LineChartData(
                          gridData: const FlGridData(show: true),
                          titlesData: const FlTitlesData(show: true),
                          borderData: FlBorderData(show: true),
                          lineBarsData: [
                            LineChartBarData(
                              spots: _history.asMap().entries.map((e) {
                                return FlSpot(
                                  e.key.toDouble(),
                                  (e.value['soil_moisture'] ?? 0).toDouble(),
                                );
                              }).toList(),
                              isCurved: true,
                              color: AppTheme.primaryGreen,
                              barWidth: 3,
                              dotData: const FlDotData(show: false),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    SizedBox(
                      height: 200,
                      child: LineChart(
                        LineChartData(
                          gridData: const FlGridData(show: true),
                          titlesData: const FlTitlesData(show: true),
                          borderData: FlBorderData(show: true),
                          lineBarsData: [
                            LineChartBarData(
                              spots: _history.asMap().entries.map((e) {
                                return FlSpot(
                                  e.key.toDouble(),
                                  (e.value['ndvi_score'] ?? e.value['soil_moisture'] ?? 0).toDouble() / 100,
                                );
                              }).toList(),
                              isCurved: true,
                              color: AppTheme.climateBlue,
                              barWidth: 3,
                              dotData: const FlDotData(show: false),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ],
              ),
            ),
    );
  }

  Widget _buildStatRow(String label, String value, {Color? color}) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        title: Text(label),
        trailing: Text(value, style: TextStyle(
          fontSize: 20, fontWeight: FontWeight.bold, color: color ?? AppTheme.primaryGreen,
        )),
      ),
    );
  }
}
