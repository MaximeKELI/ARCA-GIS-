class AppConfig {
  static const String appName = 'ARCA-GIS';
  static const String appSubtitle = 'Agro-Rescue Climate Africa';

  static const String apiBaseUrl = 'http://10.0.2.2:8003/api';
  static const String wsHost = 'ws://10.0.2.2:8003';
  static const String wsAlertsUrl = '$wsHost/ws/alerts/';
  static const String wsGpsUrl = '$wsHost/ws/gps/';
  static String wsChatUrl(int incidentId) => '$wsHost/ws/chat/$incidentId/';

  static const double defaultLat = 7.6900;
  static const double defaultLng = -5.0300;
  static const String appVersion = '7.7.0';
