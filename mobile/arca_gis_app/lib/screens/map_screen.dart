import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:provider/provider.dart';
import '../config/app_config.dart';
import '../config/theme.dart';
import '../providers/map_provider.dart';
import 'chat_screen.dart';
import 'parcel_draw_screen.dart';
import '../services/offline_tile_provider.dart';
import 'measure_map_screen.dart';
import '../widgets/sos_button.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  final MapController _mapController = MapController();
  bool _sosLoading = false;

  @override
  Widget build(BuildContext context) {
    final mapProvider = context.watch<MapProvider>();
    final center = mapProvider.userPosition ??
        LatLng(AppConfig.defaultLat, AppConfig.defaultLng);

    return Scaffold(
      body: Stack(
        children: [
          FlutterMap(
            mapController: _mapController,
            options: MapOptions(
              initialCenter: center,
              initialZoom: AppConfig.defaultZoom,
              onPositionChanged: (pos, _) {},
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'africa.arca.arca_gis_app',
                tileProvider: OfflineTileProvider(cacheDir: mapProvider.offlineTileCacheDir),
              ),
              if (mapProvider.showHeatmap && mapProvider.heatmapCells.isNotEmpty)
                CircleLayer(
                  circles: mapProvider.heatmapCells.map((c) {
                    final intensity = (c['intensity'] as num?)?.toDouble() ?? 0.5;
                    final color = Color.lerp(Colors.red, AppTheme.primaryGreen, intensity)!;
                    return CircleMarker(
                      point: LatLng((c['lat'] as num).toDouble(), (c['lng'] as num).toDouble()),
                      radius: 500,
                      useRadiusInMeter: true,
                      color: color.withValues(alpha: 0.35),
                      borderColor: color,
                      borderStrokeWidth: 1.5,
                    );
                  }).toList(),
                ),
              if (mapProvider.parcels.isNotEmpty)
                PolygonLayer(
                  polygons: mapProvider.parcels
                      .where((p) => p.coordinates != null)
                      .map((p) => Polygon(
                            points: p.coordinates!
                                .map((c) => LatLng(c[1], c[0]))
                                .toList(),
                            color: _parcelColor(p.healthStatus).withValues(alpha: 0.3),
                            borderColor: _parcelColor(p.healthStatus),
                            borderStrokeWidth: 2,
                          ))
                      .toList(),
                ),
              MarkerLayer(
                markers: [
                  if (mapProvider.userPosition != null)
                    Marker(
                      point: mapProvider.userPosition!,
                      width: 40,
                      height: 40,
                      child: const Icon(Icons.my_location, color: AppTheme.climateBlue, size: 32),
                    ),
                  ...mapProvider.climateEvents
                      .where((e) => e.centerLat != null && e.centerLng != null)
                      .map((e) => Marker(
                            point: LatLng(e.centerLat!, e.centerLng!),
                            width: 36,
                            height: 36,
                            child: Tooltip(
                              message: e.title,
                              child: Icon(
                                _climateIcon(e.eventType),
                                color: _severityColor(e.severity),
                                size: 28,
                              ),
                            ),
                          )),
                  ...mapProvider.incidents.map((i) => Marker(
                        point: LatLng(i.lat, i.lng),
                        width: 44,
                        height: 44,
                        child: GestureDetector(
                          onTap: () => Navigator.push(context, MaterialPageRoute(
                            builder: (_) => ChatScreen(incidentId: i.id, incidentTitle: i.title),
                          )),
                          child: const Icon(Icons.emergency, color: AppTheme.sosRed, size: 36),
                        ),
                      )),
                  ...mapProvider.rescuePositions.map((r) => Marker(
                        point: LatLng(r.lat, r.lng),
                        width: 36,
                        height: 36,
                        child: const Icon(Icons.local_hospital, color: AppTheme.climateBlue, size: 28),
                      )),
                ],
              ),
            ],
          ),
          if (mapProvider.isLoading)
            const Center(child: CircularProgressIndicator()),
          Positioned(
            top: MediaQuery.of(context).padding.top + 8,
            left: 12,
            right: 12,
            child: _buildLegend(),
          ),
          Positioned(
            bottom: 100,
            right: 16,
            child: Column(
              children: [
                FloatingActionButton.small(
                  heroTag: 'locate',
                  onPressed: () {
                    if (mapProvider.userPosition != null) {
                      _mapController.move(mapProvider.userPosition!, 14);
                    }
                  },
                  backgroundColor: Colors.white,
                  foregroundColor: AppTheme.primaryGreen,
                  child: const Icon(Icons.gps_fixed),
                ),
                const SizedBox(height: 8),
                FloatingActionButton.small(
                  heroTag: 'heatmap',
                  onPressed: () => mapProvider.toggleHeatmap(),
                  backgroundColor: mapProvider.showHeatmap ? AppTheme.accentOrange : Colors.white,
                  foregroundColor: mapProvider.showHeatmap ? Colors.white : AppTheme.accentOrange,
                  child: const Icon(Icons.blur_on),
                ),
                const SizedBox(height: 8),
                FloatingActionButton.small(
                  heroTag: 'offline',
                  onPressed: () async {
                    await mapProvider.downloadOfflineTiles();
                    if (context.mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text(mapProvider.offlineTilesReady ? 'Tuiles offline téléchargées' : 'Position requise')),
                      );
                    }
                  },
                  backgroundColor: mapProvider.offlineTilesReady ? AppTheme.primaryGreen : Colors.white,
                  foregroundColor: mapProvider.offlineTilesReady ? Colors.white : AppTheme.primaryGreen,
                  child: const Icon(Icons.download),
                ),
                const SizedBox(height: 8),
                FloatingActionButton.small(
                  heroTag: 'measure',
                  onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const MeasureMapScreen())),
                  backgroundColor: Colors.white,
                  foregroundColor: AppTheme.primaryGreen,
                  child: const Icon(Icons.straighten),
                ),
                const SizedBox(height: 8),
                FloatingActionButton.small(
                  heroTag: 'refresh',
                  onPressed: () => mapProvider.loadAllData(),
                  backgroundColor: Colors.white,
                  foregroundColor: AppTheme.primaryGreen,
                  child: const Icon(Icons.refresh),
                ),
                const SizedBox(height: 8),
                FloatingActionButton.small(
                  heroTag: 'ai',
                  onPressed: () => _showAIAnalysis(context, mapProvider),
                  backgroundColor: AppTheme.climateBlue,
                  foregroundColor: Colors.white,
                  child: const Icon(Icons.psychology),
                ),
                const SizedBox(height: 8),
                FloatingActionButton.small(
                  heroTag: 'draw',
                  onPressed: () => Navigator.push(context, MaterialPageRoute(
                    builder: (_) => const ParcelDrawScreen(),
                  )).then((_) => mapProvider.loadAllData()),
                  backgroundColor: AppTheme.primaryGreen,
                  foregroundColor: Colors.white,
                  child: const Icon(Icons.draw),
                ),
              ],
            ),
          ),
        ],
      ),
      floatingActionButton: SOSButton(
        isLoading: _sosLoading,
        onPressed: () => _triggerSOS(mapProvider),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }

  Widget _buildLegend() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            _legendItem(Icons.grass, 'Parcelles', AppTheme.primaryGreen),
            _legendItem(Icons.cloud, 'Climat', AppTheme.climateBlue),
            _legendItem(Icons.emergency, 'SOS', AppTheme.sosRed),
          ],
        ),
      ),
    );
  }

  Widget _legendItem(IconData icon, String label, Color color) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, color: color, size: 16),
        const SizedBox(width: 4),
        Text(label, style: const TextStyle(fontSize: 11)),
      ],
    );
  }

  Future<void> _triggerSOS(MapProvider provider) async {
    setState(() => _sosLoading = true);
    final success = await provider.triggerSOS();
    setState(() => _sosLoading = false);
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(success ? '🚨 SOS envoyé ! Secours alertés.' : 'Échec: ${provider.error}'),
          backgroundColor: success ? AppTheme.sosRed : Colors.grey,
        ),
      );
    }
  }

  void _showAIAnalysis(BuildContext context, MapProvider provider) async {
    await provider.requestAIAnalysis();
    if (!context.mounted) return;
    final analysis = provider.aiAnalysis;
    if (analysis == null) return;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => DraggableScrollableSheet(
        expand: false,
        initialChildSize: 0.5,
        maxChildSize: 0.8,
        builder: (_, controller) => Padding(
          padding: const EdgeInsets.all(20),
          child: ListView(
            controller: controller,
            children: [
              Row(
                children: [
                  const Icon(Icons.psychology, color: AppTheme.climateBlue),
                  const SizedBox(width: 8),
                  Text('Analyse IA', style: Theme.of(ctx).textTheme.titleLarge),
                ],
              ),
              const SizedBox(height: 16),
              if (analysis['weather'] != null) ...[
                Text('Météo actuelle', style: Theme.of(ctx).textTheme.titleSmall),
                const SizedBox(height: 8),
                _weatherRow('🌡️', '${analysis['weather']['temperature']}°C'),
                _weatherRow('🌧️', '${analysis['weather']['rainfall_mm']} mm'),
                _weatherRow('💧', '${analysis['weather']['humidity']}% humidité'),
                const SizedBox(height: 16),
              ],
              Text('Santé culture: ${analysis['crop_health'] ?? 'N/A'}',
                  style: const TextStyle(fontWeight: FontWeight.w600)),
              const SizedBox(height: 12),
              Text('Recommandations', style: Theme.of(ctx).textTheme.titleSmall),
              const SizedBox(height: 8),
              ...(analysis['recommendations'] as List? ?? []).map(
                (r) => Padding(
                  padding: const EdgeInsets.only(bottom: 6),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('• '),
                      Expanded(child: Text(r.toString())),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _weatherRow(String emoji, String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 4),
      child: Text('$emoji  $text'),
    );
  }

  Color _parcelColor(String health) {
    switch (health) {
      case 'excellent':
      case 'good':
        return AppTheme.primaryGreen;
      case 'moderate':
        return AppTheme.accentOrange;
      default:
        return AppTheme.sosRed;
    }
  }

  IconData _climateIcon(String type) {
    switch (type) {
      case 'drought':
        return Icons.wb_sunny;
      case 'flood':
        return Icons.water;
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
