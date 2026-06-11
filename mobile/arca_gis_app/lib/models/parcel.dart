class Parcel {
  final int id;
  final String name;
  final String cropType;
  final String cropTypeDisplay;
  final double areaHectares;
  final String healthStatus;
  final String healthStatusDisplay;
  final double soilMoisture;
  final double? centroidLat;
  final double? centroidLng;
  final bool isActive;
  final List<List<double>>? coordinates;

  Parcel({
    required this.id,
    required this.name,
    required this.cropType,
    required this.cropTypeDisplay,
    required this.areaHectares,
    required this.healthStatus,
    required this.healthStatusDisplay,
    required this.soilMoisture,
    this.centroidLat,
    this.centroidLng,
    this.isActive = true,
    this.coordinates,
  });

  factory Parcel.fromJson(Map<String, dynamic> json) {
    List<List<double>>? coords;
    if (json['geometry'] != null) {
      final geom = json['geometry'];
      if (geom['type'] == 'Polygon' && geom['coordinates'] != null) {
        final ring = geom['coordinates'][0] as List;
        coords = ring.map<List<double>>((c) => [(c[0] as num).toDouble(), (c[1] as num).toDouble()]).toList();
      }
    }

    return Parcel(
      id: json['id'],
      name: json['name'] ?? '',
      cropType: json['crop_type'] ?? '',
      cropTypeDisplay: json['crop_type_display'] ?? json['crop_type'] ?? '',
      areaHectares: (json['area_hectares'] ?? 0).toDouble(),
      healthStatus: json['health_status'] ?? 'good',
      healthStatusDisplay: json['health_status_display'] ?? '',
      soilMoisture: (json['soil_moisture'] ?? 0).toDouble(),
      centroidLat: json['centroid_lat']?.toDouble(),
      centroidLng: json['centroid_lng']?.toDouble(),
      isActive: json['is_active'] ?? true,
      coordinates: coords,
    );
  }
}
