import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

class CulturalCalendarScreen extends StatefulWidget {
  const CulturalCalendarScreen({super.key});

  @override
  State<CulturalCalendarScreen> createState() => _CulturalCalendarScreenState();
}

class _CulturalCalendarScreenState extends State<CulturalCalendarScreen> {
  final _api = ApiService();
  List<dynamic> _calendars = [];
  List<dynamic> _current = [];
  bool _loading = true;

  static const _months = ['', 'Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'];

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final cal = await _api.get('/climate/calendar/');
      final cur = await _api.get('/climate/calendar/current/');
      setState(() {
        _calendars = parseApiList(cal);
        _current = parseApiList(cur['recommendations']);
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  int _monthFromMd(String md) {
    final parts = md.split('-');
    return int.tryParse(parts.first) ?? 1;
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return Scaffold(
      appBar: AppBar(title: const Text('Calendrier cultural'), backgroundColor: AppTheme.primaryGreen),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _load,
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  if (_current.isNotEmpty) ...[
                    Text('Cette saison', style: Theme.of(context).textTheme.titleMedium),
                    const SizedBox(height: 8),
                    ..._current.map((r) {
                      final m = r as Map<String, dynamic>;
                      return Card(
                        color: AppTheme.primaryGreen.withValues(alpha: isDark ? 0.2 : 0.08),
                        child: ListTile(
                          leading: const Icon(Icons.eco, color: AppTheme.primaryGreen),
                          title: Text(m['crop']?.toString() ?? ''),
                          subtitle: Text('${m['action']} · ${m['region']}'),
                        ),
                      );
                    }),
                    const SizedBox(height: 20),
                  ],
                  Text('Calendriers par culture', style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 12),
                  ..._calendars.map((c) => _cropTimeline(c as Map<String, dynamic>, isDark)),
                ],
              ),
            ),
    );
  }

  Widget _cropTimeline(Map<String, dynamic> cal, bool isDark) {
    final plantRange = (cal['planting']?.toString() ?? '').split(' → ');
    final harvestRange = (cal['harvest']?.toString() ?? '').split(' → ');
    final plantStart = plantRange.isNotEmpty ? _monthFromMd(plantRange.first) : 4;
    final plantEnd = plantRange.length > 1 ? _monthFromMd(plantRange.last) : 5;
    final harvestStart = harvestRange.isNotEmpty ? _monthFromMd(harvestRange.first) : 8;
    final harvestEnd = harvestRange.length > 1 ? _monthFromMd(harvestRange.last) : 9;

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF2A2A2A) : Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: isDark ? null : [BoxShadow(color: Colors.black.withValues(alpha: 0.06), blurRadius: 12)],
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Text(cal['crop_name']?.toString() ?? '', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const Spacer(),
          Chip(label: Text(cal['region']?.toString() ?? ''), backgroundColor: AppTheme.primaryGreen.withValues(alpha: 0.15)),
        ]),
        const SizedBox(height: 16),
        _monthBar(plantStart, plantEnd, AppTheme.primaryGreen, 'Semis'),
        const SizedBox(height: 8),
        _monthBar(harvestStart, harvestEnd, AppTheme.accentOrange, 'Récolte'),
        const SizedBox(height: 12),
        SizedBox(
          height: 24,
          child: Row(
            children: List.generate(12, (i) => Expanded(
              child: Center(child: Text(_months[i + 1], style: TextStyle(fontSize: 9, color: Colors.grey.shade600))),
            )),
          ),
        ),
        if ((cal['tips']?.toString() ?? '').isNotEmpty) ...[
          const Divider(),
          Text(cal['tips'].toString(), style: TextStyle(fontSize: 13, color: Colors.grey.shade600)),
        ],
        if ((cal['treatments'] as List?)?.isNotEmpty == true) ...[
          const SizedBox(height: 8),
          Wrap(spacing: 6, children: (cal['treatments'] as List).map((t) =>
            Chip(label: Text(t.toString(), style: const TextStyle(fontSize: 11)), visualDensity: VisualDensity.compact),
          ).toList()),
        ],
      ]),
    );
  }

  Widget _monthBar(int start, int end, Color color, String label) {
    return Row(children: [
      SizedBox(width: 48, child: Text(label, style: TextStyle(fontSize: 11, color: color, fontWeight: FontWeight.w600))),
      Expanded(
        child: SizedBox(
          height: 14,
          child: Row(
            children: List.generate(12, (i) {
              final month = i + 1;
              final active = start <= end
                  ? month >= start && month <= end
                  : month >= start || month <= end;
              return Expanded(
                child: Container(
                  margin: const EdgeInsets.symmetric(horizontal: 1),
                  decoration: BoxDecoration(
                    color: active ? color : color.withValues(alpha: 0.12),
                    borderRadius: BorderRadius.circular(3),
                  ),
                ),
              );
            }),
          ),
        ),
      ),
    ]);
  }
}
