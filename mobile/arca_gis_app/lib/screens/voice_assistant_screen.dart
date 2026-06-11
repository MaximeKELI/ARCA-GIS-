import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class VoiceAssistantScreen extends StatefulWidget {
  const VoiceAssistantScreen({super.key});
  @override
  State<VoiceAssistantScreen> createState() => _VoiceAssistantScreenState();
}

class _VoiceAssistantScreenState extends State<VoiceAssistantScreen> {
  final ApiService _api = ApiService();
  final _controller = TextEditingController();
  final List<Map<String, String>> _messages = [];
  String _language = 'fr';

  Future<void> _ask() async {
    final query = _controller.text.trim();
    if (query.isEmpty) return;
    setState(() => _messages.add({'role': 'user', 'text': query}));
    _controller.clear();

    try {
      final resp = await _api.post('/communications/voice/', {'text': query, 'language': _language});
      setState(() => _messages.add({'role': 'assistant', 'text': resp['text'] ?? resp['response'] ?? ''}));
    } catch (_) {
      setState(() => _messages.add({'role': 'assistant', 'text': 'Service vocal indisponible.'}));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Assistant vocal'),
        actions: [
          DropdownButton<String>(
            value: _language,
            dropdownColor: Colors.white,
            items: const [
              DropdownMenuItem(value: 'fr', child: Text('FR')),
              DropdownMenuItem(value: 'en', child: Text('EN')),
              DropdownMenuItem(value: 'sw', child: Text('SW')),
              DropdownMenuItem(value: 'bm', child: Text('BM')),
            ],
            onChanged: (v) => setState(() => _language = v!),
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: _messages.length,
              itemBuilder: (_, i) {
                final m = _messages[i];
                final isUser = m['role'] == 'user';
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 4),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: isUser ? AppTheme.primaryGreen.withValues(alpha: 0.1) : AppTheme.climateBlue.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(m['text'] ?? ''),
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8),
            child: Row(children: [
              Expanded(child: TextField(controller: _controller, decoration: const InputDecoration(hintText: 'Posez votre question...'))),
              IconButton(onPressed: _ask, icon: const Icon(Icons.mic, color: AppTheme.primaryGreen)),
            ]),
          ),
        ],
      ),
    );
  }
}
