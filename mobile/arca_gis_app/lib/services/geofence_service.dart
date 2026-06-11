import 'api_service.dart';

class GeofenceService {
  final ApiService _api = ApiService();

  Future<List<Map<String, dynamic>>> checkPosition(double lat, double lng) async {
    final result = await _api.post('/core/geofences/check/', {'lat': lat, 'lng': lng});
    return (result['zones'] as List?)?.cast<Map<String, dynamic>>() ?? [];
  }

  Future<List<Map<String, dynamic>>> getGeofences() async {
    final result = await _api.get('/core/geofences/');
    final items = result['results'] ?? result;
    if (items is List) return items.cast<Map<String, dynamic>>();
    return [];
  }
}
