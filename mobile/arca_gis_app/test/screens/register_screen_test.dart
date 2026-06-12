import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:arca_gis_app/config/theme.dart';
import 'package:arca_gis_app/providers/auth_provider.dart';
import 'package:arca_gis_app/providers/security_provider.dart';
import 'package:arca_gis_app/screens/register_screen.dart';

import '../fakes/fake_auth_service.dart';
import '../helpers/secure_storage_mock.dart';

void main() {
  late FakeAuthService fakeAuth;

  setUp(() {
    mockSecureStorage();
    SharedPreferences.setMockInitialValues({});
    fakeAuth = FakeAuthService();
  });

  Widget buildScreen() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => AuthProvider(authService: fakeAuth),
        ),
        ChangeNotifierProvider(create: (_) => SecurityProvider()),
      ],
      child: MaterialApp(
        theme: AppTheme.lightTheme,
        home: const RegisterScreen(),
      ),
    );
  }

  Future<void> tapRegister(WidgetTester tester) async {
    await tester.ensureVisible(find.text('S\'inscrire'));
    await tester.tap(find.text('S\'inscrire'));
  }

  Future<void> fillForm(
    WidgetTester tester, {
    String password = 'testpass123',
    String passwordConfirm = 'testpass123',
  }) async {
    final fields = find.byType(TextFormField);
    await tester.enterText(fields.at(0), 'Jean');
    await tester.enterText(fields.at(1), 'Kouassi');
    await tester.enterText(fields.at(2), 'jean_k');
    await tester.enterText(fields.at(3), 'jean@example.ci');
    await tester.enterText(fields.at(4), password);
    await tester.enterText(fields.at(5), passwordConfirm);
  }

  group('RegisterScreen', () {
    testWidgets('affiche le champ de confirmation du mot de passe', (tester) async {
      await tester.pumpWidget(buildScreen());

      expect(find.text('Confirmer le mot de passe'), findsOneWidget);
      expect(find.text('S\'inscrire'), findsOneWidget);
    });

    testWidgets('refuse des mots de passe différents', (tester) async {
      await tester.pumpWidget(buildScreen());
      await fillForm(tester, password: 'testpass123', passwordConfirm: 'autre1234');

      await tapRegister(tester);
      await tester.pump();

      expect(find.text('Les mots de passe ne correspondent pas'), findsOneWidget);
      expect(fakeAuth.registerCallCount, 0);
    });

    testWidgets('refuse un mot de passe trop court', (tester) async {
      await tester.pumpWidget(buildScreen());
      await fillForm(tester, password: 'court', passwordConfirm: 'court');

      await tapRegister(tester);
      await tester.pump();

      expect(find.text('Min. 8 caractères'), findsOneWidget);
      expect(fakeAuth.registerCallCount, 0);
    });

    testWidgets('soumet le formulaire valide', (tester) async {
      final pending = Completer<void>();
      fakeAuth = FakeAuthService(
        onRegister: () async {
          await pending.future;
          throw StateError('non utilisé');
        },
      );
      await tester.pumpWidget(buildScreen());
      await fillForm(tester);

      await tapRegister(tester);
      await tester.pump();

      expect(fakeAuth.registerCallCount, 1);
      expect(fakeAuth.lastUsername, 'jean_k');
      expect(fakeAuth.lastPassword, 'testpass123');
    });

    testWidgets('affiche une erreur serveur', (tester) async {
      fakeAuth = FakeAuthService(registerError: Exception('Utilisateur déjà pris'));
      await tester.pumpWidget(buildScreen());
      await fillForm(tester);

      await tapRegister(tester);
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 100));

      expect(find.text('Utilisateur déjà pris'), findsOneWidget);
    });
  });
}
