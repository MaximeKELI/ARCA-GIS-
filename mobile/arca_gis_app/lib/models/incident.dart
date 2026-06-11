class Incident {
  final int id;
  final String incidentType;
  final String incidentTypeDisplay;
  final String status;
  final String statusDisplay;
  final String priority;
  final String title;
  final String description;
  final double lat;
  final double lng;
  final bool isSos;
  final String reporterName;
  final DateTime? createdAt;

  Incident({
    required this.id,
    required this.incidentType,
    required this.incidentTypeDisplay,
    required this.status,
    required this.statusDisplay,
    required this.priority,
    required this.title,
    required this.description,
    required this.lat,
    required this.lng,
    this.isSos = false,
    this.reporterName = '',
    this.createdAt,
  });

  factory Incident.fromJson(Map<String, dynamic> json) {
    return Incident(
      id: json['id'],
      incidentType: json['incident_type'] ?? '',
      incidentTypeDisplay: json['incident_type_display'] ?? '',
      status: json['status'] ?? 'pending',
      statusDisplay: json['status_display'] ?? '',
      priority: json['priority'] ?? 'medium',
      title: json['title'] ?? '',
      description: json['description'] ?? '',
      lat: (json['lat'] ?? 0).toDouble(),
      lng: (json['lng'] ?? 0).toDouble(),
      isSos: json['is_sos'] ?? false,
      reporterName: json['reporter_name'] ?? '',
      createdAt: json['created_at'] != null ? DateTime.tryParse(json['created_at']) : null,
    );
  }
}
