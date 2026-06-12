import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:http/http.dart' as http;

/// Télécharge et met en cache les tuiles cartographiques pour usage hors-ligne.
class OfflineTileService {
  static const _tileBase = 'https://tile.openstreetmap.org';
  String? _cacheDirPath;

  Future<String> get cacheDir async {
    if (_cacheDirPath != null) return _cacheDirPath!;
    final dir = await getApplicationDocumentsDirectory();
    final tiles = Directory('${dir.path}/tiles');
    if (!await tiles.exists()) await tiles.create(recursive: true);
    _cacheDirPath = tiles.path;
    return _cacheDirPath!;
  }

  Future<void> downloadRegion({required int zoom, required int xMin, required int xMax,
      required int yMin, required int yMax}) async {
    final base = await cacheDir;
    for (var x = xMin; x <= xMax; x++) {
      for (var y = yMin; y <= yMax; y++) {
        final path = '$base/$zoom/$x/$y.png';
        final file = File(path);
        if (await file.exists()) continue;
        await file.parent.create(recursive: true);
        try {
          final resp = await http.get(Uri.parse('$_tileBase/$zoom/$x/$y.png'));
          if (resp.statusCode == 200) await file.writeAsBytes(resp.bodyBytes);
        } catch (_) {}
      }
    }
  }

  String? localTilePath(int z, int x, int y) {
    if (_cacheDirPath == null) return null;
    final path = '$_cacheDirPath/$z/$x/$y.png';
    return File(path).existsSync() ? path : null;
  }

  String? get cacheDirPath => _cacheDirPath;

  Future<void> init() async {
    await cacheDir;
  }
}
