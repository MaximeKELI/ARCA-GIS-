import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';

/// Fournisseur de tuiles : cache local si disponible, sinon réseau.
class OfflineTileProvider extends TileProvider {
  final String? cacheDir;

  OfflineTileProvider({this.cacheDir});

  @override
  ImageProvider getImage(TileCoordinates coordinates, TileLayer options) {
    if (cacheDir != null) {
      final path = '$cacheDir/${coordinates.z}/${coordinates.x}/${coordinates.y}.png';
      if (File(path).existsSync()) return FileImage(File(path));
    }
    return NetworkTileProvider().getImage(coordinates, options);
  }
}
