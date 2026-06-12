import 'package:flutter_test/flutter_test.dart';
import 'package:arca_gis_app/models/user.dart';

void main() {
  group('User.fromJson', () {
    test('parse un profil complet', () {
      final user = User.fromJson({
        'id': 1,
        'username': 'kouassi',
        'email': 'k@ci.com',
        'first_name': 'Jean',
        'last_name': 'Kouassi',
        'role': 'farmer',
        'role_display': 'Agriculteur',
        'phone': '+22501',
        'country': "Côte d'Ivoire",
        'region': 'Bouaké',
        'position_lat': 7.69,
        'position_lng': -5.03,
      });

      expect(user.id, 1);
      expect(user.fullName, 'Jean Kouassi');
      expect(user.isFarmer, isTrue);
      expect(user.isRescue, isFalse);
      expect(user.positionLat, 7.69);
    });

    test('utilise le username si le nom est vide', () {
      final user = User.fromJson({
        'id': 2,
        'username': 'anon',
        'role': 'rescue',
      });

      expect(user.fullName, 'anon');
      expect(user.isRescue, isTrue);
    });
  });
}
