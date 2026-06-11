import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../config/theme.dart';
import '../providers/map_provider.dart';
import '../services/api_service.dart';

class ForecastScreen extends StatefulWidget {
  const ForecastScreen({super.key});

  @override
  State<ForecastScreen> createState() => _ForecastScreenState();
}

class _ForecastScreenState extends State<ForecastScreen> {
  final ApiService _api = ApiService();
  List<dynamic> _forecast = [];
  Map<String, dynamic>? _current;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final pos = context.read<MapProvider>().userPosition;
    if (pos == null) { setState(() => _loading = false); return; }

    try {
      final current = await _api.get('/climate/weather/current/?lat=${pos.latitude}&lng=${pos.longitude}');
      final forecast = await _api.get('/climate/weather/forecast/?lat=${pos.latitude}&lng=${pos.longitude}&days=7');
      setState(() {
        _current = current;
        _forecast = forecast['forecast'] ?? [];
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Prévisions météo')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _load,
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  if (_current != null) Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('Météo actuelle', style: Theme.of(context).textTheme.titleMedium),
                          const SizedBox(height: 8),
                          Text('🌡️ ${_current!['temperature']}°C'),
                          Text('🌧️ ${_current!['rainfall_mm']} mm'),
                          Text('💧 ${_current!['humidity']}%'),
                          if (_current!['description'] != null)
                            Text('${_current!['description']}'),
                          Text('Source: ${_current!['source']}', style: const TextStyle(fontSize: 12, color: Colors.grey)),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text('Prévisions 7 jours', style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 8),
                  ..._forecast.map((day) => Card(
                    margin: const EdgeInsets.only(bottom: 8),
                    child: ListTile(
                      leading: Icon(Icons.calendar_today, color: AppTheme.climateBlue),
                      title: Text(day['datetime']?.toString().split(' ').first ?? ''),
                      subtitle: Text('${day['temperature']}°C — ${day['rainfall_mm']}mm — ${day['humidity']}%'),
                    ),
                  )),
                ],
              ),
            ),
    );
  }
}
