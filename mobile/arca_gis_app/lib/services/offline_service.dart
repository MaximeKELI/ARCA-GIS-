import 'dart:convert';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';

class OfflineService {
  static const _cacheParcels = 'cache_parcels';
  static const _cacheAlerts = 'cache_alerts';
  static const _cacheClimate = 'cache_climate';
  static const _pendingSOS = 'pending_sos';

  Future<bool> get isOnline async {
    final result = await Connectivity().checkConnectivity();
    return !result.contains(ConnectivityResult.none);
  }

  Future<void> cacheParcels(List<dynamic> data) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_cacheParcels, jsonEncode(data));
  }

  Future<List<dynamic>> getCachedParcels() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_cacheParcels);
    if (raw == null) return [];
    return jsonDecode(raw) as List<dynamic>;
  }

  Future<void> cacheAlerts(List<dynamic> data) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_cacheAlerts, jsonEncode(data));
  }

  Future<List<dynamic>> getCachedAlerts() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_cacheAlerts);
    if (raw == null) return [];
    return jsonDecode(raw) as List<dynamic>;
  }

  Future<void> cacheClimate(List<dynamic> data) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_cacheClimate, jsonEncode(data));
  }

  Future<List<dynamic>> getCachedClimate() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_cacheClimate);
    if (raw == null) return [];
    return jsonDecode(raw) as List<dynamic>;
  }

  Future<void> queueSOS(Map<String, dynamic> payload) async {
    final prefs = await SharedPreferences.getInstance();
    final pending = await getPendingSOS();
    pending.add(payload);
    await prefs.setString(_pendingSOS, jsonEncode(pending));
  }

  Future<List<Map<String, dynamic>>> getPendingSOS() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_pendingSOS);
    if (raw == null) return [];
    return (jsonDecode(raw) as List).cast<Map<String, dynamic>>();
  }

  Future<void> clearPendingSOS() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_pendingSOS);
  }
}
