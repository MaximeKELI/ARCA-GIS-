import 'package:flutter_test/flutter_test.dart';
import 'package:arca_gis_app/models/user.dart';
import 'package:arca_gis_app/providers/auth_provider.dart';
import 'package:arca_gis_app/services/auth_service.dart';

class _FakeAuthService extends AuthService {
  _FakeAuthService({required this.onRegister, required this.onLogin});

  final Future<User> Function() onRegister;
  final Future<User> Function() onLogin;

  @override
  Future<User> register({
    required String username,
    required String email,
    required String password,
    required String firstName,
    required String lastName,
    String role = 'farmer',
    String country = "Côte d'Ivoire",
  }) =>
      onRegister();

  @override
  Future<User> login(String username, String password) => onLogin();
}

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
      authService: _FakeAuthService(
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
      authService: _FakeAuthService(
        onRegister: () async => throw Exception('Email invalide'),
        onLogin: () async => _sampleUser(),
      ),
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
