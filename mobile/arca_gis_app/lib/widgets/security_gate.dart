import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/security_provider.dart';
import '../screens/lock_screen.dart';

/// Verrouille l'app au retour arrière-plan si sécurité activée.
class SecurityGate extends StatefulWidget {
  final Widget child;

  const SecurityGate({super.key, required this.child});

  @override
  State<SecurityGate> createState() => _SecurityGateState();
}

class _SecurityGateState extends State<SecurityGate> with WidgetsBindingObserver {
  bool _showLock = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _syncLock();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.paused || state == AppLifecycleState.inactive) {
      context.read<SecurityProvider>().lock();
    }
    if (state == AppLifecycleState.resumed) {
      _syncLock();
    }
  }

  void _syncLock() {
    final locked = context.read<SecurityProvider>().isLocked;
    if (locked != _showLock) setState(() => _showLock = locked);
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<SecurityProvider>(
      builder: (context, sec, _) {
        if (sec.isLocked) {
          return LockScreen(onUnlocked: () => setState(() => _showLock = false));
        }
        return widget.child;
      },
    );
  }
}
