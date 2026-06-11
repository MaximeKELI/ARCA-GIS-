class AppConfig {
  static const String appName = 'ARCA-GIS';
  static const String appSubtitle = 'Agro-Rescue Climate Africa';

  // Android emulator: 10.0.2.2 maps to host localhost
  static const String apiBaseUrl = 'http://10.0.2.2:8002/api';
  static const String wsBaseUrl = 'ws://10.0.2.2:8002/ws/alerts/';

  // For iOS simulator or physical device, use your machine IP:
  // static const String apiBaseUrl = 'http://192.168.1.X:8000/api';
  // static const String wsBaseUrl = 'ws://192.168.1.X:8000/ws/alerts/';

  static const double defaultLat = 7.6900;
  static const double defaultLng = -5.0300;
  static const double defaultZoom = 12.0;
}
