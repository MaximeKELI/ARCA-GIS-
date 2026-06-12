import 'package:flutter/foundation.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:shared_preferences/shared_preferences.dart';

class SecurityProvider extends ChangeNotifier {
  static const _storage = FlutterSecureStorage();
  static const _pinKey = 'app_pin';

  bool biometricEnabled = false;
  bool pinEnabled = false;
  bool _locked = false;

  bool get isLocked => _locked && (biometricEnabled || pinEnabled);
  bool get isEnabled => biometricEnabled || pinEnabled;

  Future<void> load({bool lockOnStart = true}) async {
    final prefs = await SharedPreferences.getInstance();
    biometricEnabled = prefs.getBool('biometric_enabled') ?? false;
    pinEnabled = prefs.getBool('pin_enabled') ?? false;
    if (lockOnStart && isEnabled) _locked = true;
    notifyListeners();
  }

  Future<void> setBiometric(bool enabled) async {
    final prefs = await SharedPreferences.getInstance();
    biometricEnabled = enabled;
    await prefs.setBool('biometric_enabled', enabled);
    notifyListeners();
  }

  Future<void> setPin(String pin) async {
    if (pin.length < 4) return;
    await _storage.write(key: _pinKey, value: pin);
    final prefs = await SharedPreferences.getInstance();
    pinEnabled = true;
    await prefs.setBool('pin_enabled', true);
    notifyListeners();
  }

  Future<void> clearPin() async {
    await _storage.delete(key: _pinKey);
    final prefs = await SharedPreferences.getInstance();
    pinEnabled = false;
    await prefs.setBool('pin_enabled', false);
    if (!biometricEnabled) _locked = false;
    notifyListeners();
  }

  Future<bool> verifyPin(String pin) async {
    final stored = await _storage.read(key: _pinKey);
    return stored != null && stored == pin;
  }

  void lock() {
    if (isEnabled) {
      _locked = true;
      notifyListeners();
    }
  }

  void unlock() {
    _locked = false;
    notifyListeners();
  }
}
