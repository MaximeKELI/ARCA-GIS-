import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/chat_service.dart';

class ChatScreen extends StatefulWidget {
  final int incidentId;
  final String incidentTitle;

  const ChatScreen({super.key, required this.incidentId, required this.incidentTitle});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final ChatService _chat = ChatService();
  final _controller = TextEditingController();
  final List<ChatMessage> _messages = [];

  @override
  void initState() {
    super.initState();
    _init();
  }

  Future<void> _init() async {
    final history = await _chat.loadHistory(widget.incidentId);
    setState(() => _messages.addAll(history));
    await _chat.connect(widget.incidentId);
    _chat.messageStream.listen((msg) {
      setState(() => _messages.add(msg));
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    _chat.dispose();
    super.dispose();
  }

  void _send() {
    final text = _controller.text.trim();
    if (text.isEmpty) return;
    _chat.sendMessage(text);
    _controller.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Chat — ${widget.incidentTitle}')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: _messages.length,
              itemBuilder: (ctx, i) {
                final msg = _messages[i];
                final isRescue = msg.senderRole == 'rescue';
                return Align(
                  alignment: isRescue ? Alignment.centerLeft : Alignment.centerRight,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 4),
                    padding: const EdgeInsets.all(12),
                    constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
                    decoration: BoxDecoration(
                      color: isRescue ? AppTheme.climateBlue.withValues(alpha: 0.1) : AppTheme.primaryGreen.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(msg.senderName, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 12)),
                        Text(msg.message),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(hintText: 'Votre message...'),
                    onSubmitted: (_) => _send(),
                  ),
                ),
                IconButton(onPressed: _send, icon: const Icon(Icons.send, color: AppTheme.primaryGreen)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
