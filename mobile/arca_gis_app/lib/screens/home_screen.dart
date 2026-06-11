import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../config/theme.dart';
import '../providers/map_provider.dart';
import 'alerts_screen.dart';
import 'analytics_screen.dart';
import 'forecast_screen.dart';
import 'map_screen.dart';
import 'parcels_screen.dart';
import 'profile_screen.dart';
import 'cooperatives_screen.dart';
import 'marketplace_screen.dart';
import 'voice_assistant_screen.dart';
import 'ar_screen.dart';
import 'traceability_screen.dart';
import 'forum_screen.dart';
import 'training_screen.dart';
import 'gamification_screen.dart';
import 'insurance_screen.dart';
import 'disease_screen.dart';
import 'feature_phone_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _currentIndex = 0;

  final _screens = const [
    MapScreen(),
    ParcelsScreen(),
    AlertsScreen(),
    AnalyticsScreen(),
    ProfileScreen(),
  ];

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<MapProvider>().initialize();
    });
  }

  @override
  Widget build(BuildContext context) {
    final map = context.watch<MapProvider>();
    final alertCount = map.alerts.where((a) => !a.isRead).length;

    return Scaffold(
      appBar: map.isOffline ? AppBar(
        automaticallyImplyLeading: false,
        backgroundColor: AppTheme.accentOrange,
        title: const Text('Mode hors-ligne', style: TextStyle(fontSize: 14)),
        toolbarHeight: 32,
      ) : null,
      drawer: Drawer(
        child: ListView(
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(color: AppTheme.primaryGreen),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Icon(Icons.map, color: Colors.white, size: 40),
                  SizedBox(height: 8),
                  Text('ARCA-GIS', style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                  Text('Agro-Rescue Climate Africa', style: TextStyle(color: Colors.white70, fontSize: 12)),
                ],
              ),
            ),
            ListTile(
              leading: const Icon(Icons.wb_sunny),
              title: const Text('Prévisions météo'),
              onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ForecastScreen())),
            ),
            ListTile(leading: const Icon(Icons.groups), title: const Text('Coopératives'),
              onTap: () { Navigator.pop(context); Navigator.push(context, MaterialPageRoute(builder: (_) => const CooperativesScreen())); }),
            ListTile(leading: const Icon(Icons.store), title: const Text('Prix marchés'),
              onTap: () { Navigator.pop(context); Navigator.push(context, MaterialPageRoute(builder: (_) => const MarketplaceScreen())); }),
            ListTile(leading: const Icon(Icons.mic), title: const Text('Assistant vocal'),
              onTap: () { Navigator.pop(context); Navigator.push(context, MaterialPageRoute(builder: (_) => const VoiceAssistantScreen())); }),
            ListTile(leading: const Icon(Icons.view_in_ar), title: const Text('Réalité augmentée'),
              onTap: () { Navigator.pop(context); Navigator.push(context, MaterialPageRoute(builder: (_) => const ARScreen())); }),
            ListTile(leading: const Icon(Icons.verified), title: const Text('Traçabilité'),
              onTap: () { Navigator.pop(context); Navigator.push(context, MaterialPageRoute(builder: (_) => const TraceabilityScreen())); }),
            ListTile(leading: const Icon(Icons.sms), title: const Text('SOS par SMS/USSD'),
              subtitle: const Text('*384*ARCA#'), onTap: () => Navigator.pop(context)),
            const Divider(),
            ListTile(leading: const Icon(Icons.forum), title: const Text('Forum'),
              onTap: () { Navigator.pop(context); Navigator.push(context, MaterialPageRoute(builder: (_) => const ForumScreen())); }),
            ListTile(leading: const Icon(Icons.school), title: const Text('Formation'),
              onTap: () { Navigator.pop(context); Navigator.push(context, MaterialPageRoute(builder: (_) => const TrainingScreen())); }),
            ListTile(leading: const Icon(Icons.emoji_events), title: const Text('Badges & Points'),
              onTap: () { Navigator.pop(context); Navigator.push(context, MaterialPageRoute(builder: (_) => const GamificationScreen())); }),
            ListTile(leading: const Icon(Icons.shield), title: const Text('Assurance'),
              onTap: () { Navigator.pop(context); Navigator.push(context, MaterialPageRoute(builder: (_) => const InsuranceScreen())); }),
            ListTile(leading: const Icon(Icons.biotech), title: const Text('Diagnostic maladies'),
              onTap: () { Navigator.pop(context); Navigator.push(context, MaterialPageRoute(builder: (_) => const DiseaseScreen())); }),
            ListTile(leading: const Icon(Icons.phone_android), title: const Text('Mode feature phone'),
              onTap: () { Navigator.pop(context); Navigator.push(context, MaterialPageRoute(builder: (_) => const FeaturePhoneScreen())); }),
          ],
        ),
      ),
      body: IndexedStack(index: _currentIndex, children: _screens),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (i) => setState(() => _currentIndex = i),
        type: BottomNavigationBarType.fixed,
        items: [
          const BottomNavigationBarItem(icon: Icon(Icons.map), label: 'Carte'),
          const BottomNavigationBarItem(icon: Icon(Icons.agriculture), label: 'Parcelles'),
          BottomNavigationBarItem(
            icon: Badge(
              isLabelVisible: alertCount > 0,
              label: Text('$alertCount'),
              child: const Icon(Icons.notifications),
            ),
            label: 'Alertes',
          ),
          const BottomNavigationBarItem(icon: Icon(Icons.bar_chart), label: 'Stats'),
          const BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profil'),
        ],
      ),
    );
  }
}
