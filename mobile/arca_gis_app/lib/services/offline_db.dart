import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

/// Stockage offline SQLite avec migration depuis SharedPreferences.
class OfflineDB {
  static Database? _db;
  static const _legacyPendingKey = 'pending_sync';
  static const _legacySosKey = 'pending_sos';

  Future<Database> get database async {
    if (_db != null) return _db!;
    _db = await _initDb();
    await _migrateFromPrefs(_db!);
    return _db!;
  }

  Future<Database> _initDb() async {
    final path = join(await getDatabasesPath(), 'arca_gis_offline.db');
    return openDatabase(path, version: 1, onCreate: (db, version) async {
      await db.execute('''
        CREATE TABLE pending_sync (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          action_type TEXT NOT NULL,
          payload TEXT NOT NULL,
          queued_at TEXT NOT NULL
        )
      ''');
      await db.execute('''
        CREATE TABLE parcels_cache (
          id INTEGER PRIMARY KEY,
          data TEXT NOT NULL
        )
      ''');
    });
  }

  Future<void> _migrateFromPrefs(Database db) async {
    final prefs = await SharedPreferences.getInstance();
    final legacy = prefs.getStringList(_legacyPendingKey) ?? [];
    if (legacy.isEmpty) return;
    for (final raw in legacy) {
      final item = jsonDecode(raw) as Map<String, dynamic>;
      await db.insert('pending_sync', {
        'action_type': item['action_type'],
        'payload': jsonEncode(item['payload']),
        'queued_at': item['queued_at'] ?? DateTime.now().toIso8601String(),
      });
    }
    await prefs.remove(_legacyPendingKey);
    await prefs.remove(_legacySosKey);
  }

  Future<void> saveParcels(List<Map<String, dynamic>> parcels) async {
    final db = await database;
    await db.delete('parcels_cache');
    for (final p in parcels) {
      await db.insert('parcels_cache', {'id': p['id'], 'data': jsonEncode(p)});
    }
  }

  Future<List<Map<String, dynamic>>> loadParcels() async {
    final db = await database;
    final rows = await db.query('parcels_cache');
    return rows.map((r) => jsonDecode(r['data'] as String) as Map<String, dynamic>).toList();
  }

  Future<void> queueSOS(Map<String, dynamic> sos) async => queueAction('sos', sos);

  Future<void> queueAction(String actionType, Map<String, dynamic> payload) async {
    final db = await database;
    await db.insert('pending_sync', {
      'action_type': actionType,
      'payload': jsonEncode(payload),
      'queued_at': DateTime.now().toIso8601String(),
    });
  }

  Future<List<Map<String, dynamic>>> pendingActions() async {
    final db = await database;
    final rows = await db.query('pending_sync', orderBy: 'id ASC');
    return rows.map((r) => {
      'action_type': r['action_type'],
      'payload': jsonDecode(r['payload'] as String) as Map<String, dynamic>,
      'queued_at': r['queued_at'],
    }).toList();
  }

  Future<List<Map<String, dynamic>>> pendingSOS() async {
    final all = await pendingActions();
    return all.where((a) => a['action_type'] == 'sos').map((a) => a['payload'] as Map<String, dynamic>).toList();
  }

  Future<void> clearPending() async {
    final db = await database;
    await db.delete('pending_sync');
  }

  Future<void> setDisasterMode(bool enabled) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('disaster_mode', enabled);
  }

  Future<bool> isDisasterMode() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool('disaster_mode') ?? false;
  }
}
