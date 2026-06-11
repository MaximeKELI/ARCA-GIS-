import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../config/app_config.dart';
import 'auth_service.dart';
import 'api_service.dart';

class ChatMessage {
  final int? id;
  final String sender;
  final String senderName;
  final String senderRole;
  final String message;
  final DateTime? createdAt;

  ChatMessage({
    this.id,
    required this.sender,
    required this.senderName,
    required this.senderRole,
    required this.message,
    this.createdAt,
  });

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
      id: json['id'],
      sender: json['sender'] ?? '',
      senderName: json['sender_name'] ?? json['sender'] ?? '',
      senderRole: json['sender_role'] ?? '',
      message: json['message'] ?? '',
      createdAt: json['created_at'] != null ? DateTime.tryParse(json['created_at']) : null,
    );
  }
}

class ChatService {
  final ApiService _api = ApiService();
  final AuthService _auth = AuthService();
  WebSocketChannel? _channel;
  final _messages = StreamController<ChatMessage>.broadcast();

  Stream<ChatMessage> get messageStream => _messages.stream;

  Future<List<ChatMessage>> loadHistory(int incidentId) async {
    final data = await _api.get('/chat/$incidentId/');
    final items = data['results'] ?? data;
    if (items is List) {
      return items.map((j) => ChatMessage.fromJson(j)).toList();
    }
    return [];
  }

  Future<void> connect(int incidentId) async {
    final token = await _auth.getAccessToken();
    if (token == null) return;

    _channel = WebSocketChannel.connect(
      Uri.parse('${AppConfig.wsChatUrl(incidentId)}?token=$token'),
    );

    _channel!.stream.listen((data) {
      try {
        final json = jsonDecode(data);
        if (json is Map && json.containsKey('message')) {
          _messages.add(ChatMessage.fromJson(json));
        }
      } catch (_) {}
    });
  }

  void sendMessage(String message) {
    _channel?.sink.add(jsonEncode({'message': message}));
  }

  void dispose() {
    _channel?.sink.close();
    _messages.close();
  }
}
