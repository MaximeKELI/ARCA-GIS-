import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../models/alert.dart';

class AlertBanner extends StatelessWidget {
  final AlertModel alert;
  final VoidCallback? onDismiss;

  const AlertBanner({super.key, required this.alert, this.onDismiss});

  Color get _severityColor {
    switch (alert.severity) {
      case 'critical':
        return AppTheme.sosRed;
      case 'high':
        return AppTheme.accentOrange;
      case 'medium':
        return AppTheme.climateBlue;
      default:
        return AppTheme.primaryGreen;
    }
  }

  IconData get _icon {
    switch (alert.alertType) {
      case 'sos':
        return Icons.sos;
      case 'climate':
        return Icons.cloud;
      case 'crop':
        return Icons.eco;
      default:
        return Icons.notifications;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      decoration: BoxDecoration(
        color: _severityColor.withValues(alpha: 0.1),
        border: Border(left: BorderSide(color: _severityColor, width: 4)),
        borderRadius: BorderRadius.circular(8),
      ),
      child: ListTile(
        leading: Icon(_icon, color: _severityColor),
        title: Text(alert.title, style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(alert.message, maxLines: 2, overflow: TextOverflow.ellipsis),
        trailing: onDismiss != null
            ? IconButton(icon: const Icon(Icons.close, size: 18), onPressed: onDismiss)
            : null,
        dense: true,
      ),
    );
  }
}
