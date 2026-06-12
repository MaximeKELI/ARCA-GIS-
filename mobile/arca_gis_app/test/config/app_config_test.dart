import 'package:flutter_test/flutter_test.dart';
import 'package:arca_gis_app/config/app_config.dart';

void main() {
  group('AppConfig', () {
    test('apiBaseUrl est une URL API valide', () {
      expect(AppConfig.apiBaseUrl, startsWith('http://'));
      expect(AppConfig.apiBaseUrl, endsWith('/api'));
      expect(AppConfig.apiHost, contains('8003'));
    });

    test('urls websocket dérivées du host API', () {
      expect(AppConfig.wsAlertsUrl, '${AppConfig.wsHost}/ws/alerts/');
      expect(AppConfig.wsChatUrl(42), '${AppConfig.wsHost}/ws/chat/42/');
    });

    test('version applicative définie', () {
      expect(AppConfig.appVersion, isNotEmpty);
    });
  });
}
