import 'package:flutter/material.dart';
import '../config/lightweight_config.dart';
import '../config/theme.dart';
/// Interface simplifiée pour téléphones d'entrée de gamme (KaiOS / feature phone).
class FeaturePhoneScreen extends StatelessWidget {
  const FeaturePhoneScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text('ARCA-GIS Lite', style: TextStyle(fontSize: 16)),
        backgroundColor: AppTheme.primaryGreen,
        toolbarHeight: 40,
      ),
      body: ListView(
        children: [
          const Padding(
            padding: EdgeInsets.all(12),
            child: Text('Mode léger activé', style: TextStyle(fontSize: 12, color: Colors.grey)),
          ),
          _bigButton(context, Icons.warning, 'SOS Urgence', Colors.red, () {
            showDialog(context: context, builder: (_) => const AlertDialog(
              title: Text('SOS'), content: Text('Alerte envoyée aux secours.')));
          }),
          _bigButton(context, Icons.cloud, 'Météo', AppTheme.primaryGreen, () {}),
          _bigButton(context, Icons.grass, 'Mes parcelles', AppTheme.primaryGreen, () {}),
          _bigButton(context, Icons.phone, 'Appel vocal', AppTheme.accentOrange, () {}),
        ],
      ),
    );
  }

  Widget _bigButton(BuildContext ctx, IconData icon, String label, Color color, VoidCallback onTap) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      child: Material(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(8),
        child: InkWell(
          onTap: onTap,
          child: SizedBox(
            height: LightweightConfig.disableAnimations ? 56 : 64,
            child: Row(
              children: [
                const SizedBox(width: 16),
                Icon(icon, color: color, size: 28),
                const SizedBox(width: 16),
                Text(label, style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600, color: color)),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
