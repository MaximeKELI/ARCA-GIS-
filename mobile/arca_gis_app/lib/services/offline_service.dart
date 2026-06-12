import 'dart:convert';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'offline_db.dart';

class OfflineService {
  final _db = OfflineDB();
  static const _cacheParcels = 'cache_parcels';
  static const _cacheAlerts = 'cache_alerts';
  static const _cacheClimate = 'cache_climate';

  Future<bool> get isOnline async {
    final result = await Connectivity().checkConnectivity();
    return !result.contains(ConnectivityResult.none);
  }

  Future<void> cacheParcels(List<dynamic> data) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_cacheParcels, jsonEncode(data));
    await _db.saveParcels(data.cast<Map<String, dynamic>>());
  }

  Future<List<dynamic>> getCachedParcels() async {
    final cached = await _db.loadParcels();
    if (cached.isNotEmpty) return cached;
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
    await _db.queueAction('sos', payload);
  }

  Future<List<Map<String, dynamic>>> getPendingSOS() async => _db.pendingSOS();

  Future<void> clearPendingSOS() async => _db.clearPending();
}
