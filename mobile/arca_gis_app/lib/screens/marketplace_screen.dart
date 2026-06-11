import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class MarketplaceScreen extends StatefulWidget {
  const MarketplaceScreen({super.key});
  @override
  State<MarketplaceScreen> createState() => _MarketplaceScreenState();
}

class _MarketplaceScreenState extends State<MarketplaceScreen> {
  final ApiService _api = ApiService();
  List<dynamic> _prices = [];

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    final data = await _api.get('/marketplace/prices/');
    setState(() => _prices = data['results'] ?? data ?? []);
  }

  IconData _trendIcon(String trend) {
    switch (trend) {
      case 'up': return Icons.trending_up;
      case 'down': return Icons.trending_down;
      default: return Icons.trending_flat;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Prix des marchés')),
      body: RefreshIndicator(
        onRefresh: _load,
        child: ListView.builder(
          itemCount: _prices.length,
          itemBuilder: (_, i) {
            final p = _prices[i];
            return Card(
              margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              child: ListTile(
                leading: Icon(_trendIcon(p['trend'] ?? 'stable'), color: AppTheme.accentOrange),
                title: Text('${p['crop_name']} — ${p['market_name']}'),
                subtitle: Text(p['region'] ?? p['country'] ?? ''),
                trailing: Text('${p['price_per_kg']} F/kg',
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              ),
            );
          },
        ),
      ),
    );
  }
}
