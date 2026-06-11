class AlertModel {
  final int? id;
  final String alertType;
  final String severity;
  final String title;
  final String message;
  final Map<String, dynamic> data;
  final bool isRead;
  final DateTime? createdAt;

  AlertModel({
    this.id,
    required this.alertType,
    required this.severity,
    required this.title,
    required this.message,
    this.data = const {},
    this.isRead = false,
    this.createdAt,
  });

  factory AlertModel.fromJson(Map<String, dynamic> json) {
    return AlertModel(
      id: json['id'],
      alertType: json['alert_type'] ?? 'system',
      severity: json['severity'] ?? 'medium',
      title: json['title'] ?? '',
      message: json['message'] ?? '',
      data: Map<String, dynamic>.from(json['data'] ?? {}),
      isRead: json['is_read'] ?? false,
      createdAt: json['created_at'] != null ? DateTime.tryParse(json['created_at']) : null,
    );
  }
}
