import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../models/parcel.dart';

class ParcelCard extends StatelessWidget {
  final Parcel parcel;
  final VoidCallback? onTap;

  const ParcelCard({super.key, required this.parcel, this.onTap});

  Color get _healthColor {
    switch (parcel.healthStatus) {
      case 'excellent':
        return AppTheme.primaryGreen;
      case 'good':
        return Colors.lightGreen;
      case 'moderate':
        return AppTheme.accentOrange;
      case 'poor':
        return Colors.deepOrange;
      case 'critical':
        return AppTheme.sosRed;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  color: _healthColor.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Icon(Icons.grass, color: _healthColor),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(parcel.name, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 15)),
                    Text(parcel.cropTypeDisplay, style: TextStyle(color: Colors.grey[600], fontSize: 13)),
                  ],
                ),
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text('${parcel.areaHectares.toStringAsFixed(1)} ha',
                      style: const TextStyle(fontWeight: FontWeight.w500)),
                  Text('💧 ${parcel.soilMoisture.toStringAsFixed(0)}%',
                      style: TextStyle(color: Colors.grey[600], fontSize: 12)),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
