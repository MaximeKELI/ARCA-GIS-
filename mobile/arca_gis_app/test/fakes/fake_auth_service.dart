import 'package:arca_gis_app/models/user.dart';
import 'package:arca_gis_app/services/auth_service.dart';

class FakeAuthService extends AuthService {
  FakeAuthService({
    this.onRegister,
    this.onLogin,
    this.registerError,
  });

  final Future<User> Function()? onRegister;
  final Future<User> Function()? onLogin;
  final Object? registerError;

  int registerCallCount = 0;
  String? lastUsername;
  String? lastPassword;

  @override
  Future<User> register({
    required String username,
    required String email,
    required String password,
    required String firstName,
    required String lastName,
    String role = 'farmer',
    String country = "Côte d'Ivoire",
  }) async {
    registerCallCount++;
    lastUsername = username;
    lastPassword = password;
    if (registerError != null) throw registerError!;
    if (onRegister != null) return onRegister!();
    return User(
      id: 1,
      username: username,
      email: email,
      firstName: firstName,
      lastName: lastName,
      role: role,
      roleDisplay: role,
    );
  }

  @override
  Future<User> login(String username, String password) async {
    if (onLogin != null) return onLogin!();
    return User(
      id: 1,
      username: username,
      email: 't@t.com',
      firstName: 'T',
      lastName: 'U',
      role: 'farmer',
      roleDisplay: 'Agriculteur',
    );
  }
}
