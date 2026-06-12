import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:arca_gis_app/config/app_config.dart';
import 'package:arca_gis_app/services/auth_service.dart';

import '../helpers/secure_storage_mock.dart';

void main() {
  setUp(mockSecureStorage);

  group('AuthService.register', () {
    test('inscription puis connexion automatique', () async {
      final client = MockClient((request) async {
        if (request.url.path.endsWith('/users/register/')) {
          expect(request.method, 'POST');
          final body = jsonDecode(request.body) as Map<String, dynamic>;
          expect(body['password_confirm'], body['password']);
          return http.Response(
            jsonEncode({
              'username': body['username'],
              'email': body['email'],
              'first_name': body['first_name'],
              'last_name': body['last_name'],
              'role': body['role'],
            }),
            201,
          );
        }
        if (request.url.path.endsWith('/auth/token/')) {
          return http.Response(
            jsonEncode({'access': 'tok_access', 'refresh': 'tok_refresh'}),
            200,
          );
        }
        if (request.url.path.endsWith('/users/profile/')) {
          return http.Response(
            jsonEncode({
              'id': 9,
              'username': 'newbie',
              'email': 'n@t.com',
              'first_name': 'N',
              'last_name': 'U',
              'role': 'farmer',
              'role_display': 'Agriculteur',
            }),
            200,
          );
        }
        return http.Response('not found', 404);
      });

      final auth = AuthService(client: client);
      final user = await auth.register(
        username: 'newbie',
        email: 'n@t.com',
        password: 'testpass123',
        firstName: 'N',
        lastName: 'U',
      );

      expect(user.username, 'newbie');
      expect(await auth.getAccessToken(), 'tok_access');
    });

    test('erreur API lisible si inscription refusée', () async {
      final client = MockClient((request) async {
        return http.Response(
          jsonEncode({'username': ['Un utilisateur avec ce nom existe déjà.']}),
          400,
        );
      });

      final auth = AuthService(client: client);
      expect(
        () => auth.register(
          username: 'doublon',
          email: 'd@t.com',
          password: 'testpass123',
          firstName: 'D',
          lastName: 'U',
        ),
        throwsA(
          predicate<Exception>(
            (e) => e.toString().contains('Utilisateur'),
          ),
        ),
      );
    });

    test('erreur connexion si serveur inaccessible', () async {
      final client = MockClient((_) async => throw http.ClientException('failed'));

      final auth = AuthService(client: client);
      expect(
        () => auth.login('x', 'y'),
        throwsA(
          predicate<Exception>(
            (e) => e.toString().contains(AppConfig.apiHost),
          ),
        ),
      );
    });
  });
}
