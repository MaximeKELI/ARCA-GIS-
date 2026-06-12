import 'dart:typed_data';

/// Extrait la position GPS depuis les métadonnées EXIF d'une photo.
class ExifService {
  /// Retourne {lat, lng} ou null si non trouvé.
  /// Parsing simplifié — en production utiliser package `exif`.
  static Map<String, double>? extractGps(Uint8List bytes) {
    try {
      final text = String.fromCharCodes(bytes.take(4096));
      final latMatch = RegExp(r'GPSLatitude["\s:]*([0-9.]+)').firstMatch(text);
      final lngMatch = RegExp(r'GPSLongitude["\s:]*([0-9.]+)').firstMatch(text);
      if (latMatch != null && lngMatch != null) {
        return {
          'lat': double.parse(latMatch.group(1)!),
          'lng': double.parse(lngMatch.group(1)!),
        };
      }
    } catch (_) {}
    return null;
  }
}
