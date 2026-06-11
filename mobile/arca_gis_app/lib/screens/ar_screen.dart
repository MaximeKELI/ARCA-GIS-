import 'package:flutter/material.dart';
import '../config/theme.dart';

class ARScreen extends StatelessWidget {
  const ARScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Réalité Augmentée')),
      body: Stack(
        children: [
          Container(color: Colors.black87, child: const Center(
            child: Icon(Icons.camera_alt, size: 120, color: Colors.white24),
          )),
          Positioned(
            top: 100, left: 40,
            child: _arOverlay(Icons.grass, 'Parcelle Maïs', 'Santé: Bon', AppTheme.primaryGreen),
          ),
          Positioned(
            top: 200, right: 30,
            child: _arOverlay(Icons.cloud, 'Alerte climat', 'Sécheresse modérée', AppTheme.accentOrange),
          ),
          Positioned(
            bottom: 120, left: 60,
            child: _arOverlay(Icons.water_drop, 'Humidité sol', '42%', AppTheme.climateBlue),
          ),
          Positioned(
            bottom: 40, left: 0, right: 0,
            child: Center(child: Text(
              'Mode AR — Pointez la caméra vers vos champs',
              style: TextStyle(color: Colors.white.withValues(alpha: 0.7)),
            )),
          ),
        ],
      ),
    );
  }

  Widget _arOverlay(IconData icon, String title, String subtitle, Color color) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.85),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: Colors.white, size: 20),
          const SizedBox(width: 8),
          Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12)),
            Text(subtitle, style: const TextStyle(color: Colors.white70, fontSize: 10)),
          ]),
        ],
      ),
    );
  }
}
