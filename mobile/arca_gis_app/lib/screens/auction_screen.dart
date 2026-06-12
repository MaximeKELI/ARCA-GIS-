import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class AuctionScreen extends StatefulWidget {
  const AuctionScreen({super.key});

  @override
  State<AuctionScreen> createState() => _AuctionScreenState();
}

class _AuctionScreenState extends State<AuctionScreen> {
  final _api = ApiService();
  List<dynamic> _auctions = [];

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final data = await _api.get('/economy/auctions/');
      setState(() => _auctions = data is List ? data : []);
    } catch (_) {}
  }

  Future<void> _bid(int id, double amount) async {
    await _api.post('/economy/auctions/$id/bid/', {'amount': amount});
    _load();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Enchères live'), backgroundColor: AppTheme.primaryGreen),
      body: ListView.builder(
        itemCount: _auctions.length,
        itemBuilder: (_, i) {
          final a = _auctions[i] as Map<String, dynamic>;
          return Card(
            margin: const EdgeInsets.all(12),
            child: ListTile(
              title: Text('${a['crop_type']} — ${a['quantity_kg']} kg'),
              subtitle: Text('Départ: ${a['starting_price']} XOF · Enchère: ${a['current_bid'] ?? '—'}'),
              trailing: IconButton(
                icon: const Icon(Icons.gavel),
                onPressed: () => _bid(a['id'] as int, (a['current_bid'] as num? ?? a['starting_price'] as num) + 10),
              ),
            ),
          );
        },
      ),
    );
  }
}
