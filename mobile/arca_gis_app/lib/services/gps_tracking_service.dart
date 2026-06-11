import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../config/app_config.dart';
import 'auth_service.dart';

class RescuePosition {
  final int userId;
  final String name;
  final double lat;
  final double lng;
  final bool isAvailable;

  RescuePosition({
    required this.userId,
    required this.name,
    required this.lat,
    required this.lng,
    this.isAvailable = true,
  });

  factory RescuePosition.fromJson(Map<String, dynamic> json) {
    return RescuePosition(
      userId: json['user_id'],
      name: json['name'] ?? json['username'] ?? '',
      lat: (json['lat'] as num).toDouble(),
      lng: (json['lng'] as num).toDouble(),
      isAvailable: json['is_available'] ?? true,
    );
  }
}

class GPSTrackingService {
  WebSocketChannel? _channel;
  final _positions = <int, RescuePosition>{};
  final _controller = StreamController<List<RescuePosition>>.broadcast();
  final AuthService _auth = AuthService();

  Stream<List<RescuePosition>> get positionsStream => _controller.stream;
  List<RescuePosition> get positions => _positions.values.toList();

  Future<void> connect() async {
    final token = await _auth.getAccessToken();
    if (token == null) return;

    _channel = WebSocketChannel.connect(
      Uri.parse('${AppConfig.wsGpsUrl}?token=$token'),
    );

    _channel!.stream.listen((data) {
      try {
        final json = jsonDecode(data);
        if (json is Map && json.containsKey('lat')) {
          final pos = RescuePosition.fromJson(Map<String, dynamic>.from(json));
          _positions[pos.userId] = pos;
          _controller.add(positions);
        }
      } catch (_) {}
    });
  }

  void sendPosition(double lat, double lng) {
    _channel?.sink.add(jsonEncode({'lat': lat, 'lng': lng}));
  }

  void dispose() {
    _channel?.sink.close();
    _controller.close();
  }
}
