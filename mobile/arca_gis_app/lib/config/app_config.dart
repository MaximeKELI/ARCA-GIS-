import 'package:flutter/foundation.dart' show kIsWeb, defaultTargetPlatform, TargetPlatform;

class AppConfig {
  static const String appName = 'ARCA-GIS';
  static const String appSubtitle = 'Agro-Rescue Climate Africa';

  /// Surcharge possible : `flutter run --dart-define=API_HOST=192.168.1.10:8003`
  static const String _apiHostOverride = String.fromEnvironment('API_HOST');

  static String get apiHost {
    if (_apiHostOverride.isNotEmpty) return _apiHostOverride;
    if (kIsWeb) return 'localhost:8003';
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return '10.0.2.2:8003';
      default:
        // Linux, Windows, macOS, iOS simulateur
        return 'localhost:8003';
    }
  }

  static String get apiBaseUrl => 'http://$apiHost/api';
  static String get wsHost => 'ws://$apiHost';
  static String get wsAlertsUrl => '$wsHost/ws/alerts/';
  static String get wsGpsUrl => '$wsHost/ws/gps/';
  static String wsChatUrl(int incidentId) => '$wsHost/ws/chat/$incidentId/';

  static const double defaultLat = 7.6900;
  static const double defaultLng = -5.0300;
  static const double defaultZoom = 12.0;
  static const String appVersion = '7.7.0';
}
