import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class UssdSimulatorScreen extends StatefulWidget {
  const UssdSimulatorScreen({super.key});
  @override
  State<UssdSimulatorScreen> createState() => _UssdSimulatorScreenState();
}

class _UssdSimulatorScreenState extends State<UssdSimulatorScreen> {
  final _api = ApiService();
  final _input = TextEditingController();
  String _response = 'Composez *123# pour commencer';

  Future<void> _send() async {
    final r = await _api.post('/communications/ussd/simulate/', {'text': _input.text, 'phone': '+2250700000001'});
    setState(() => _response = r['response']?.toString() ?? '');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Simulateur USSD'), backgroundColor: AppTheme.primaryGreen),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(color: Colors.grey.shade200, borderRadius: BorderRadius.circular(8)),
            child: Text(_response),
          ),
          const SizedBox(height: 16),
          TextField(controller: _input, decoration: const InputDecoration(labelText: 'Entrée USSD')),
          const SizedBox(height: 8),
          ElevatedButton(onPressed: _send, child: const Text('Envoyer')),
        ]),
      ),
    );
  }
}
