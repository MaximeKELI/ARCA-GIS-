import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class ParcelQrScreen extends StatefulWidget {
  final int parcelId;
  const ParcelQrScreen({super.key, required this.parcelId});

  @override
  State<ParcelQrScreen> createState() => _ParcelQrScreenState();
}

class _ParcelQrScreenState extends State<ParcelQrScreen> {
  final _api = ApiService();
  final _verifyCtrl = TextEditingController();
  Map<String, dynamic>? _qr;
  Map<String, dynamic>? _verifyResult;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final data = await _api.get('/parcels/${widget.parcelId}/qr/');
      setState(() => _qr = data is Map<String, dynamic> ? data : null);
    } catch (_) {}
  }

  Future<void> _verify() async {
    final code = _verifyCtrl.text.trim();
    if (code.isEmpty) return;
    try {
      final data = await _api.get('/parcels/verify/$code/');
      setState(() => _verifyResult = data is Map<String, dynamic> ? data : null);
    } catch (_) {
      setState(() => _verifyResult = {'valid': false});
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('QR Parcelle'), backgroundColor: AppTheme.primaryGreen),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          if (_qr != null) ...[
            Text(_qr!['name']?.toString() ?? '', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(24),
              color: Colors.grey.shade200,
              child: Text(_qr!['qr_code']?.toString() ?? '', style: const TextStyle(fontSize: 28, letterSpacing: 2)),
            ),
            const SizedBox(height: 8),
            ElevatedButton.icon(
              onPressed: () {
                Clipboard.setData(ClipboardData(text: _qr!['qr_code']?.toString() ?? ''));
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Code copié')));
              },
              icon: const Icon(Icons.copy), label: const Text('Copier le code'),
            ),
          ],
          const Divider(height: 32),
          const Text('Vérifier un code', style: TextStyle(fontWeight: FontWeight.bold)),
          TextField(controller: _verifyCtrl, decoration: const InputDecoration(hintText: 'ARCA-XXXXXXXXXXXX')),
          ElevatedButton(onPressed: _verify, child: const Text('Vérifier')),
          if (_verifyResult != null)
            Text(_verifyResult!['valid'] == true
                ? 'Valide: ${_verifyResult!['parcel']} (${_verifyResult!['crop']})'
                : 'Code invalide'),
        ]),
      ),
    );
  }
}
