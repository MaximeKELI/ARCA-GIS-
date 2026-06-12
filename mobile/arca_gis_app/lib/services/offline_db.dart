import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

/// Stockage offline simplifié (SQLite-ready via shared_preferences).
class OfflineDB {
  static const _parcelsKey = 'offline_parcels';
  static const _pendingSosKey = 'pending_sos';
  static const _disasterModeKey = 'disaster_mode';

  Future<void> saveParcels(List<Map<String, dynamic>> parcels) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_parcelsKey, jsonEncode(parcels));
  }

  Future<List<Map<String, dynamic>>> loadParcels() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_parcelsKey);
    if (raw == null) return [];
    return (jsonDecode(raw) as List).cast<Map<String, dynamic>>();
  }

  Future<void> queueSOS(Map<String, dynamic> sos) async {
    final prefs = await SharedPreferences.getInstance();
    final list = prefs.getStringList(_pendingSosKey) ?? [];
    list.add(jsonEncode(sos));
    await prefs.setStringList(_pendingSosKey, list);
  }

  Future<List<Map<String, dynamic>>> pendingSOS() async {
    final prefs = await SharedPreferences.getInstance();
    return (prefs.getStringList(_pendingSosKey) ?? [])
        .map((s) => jsonDecode(s) as Map<String, dynamic>).toList();
  }

  Future<void> setDisasterMode(bool enabled) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_disasterModeKey, enabled);
  }

  Future<bool> isDisasterMode() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_disasterModeKey) ?? false;
  }
}
