import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../config/theme.dart';
import '../providers/security_provider.dart';
import '../services/biometric_service.dart';

class LockScreen extends StatefulWidget {
  final VoidCallback onUnlocked;

  const LockScreen({super.key, required this.onUnlocked});

  @override
  State<LockScreen> createState() => _LockScreenState();
}

class _LockScreenState extends State<LockScreen> {
  final _bio = BiometricService();
  String _pin = '';
  String? _error;
  bool _bioAvailable = false;

  @override
  void initState() {
    super.initState();
    _initBio();
  }

  Future<void> _initBio() async {
    _bioAvailable = await _bio.isAvailable();
    if (mounted) setState(() {});
    final sec = context.read<SecurityProvider>();
    if (sec.biometricEnabled && _bioAvailable) {
      _tryBiometric();
    }
  }

  Future<void> _tryBiometric() async {
    final ok = await _bio.authenticate();
    if (ok && mounted) {
      context.read<SecurityProvider>().unlock();
      widget.onUnlocked();
    }
  }

  Future<void> _submitPin() async {
    final sec = context.read<SecurityProvider>();
    if (await sec.verifyPin(_pin)) {
      sec.unlock();
      widget.onUnlocked();
    } else {
      setState(() { _error = 'Code incorrect'; _pin = ''; });
    }
  }

  void _tapDigit(String d) {
    if (_pin.length >= 4) return;
    setState(() {
      _error = null;
      _pin += d;
      if (_pin.length == 4) _submitPin();
    });
  }

  @override
  Widget build(BuildContext context) {
    final sec = context.watch<SecurityProvider>();
    return Scaffold(
      backgroundColor: AppTheme.primaryGreen,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(children: [
            const Spacer(),
            const Icon(Icons.lock, size: 64, color: Colors.white),
            const SizedBox(height: 16),
            const Text('ARCA-GIS verrouillé', style: TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(
              sec.pinEnabled ? 'Entrez votre code PIN' : 'Authentification requise',
              style: TextStyle(color: Colors.white.withValues(alpha: 0.85)),
            ),
            const SizedBox(height: 32),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(4, (i) => Container(
                margin: const EdgeInsets.symmetric(horizontal: 8),
                width: 16, height: 16,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: i < _pin.length ? Colors.white : Colors.white.withValues(alpha: 0.3),
                ),
              )),
            ),
            if (_error != null) Padding(
              padding: const EdgeInsets.only(top: 12),
              child: Text(_error!, style: const TextStyle(color: Colors.amber)),
            ),
            const Spacer(),
            if (sec.pinEnabled) _pinPad(),
            if (sec.biometricEnabled && _bioAvailable) ...[
              const SizedBox(height: 16),
              OutlinedButton.icon(
                onPressed: _tryBiometric,
                icon: const Icon(Icons.fingerprint, color: Colors.white),
                label: const Text('Empreinte / Face ID', style: TextStyle(color: Colors.white)),
                style: OutlinedButton.styleFrom(side: const BorderSide(color: Colors.white54)),
              ),
            ],
            const SizedBox(height: 24),
          ]),
        ),
      ),
    );
  }

  Widget _pinPad() {
    const keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '', '0', '⌫'];
    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3, mainAxisSpacing: 12, crossAxisSpacing: 12),
      itemCount: keys.length,
      itemBuilder: (_, i) {
        final k = keys[i];
        if (k.isEmpty) return const SizedBox();
        return Material(
          color: Colors.white.withValues(alpha: 0.15),
          borderRadius: BorderRadius.circular(12),
          child: InkWell(
            borderRadius: BorderRadius.circular(12),
            onTap: () => k == '⌫'
                ? setState(() { if (_pin.isNotEmpty) _pin = _pin.substring(0, _pin.length - 1); _error = null; })
                : _tapDigit(k),
            child: Center(child: Text(k, style: const TextStyle(color: Colors.white, fontSize: 24))),
          ),
        );
      },
    );
  }
}
