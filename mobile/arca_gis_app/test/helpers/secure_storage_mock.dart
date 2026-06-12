import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

/// Simule flutter_secure_storage pour les tests unitaires.
void mockSecureStorage() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final store = <String, String>{};

  const channel = MethodChannel('plugins.it_nomads.com/flutter_secure_storage');
  channel.setMockMethodCallHandler((call) async {
    switch (call.method) {
      case 'read':
        return store[call.arguments['key'] as String];
      case 'write':
        store[call.arguments['key'] as String] = call.arguments['value'] as String;
        return null;
      case 'delete':
        store.remove(call.arguments['key'] as String);
        return null;
      case 'deleteAll':
        store.clear();
        return null;
      default:
        return null;
    }
  });
}
