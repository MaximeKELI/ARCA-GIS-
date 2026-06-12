/// Parse une réponse API DRF (liste directe ou paginée).
List<dynamic> parseApiList(dynamic data) {
  if (data is List) return data;
  if (data is Map && data['results'] is List) return data['results'] as List;
  return [];
}

Map<String, dynamic> parseApiMap(dynamic data) {
  if (data is Map<String, dynamic>) return data;
  return {};
}
