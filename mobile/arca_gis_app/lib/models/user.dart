class User {
  final int id;
  final String username;
  final String email;
  final String firstName;
  final String lastName;
  final String role;
  final String roleDisplay;
  final String phone;
  final String country;
  final String region;
  final double? positionLat;
  final double? positionLng;

  User({
    required this.id,
    required this.username,
    required this.email,
    required this.firstName,
    required this.lastName,
    required this.role,
    required this.roleDisplay,
    this.phone = '',
    this.country = '',
    this.region = '',
    this.positionLat,
    this.positionLng,
  });

  String get fullName => '$firstName $lastName'.trim().isEmpty ? username : '$firstName $lastName'.trim();

  bool get isFarmer => role == 'farmer';
  bool get isRescue => role == 'rescue';
  bool get isAdmin => role == 'admin';

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      username: json['username'] ?? '',
      email: json['email'] ?? '',
      firstName: json['first_name'] ?? '',
      lastName: json['last_name'] ?? '',
      role: json['role'] ?? 'farmer',
      roleDisplay: json['role_display'] ?? '',
      phone: json['phone'] ?? '',
      country: json['country'] ?? '',
      region: json['region'] ?? '',
      positionLat: json['position_lat']?.toDouble(),
      positionLng: json['position_lng']?.toDouble(),
    );
  }
}
