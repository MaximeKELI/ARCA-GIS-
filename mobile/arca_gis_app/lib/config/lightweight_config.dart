/// Mode ultra-léger pour téléphones d'entrée de gamme.
class LightweightConfig {
  static const bool enabled = false;
  static const bool disableAnimations = true;
  static const bool lowResTiles = true;
  static const int maxCachedItems = 50;
  static const String tileUrl = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';
  static const double maxZoom = 16;
}
