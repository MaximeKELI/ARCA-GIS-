import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import '../config/app_config.dart';
import '../models/user.dart';

class AuthService {
  static const _storage = FlutterSecureStorage();
  static const _accessKey = 'access_token';
  static const _refreshKey = 'refresh_token';

  Future<String?> getAccessToken() => _storage.read(key: _accessKey);

  Future<bool> isLoggedIn() async {
    final token = await getAccessToken();
    return token != null && token.isNotEmpty;
  }

  Future<User> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('${AppConfig.apiBaseUrl}/auth/token/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );

    if (response.statusCode != 200) {
      throw Exception('Identifiants incorrects');
    }

    final data = jsonDecode(response.body);
    await _storage.write(key: _accessKey, value: data['access']);
    await _storage.write(key: _refreshKey, value: data['refresh']);

    return getProfile();
  }

  Future<User> register({
    required String username,
    required String email,
    required String password,
    required String firstName,
    required String lastName,
    String role = 'farmer',
    String country = "Côte d'Ivoire",
  }) async {
    final response = await http.post(
      Uri.parse('${AppConfig.apiBaseUrl}/users/register/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'email': email,
        'password': password,
        'password_confirm': password,
        'first_name': firstName,
        'last_name': lastName,
        'role': role,
        'country': country,
      }),
    );

    if (response.statusCode != 201) {
      final body = jsonDecode(response.body);
      throw Exception(body.toString());
    }

    return login(username, password);
  }

  Future<User> getProfile() async {
    final token = await getAccessToken();
    final response = await http.get(
      Uri.parse('${AppConfig.apiBaseUrl}/users/profile/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode != 200) {
      throw Exception('Session expirée');
    }

    return User.fromJson(jsonDecode(response.body));
  }

  Future<void> logout() async {
    await _storage.delete(key: _accessKey);
    await _storage.delete(key: _refreshKey);
  }
}
