import 'package:flutter/material.dart';
import '../config/theme.dart';
import '../services/api_service.dart';

class QuizScreen extends StatefulWidget {
  const QuizScreen({super.key});
  @override
  State<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  final _api = ApiService();
  Map<String, dynamic>? _quiz;
  final Map<String, int> _answers = {};
  String? _result;

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    try {
      final data = await _api.get('/training/quizzes/1/');
      setState(() => _quiz = data is Map<String, dynamic> ? data : null);
    } catch (_) {}
  }

  Future<void> _submit() async {
    if (_quiz == null) return;
    final r = await _api.post('/training/quizzes/${_quiz!['id']}/submit/', {
      'answers': _answers.map((k, v) => MapEntry(k, v)),
    });
    setState(() {
      _result = 'Score: ${r['score']}% — ${r['passed'] == true ? 'Réussi' : 'Échoué'}';
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_quiz == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('Quiz formation'), backgroundColor: AppTheme.primaryGreen),
        body: const Center(child: Text('Aucun quiz disponible')),
      );
    }
    final questions = (_quiz!['questions'] as List?) ?? [];
    return Scaffold(
      appBar: AppBar(title: Text(_quiz!['title']?.toString() ?? 'Quiz'), backgroundColor: AppTheme.primaryGreen),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (_result != null) Text(_result!, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ...questions.map((q) {
            final qm = q as Map<String, dynamic>;
            final opts = (qm['options'] as List?)?.cast<String>() ?? [];
            final qid = qm['id'].toString();
            return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(qm['question']?.toString() ?? '', style: const TextStyle(fontWeight: FontWeight.w600)),
              RadioGroup<int>(
                groupValue: _answers[qid],
                onChanged: (v) => setState(() => _answers[qid] = v!),
                child: Column(
                  children: List.generate(
                    opts.length,
                    (i) => RadioListTile<int>(value: i, title: Text(opts[i])),
                  ),
                ),
              ),
              const Divider(),
            ]);
          }),
          ElevatedButton(onPressed: _submit, child: const Text('Valider')),
        ],
      ),
    );
  }
}
