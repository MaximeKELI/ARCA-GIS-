import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../config/app_config.dart';
import '../providers/security_provider.dart';
import '../services/biometric_service.dart';
import '../config/theme.dart';
import '../providers/auth_provider.dart';
import '../providers/locale_provider.dart';
import '../providers/theme_provider.dart';
import 'login_screen.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    final user = auth.user;

    if (user == null) return const SizedBox();

    return Scaffold(
      appBar: AppBar(title: const Text('Profil')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  CircleAvatar(
                    radius: 40,
                    backgroundColor: AppTheme.primaryGreen.withValues(alpha: 0.2),
                    child: Text(
                      user.firstName.isNotEmpty ? user.firstName[0].toUpperCase() : user.username[0].toUpperCase(),
                      style: const TextStyle(fontSize: 32, color: AppTheme.primaryGreen, fontWeight: FontWeight.bold),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(user.fullName, style: Theme.of(context).textTheme.titleLarge),
                  const SizedBox(height: 4),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                    decoration: BoxDecoration(
                      color: _roleColor(user.role).withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(user.roleDisplay, style: TextStyle(color: _roleColor(user.role), fontWeight: FontWeight.w600)),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          _infoTile(Icons.person, 'Utilisateur', user.username),
          _infoTile(Icons.email, 'Email', user.email),
          if (user.phone.isNotEmpty) _infoTile(Icons.phone, 'Téléphone', user.phone),
          _infoTile(Icons.public, 'Pays', user.country),
          if (user.region.isNotEmpty) _infoTile(Icons.location_on, 'Région', user.region),
          const SizedBox(height: 16),
          Card(
            child: SwitchListTile(
              secondary: const Icon(Icons.dark_mode, color: AppTheme.primaryGreen),
              title: const Text('Mode sombre'),
              value: context.watch<ThemeProvider>().isDark,
              onChanged: (_) => context.read<ThemeProvider>().toggle(),
            ),
          ),
          Card(
            child: ListTile(
              leading: const Icon(Icons.language, color: AppTheme.primaryGreen),
              title: const Text('Langue'),
              trailing: DropdownButton<String>(
                value: context.watch<LocaleProvider>().locale.languageCode,
                underline: const SizedBox(),
                items: const [
                  DropdownMenuItem(value: 'fr', child: Text('Français')),
                  DropdownMenuItem(value: 'en', child: Text('English')),
                  DropdownMenuItem(value: 'sw', child: Text('Kiswahili')),
                ],
                onChanged: (v) => context.read<LocaleProvider>().setLocale(v!),
              ),
            ),
          ),
          const SizedBox(height: 24),
          Card(
            child: Column(
              children: [
                ListTile(
                  leading: const Icon(Icons.info_outline, color: AppTheme.primaryGreen),
                  title: const Text('À propos'),
                  subtitle: Text('${AppConfig.appName} v5.0.0\n${AppConfig.appSubtitle}'),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          OutlinedButton.icon(
            onPressed: () async {
              await auth.logout();
              if (context.mounted) {
                Navigator.of(context).pushAndRemoveUntil(
                  MaterialPageRoute(builder: (_) => const LoginScreen()),
                  (_) => false,
                );
              }
            },
            icon: const Icon(Icons.logout, color: AppTheme.sosRed),
            label: const Text('Déconnexion', style: TextStyle(color: AppTheme.sosRed)),
            style: OutlinedButton.styleFrom(
              side: const BorderSide(color: AppTheme.sosRed),
              padding: const EdgeInsets.symmetric(vertical: 14),
            ),
          ),
        ],
      ),
    );
  }

  Widget _infoTile(IconData icon, String label, String value) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Icon(icon, color: AppTheme.primaryGreen),
        title: Text(label, style: const TextStyle(fontSize: 12, color: Colors.grey)),
        subtitle: Text(value, style: const TextStyle(fontWeight: FontWeight.w500)),
      ),
    );
  }

  Color _roleColor(String role) {
    switch (role) {
      case 'farmer':
        return AppTheme.primaryGreen;
      case 'rescue':
        return AppTheme.sosRed;
      case 'admin':
        return AppTheme.climateBlue;
      default:
        return Colors.grey;
    }
  }
}
