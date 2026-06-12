import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import '../config/app_config.dart';
import '../models/user.dart';

class AuthService {
  AuthService({http.Client? client, FlutterSecureStorage? storage})
      : _client = client ?? http.Client(),
        _storage = storage ?? const FlutterSecureStorage();

  final http.Client _client;
  final FlutterSecureStorage _storage;
  static const _accessKey = 'access_token';
  static const _refreshKey = 'refresh_token';

  Future<String?> getAccessToken() => _storage.read(key: _accessKey);

  Future<bool> isLoggedIn() async {
    final token = await getAccessToken();
    return token != null && token.isNotEmpty;
  }

  Future<User> login(String username, String password) async {
    try {
      final response = await _client.post(
        Uri.parse('${AppConfig.apiBaseUrl}/auth/token/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'username': username, 'password': password}),
      );

      if (response.statusCode != 200) {
        throw Exception(_parseApiError(response, fallback: 'Identifiants incorrects'));
      }

      final data = jsonDecode(response.body);
      await _storage.write(key: _accessKey, value: data['access']);
      await _storage.write(key: _refreshKey, value: data['refresh']);

      return getProfile();
    } on http.ClientException {
      throw Exception(_connectionError());
    }
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
    try {
      final response = await _client.post(
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
        throw Exception(_parseApiError(response, fallback: 'Inscription refusée'));
      }

      return login(username, password);
    } on http.ClientException {
      throw Exception(_connectionError());
    }
  }

  Future<User> getProfile() async {
    final token = await getAccessToken();
    final response = await _client.get(
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

  String _connectionError() =>
      'Serveur inaccessible (${AppConfig.apiHost}).\n'
      'Démarrez le backend : docker compose up -d';

  String _parseApiError(http.Response response, {required String fallback}) {
    try {
      final body = jsonDecode(response.body);
      if (body is Map<String, dynamic>) {
        if (body['detail'] != null) return body['detail'].toString();
        final lines = <String>[];
        body.forEach((key, value) {
          if (value is List) {
            lines.add('${_fieldLabel(key)} : ${value.join(', ')}');
          } else {
            lines.add('${_fieldLabel(key)} : $value');
          }
        });
        if (lines.isNotEmpty) return lines.join('\n');
      }
    } catch (_) {}
    return '$fallback (code ${response.statusCode})';
  }

  String _fieldLabel(String key) => switch (key) {
    'username' => 'Utilisateur',
    'email' => 'Email',
    'password' => 'Mot de passe',
    'role' => 'Rôle',
    'non_field_errors' => 'Erreur',
    _ => key,
  };
}
