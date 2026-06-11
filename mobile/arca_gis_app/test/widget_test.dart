import 'package:flutter_test/flutter_test.dart';
import 'package:arca_gis_app/main.dart';

void main() {
  testWidgets('App launches splash screen', (WidgetTester tester) async {
    await tester.pumpWidget(const ArcaGisApp());
    expect(find.text('ARCA-GIS'), findsOneWidget);
  });
}
