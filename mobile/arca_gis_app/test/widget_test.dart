import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:arca_gis_app/main.dart';

import 'helpers/secure_storage_mock.dart';

void main() {
  setUp(() {
    mockSecureStorage();
    SharedPreferences.setMockInitialValues({});
  });

  testWidgets('App démarre sur le splash puis affiche la connexion', (tester) async {
    await tester.pumpWidget(const ArcaGisApp());
    expect(find.text('ARCA-GIS'), findsOneWidget);

    await tester.pump(const Duration(seconds: 2));
    await tester.pumpAndSettle();

    expect(find.text('Se connecter'), findsOneWidget);
  });
}
