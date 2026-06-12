import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../config/theme.dart';
import '../providers/map_provider.dart';
import '../widgets/parcel_card.dart';
import 'parcel_qr_screen.dart';
import 'parcel_compare_screen.dart';

class ParcelsScreen extends StatelessWidget {
  const ParcelsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final mapProvider = context.watch<MapProvider>();
    final parcels = mapProvider.parcels;

    return Scaffold(
      appBar: AppBar(title: const Text('Mes Parcelles')),
      body: RefreshIndicator(
        onRefresh: () => mapProvider.loadAllData(),
        child: parcels.isEmpty
            ? ListView(
                children: const [
                  SizedBox(height: 100),
                  Icon(Icons.agriculture, size: 64, color: Colors.grey, textDirection: TextDirection.ltr),
                  SizedBox(height: 16),
                  Center(child: Text('Aucune parcelle enregistrée', style: TextStyle(color: Colors.grey))),
                ],
              )
            : ListView.builder(
                itemCount: parcels.length,
                itemBuilder: (context, index) {
                  final parcel = parcels[index];
                  return ParcelCard(
                    parcel: parcel,
                    onTap: () => _showParcelDetail(context, parcel),
                  );
                },
              ),
      ),
    );
  }

  void _showParcelDetail(BuildContext context, parcel) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(parcel.name, style: Theme.of(ctx).textTheme.titleLarge),
            const SizedBox(height: 8),
            Text('Culture: ${parcel.cropTypeDisplay}'),
            Text('Surface: ${parcel.areaHectares.toStringAsFixed(2)} hectares'),
            Text('Santé: ${parcel.healthStatusDisplay}'),
            Text('Humidité sol: ${parcel.soilMoisture.toStringAsFixed(0)}%'),
            const SizedBox(height: 16),
            Row(children: [
              Expanded(child: OutlinedButton.icon(
                onPressed: () { Navigator.pop(ctx); Navigator.push(context, MaterialPageRoute(
                  builder: (_) => ParcelQrScreen(parcelId: parcel.id))); },
                icon: const Icon(Icons.qr_code), label: const Text('QR'),
              )),
              const SizedBox(width: 8),
              Expanded(child: OutlinedButton.icon(
                onPressed: () {
                  Navigator.pop(ctx);
                  final others = context.read<MapProvider>().parcels.where((p) => p.id != parcel.id).take(1);
                  if (others.isEmpty) return;
                  Navigator.push(context, MaterialPageRoute(builder: (_) => ParcelCompareScreen(
                    parcelIds: [parcel.id, others.first.id])));
                },
                icon: const Icon(Icons.compare), label: const Text('Comparer'),
              )),
            ]),
            const SizedBox(height: 8),
            ElevatedButton.icon(
              onPressed: () {
                Navigator.pop(ctx);
                context.read<MapProvider>().requestAIAnalysis(cropType: parcel.cropType);
              },
              icon: const Icon(Icons.psychology),
              label: const Text('Analyse IA'),
              style: ElevatedButton.styleFrom(backgroundColor: AppTheme.climateBlue),
            ),
          ],
        ),
      ),
    );
  }
}
