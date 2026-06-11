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
            ListTile(
              leading: const Icon(Icons.sensors),
              title: const Text('Capteurs IoT'),
              subtitle: const Text('Stations connectées'),
              onTap: () => Navigator.pop(context),
            ),
            ListTile(
              leading: const Icon(Icons.dashboard),
              title: const Text('Dashboard web'),
              subtitle: const Text('admin.arca-gis.local/dashboard'),
              onTap: () => Navigator.pop(context),
            ),
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
