import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../config/theme.dart';
import '../providers/map_provider.dart';
import '../widgets/alert_banner.dart';

class AlertsScreen extends StatelessWidget {
  const AlertsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final mapProvider = context.watch<MapProvider>();
    final alerts = mapProvider.alerts;
    final climateEvents = mapProvider.climateEvents;

    return Scaffold(
      appBar: AppBar(title: const Text('Alertes')),
      body: RefreshIndicator(
        onRefresh: () => mapProvider.loadAllData(),
        child: ListView(
          children: [
            if (alerts.isEmpty && climateEvents.isEmpty)
              const Padding(
                padding: EdgeInsets.all(48),
                child: Column(
                  children: [
                    Icon(Icons.notifications_off, size: 64, color: Colors.grey),
                    SizedBox(height: 16),
                    Text('Aucune alerte active', style: TextStyle(color: Colors.grey)),
                  ],
                ),
              ),
            if (alerts.isNotEmpty) ...[
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
                child: Text('Notifications', style: Theme.of(context).textTheme.titleMedium),
              ),
              ...alerts.map((a) => AlertBanner(alert: a)),
            ],
            if (climateEvents.isNotEmpty) ...[
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 24, 16, 8),
                child: Text('Événements climatiques', style: Theme.of(context).textTheme.titleMedium),
              ),
              ...climateEvents.map((e) => Card(
                    margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                    child: ListTile(
                      leading: Icon(_eventIcon(e.eventType), color: _severityColor(e.severity)),
                      title: Text(e.title, style: const TextStyle(fontWeight: FontWeight.w600)),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(e.description, maxLines: 2, overflow: TextOverflow.ellipsis),
                          if (e.aiRecommendation != null)
                            Padding(
                              padding: const EdgeInsets.only(top: 4),
                              child: Text('💡 ${e.aiRecommendation}',
                                  style: TextStyle(color: AppTheme.primaryGreen, fontSize: 12)),
                            ),
                        ],
                      ),
                      isThreeLine: true,
                    ),
                  )),
            ],
          ],
        ),
      ),
    );
  }

  IconData _eventIcon(String type) {
    switch (type) {
      case 'drought':
        return Icons.wb_sunny;
      case 'flood':
        return Icons.water_drop;
      case 'heatwave':
        return Icons.thermostat;
      default:
        return Icons.cloud;
    }
  }

  Color _severityColor(String severity) {
    switch (severity) {
      case 'critical':
      case 'high':
        return AppTheme.sosRed;
      case 'medium':
        return AppTheme.accentOrange;
      default:
        return AppTheme.climateBlue;
    }
  }
}
