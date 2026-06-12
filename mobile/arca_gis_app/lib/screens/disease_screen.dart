import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

class DiseaseScreen extends StatefulWidget {
  const DiseaseScreen({super.key});

  @override
  State<DiseaseScreen> createState() => _DiseaseScreenState();
}

class _DiseaseScreenState extends State<DiseaseScreen> {
  final _api = ApiService();
  final _picker = ImagePicker();
  Map<String, dynamic>? _result;
  bool _analyzing = false;
  String _crop = 'maize';

  Future<void> _pickAndAnalyze() async {
    final image = await _picker.pickImage(source: ImageSource.camera, maxWidth: 1024, imageQuality: 85);
    if (image == null) return;
    setState(() { _analyzing = true; _result = null; });
    try {
      final bytes = await image.readAsBytes();
      final data = await _api.post('/ai/disease/', {
        'image_b64': base64Encode(bytes),
        'crop_type': _crop,
      });
      setState(() => _result = parseApiMap(data));
    } catch (e) {
      setState(() => _result = {'error': e.toString()});
    } finally {
      setState(() => _analyzing = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Diagnostic maladies'), backgroundColor: AppTheme.primaryGreen),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            DropdownButtonFormField<String>(
              initialValue: _crop,
              decoration: const InputDecoration(labelText: 'Culture'),
              items: const [
                DropdownMenuItem(value: 'maize', child: Text('Maïs')),
                DropdownMenuItem(value: 'rice', child: Text('Riz')),
                DropdownMenuItem(value: 'cassava', child: Text('Manioc')),
              ],
              onChanged: (v) => setState(() => _crop = v ?? 'maize'),
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: _analyzing ? null : _pickAndAnalyze,
              icon: const Icon(Icons.camera_alt),
              label: Text(_analyzing ? 'Analyse...' : 'Photographier la plante'),
              style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGreen, foregroundColor: Colors.white, minimumSize: const Size(double.infinity, 48)),
            ),
            const SizedBox(height: 24),
            if (_result != null) ...[
              if (_result!['error'] != null)
                Text(_result!['error'].toString(), style: const TextStyle(color: Colors.red))
              else ...[
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Diagnostic: ${_result!['diagnosis']?['name'] ?? ''}',
                            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                        Text('Confiance: ${(((_result!['confidence'] as num?) ?? 0) * 100).toInt()}%'),
                        const SizedBox(height: 8),
                        Text('Traitement: ${_result!['treatment']}'),
                        if (_result!['prevention'] != null)
                          Padding(
                            padding: const EdgeInsets.only(top: 8),
                            child: Text('Prévention: ${_result!['prevention']}', style: TextStyle(fontSize: 13, color: Colors.grey.shade700)),
                          ),
                      ],
                    ),
                  ),
                ),
              ],
            ],
          ],
        ),
      ),
    );
  }
}
