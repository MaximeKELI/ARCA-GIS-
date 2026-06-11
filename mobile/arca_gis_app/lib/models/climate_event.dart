class ClimateEvent {
  final int id;
  final String eventType;
  final String eventTypeDisplay;
  final String severity;
  final String severityDisplay;
  final String title;
  final String description;
  final double? centerLat;
  final double? centerLng;
  final double? temperature;
  final double? rainfallMm;
  final String? aiRecommendation;
  final double aiConfidence;
  final bool isActive;

  ClimateEvent({
    required this.id,
    required this.eventType,
    required this.eventTypeDisplay,
    required this.severity,
    required this.severityDisplay,
    required this.title,
    required this.description,
    this.centerLat,
    this.centerLng,
    this.temperature,
    this.rainfallMm,
    this.aiRecommendation,
    this.aiConfidence = 0,
    this.isActive = true,
  });

  factory ClimateEvent.fromJson(Map<String, dynamic> json) {
    return ClimateEvent(
      id: json['id'],
      eventType: json['event_type'] ?? '',
      eventTypeDisplay: json['event_type_display'] ?? '',
      severity: json['severity'] ?? 'medium',
      severityDisplay: json['severity_display'] ?? '',
      title: json['title'] ?? '',
      description: json['description'] ?? '',
      centerLat: json['center_lat']?.toDouble(),
      centerLng: json['center_lng']?.toDouble(),
      temperature: json['temperature']?.toDouble(),
      rainfallMm: json['rainfall_mm']?.toDouble(),
      aiRecommendation: json['ai_recommendation'],
      aiConfidence: (json['ai_confidence'] ?? 0).toDouble(),
      isActive: json['is_active'] ?? true,
    );
  }
}
