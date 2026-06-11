import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../config/app_config.dart';
import '../models/alert.dart';
import 'auth_service.dart';

class WebSocketService {
  WebSocketChannel? _channel;
  final _alertController = StreamController<AlertModel>.broadcast();
  final AuthService _auth = AuthService();

  Stream<AlertModel> get alertStream => _alertController.stream;

  Future<void> connect() async {
    final token = await _auth.getAccessToken();
    if (token == null) return;

    disconnect();

    try {
      _channel = WebSocketChannel.connect(
        Uri.parse('${AppConfig.wsAlertsUrl}?token=$token'),
      );

      _channel!.stream.listen(
        (data) {
          try {
            final json = jsonDecode(data);
            if (json is Map<String, dynamic> && json.containsKey('title')) {
              _alertController.add(AlertModel.fromJson(json));
            }
          } catch (_) {}
        },
        onError: (_) => _scheduleReconnect(),
        onDone: () => _scheduleReconnect(),
      );
    } catch (_) {
      _scheduleReconnect();
    }
  }

  void _scheduleReconnect() {
    Future.delayed(const Duration(seconds: 5), connect);
  }

  void disconnect() {
    _channel?.sink.close();
    _channel = null;
  }

  void dispose() {
    disconnect();
    _alertController.close();
  }
}
