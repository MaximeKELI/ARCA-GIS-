import 'package:flutter_test/flutter_test.dart';
import 'package:arca_gis_app/models/user.dart';
import 'package:arca_gis_app/providers/auth_provider.dart';

import '../fakes/fake_auth_service.dart';

User _sampleUser() => User(
      id: 1,
      username: 'test',
      email: 't@t.com',
      firstName: 'T',
      lastName: 'U',
      role: 'farmer',
      roleDisplay: 'Agriculteur',
    );

void main() {
  test('register met à jour user en cas de succès', () async {
    final provider = AuthProvider(
      authService: FakeAuthService(
        onRegister: () async => _sampleUser(),
        onLogin: () async => _sampleUser(),
      ),
    );

    final ok = await provider.register(
      username: 'test',
      email: 't@t.com',
      password: 'testpass123',
      firstName: 'T',
      lastName: 'U',
    );

    expect(ok, isTrue);
    expect(provider.isLoggedIn, isTrue);
    expect(provider.error, isNull);
  });

  test('register expose un message d erreur lisible', () async {
    final provider = AuthProvider(
      authService: FakeAuthService(registerError: Exception('Email invalide')),
    );

    final ok = await provider.register(
      username: 'bad',
      email: 'bad',
      password: 'testpass123',
      firstName: 'B',
      lastName: 'D',
    );

    expect(ok, isFalse);
    expect(provider.error, 'Email invalide');
  });
}
