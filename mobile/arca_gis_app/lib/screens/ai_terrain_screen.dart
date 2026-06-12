import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../config/theme.dart';
import '../services/api_service.dart';
import '../utils/api_utils.dart';

/// Hub IA terrain v7.6 : conseiller, diagnostic photo, planificateur vocal.
class AiTerrainScreen extends StatefulWidget {
  const AiTerrainScreen({super.key});

  @override
  State<AiTerrainScreen> createState() => _AiTerrainScreenState();
}

class _AiTerrainScreenState extends State<AiTerrainScreen> with SingleTickerProviderStateMixin {
  late TabController _tabs;

  @override
  void initState() {
    super.initState();
    _tabs = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabs.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('IA terrain'),
        backgroundColor: AppTheme.primaryGreen,
        bottom: TabBar(
          controller: _tabs,
          indicatorColor: Colors.white,
          labelColor: Colors.white,
          unselectedLabelColor: Colors.white70,
          tabs: const [
            Tab(icon: Icon(Icons.chat), text: 'Conseiller'),
            Tab(icon: Icon(Icons.biotech), text: 'Diagnostic'),
            Tab(icon: Icon(Icons.calendar_month), text: 'Planificateur'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabs,
        children: const [
          _AdvisorTab(),
          _DiseaseTab(),
          _PlannerTab(),
        ],
      ),
    );
  }
}

class _AdvisorTab extends StatefulWidget {
  const _AdvisorTab();

  @override
  State<_AdvisorTab> createState() => _AdvisorTabState();
}

class _AdvisorTabState extends State<_AdvisorTab> {
  final _api = ApiService();
  final _controller = TextEditingController();
  final List<Map<String, String>> _messages = [];
  int? _parcelId;
  List<Map<String, dynamic>> _parcels = [];
  bool _loading = false;

  @override
  void initState() {
    super.initState();
    _loadParcels();
  }

  Future<void> _loadParcels() async {
    try {
      final data = await _api.get('/parcels/');
      setState(() => _parcels = parseApiList(data['results'] ?? data).cast<Map<String, dynamic>>());
    } catch (_) {}
  }

  Future<void> _send() async {
    final query = _controller.text.trim();
    if (query.isEmpty || _loading) return;
    setState(() {
      _messages.add({'role': 'user', 'text': query});
      _loading = true;
    });
    _controller.clear();
    try {
      final body = <String, dynamic>{'query': query, 'language': 'fr'};
      if (_parcelId != null) body['parcel_id'] = _parcelId;
      final resp = await _api.post('/ai/chat/', body);
      setState(() => _messages.add({'role': 'assistant', 'text': resp['response']?.toString() ?? ''}));
    } catch (_) {
      setState(() => _messages.add({'role': 'assistant', 'text': 'Conseiller indisponible.'}));
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(children: [
      if (_parcels.isNotEmpty)
        SizedBox(
          height: 44,
          child: ListView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            children: [
              Padding(
                padding: const EdgeInsets.only(right: 8),
                child: ChoiceChip(
                  label: const Text('Toutes'),
                  selected: _parcelId == null,
                  onSelected: (_) => setState(() => _parcelId = null),
                ),
              ),
              ..._parcels.map((p) => Padding(
                padding: const EdgeInsets.only(right: 8),
                child: ChoiceChip(
                  label: Text(p['name']?.toString() ?? 'Parcelle'),
                  selected: _parcelId == p['id'],
                  onSelected: (_) => setState(() => _parcelId = p['id'] as int?),
                ),
              )),
            ],
          ),
        ),
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
                constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.8),
                decoration: BoxDecoration(
                  color: isUser ? AppTheme.primaryGreen.withValues(alpha: 0.12) : AppTheme.climateBlue.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(m['text'] ?? ''),
              ),
            );
          },
        ),
      ),
      if (_loading) const LinearProgressIndicator(minHeight: 2),
      Padding(
        padding: const EdgeInsets.all(8),
        child: Row(children: [
          Expanded(child: TextField(
            controller: _controller,
            decoration: const InputDecoration(hintText: 'Question agricole...', isDense: true),
            onSubmitted: (_) => _send(),
          )),
          IconButton(onPressed: _send, icon: const Icon(Icons.send, color: AppTheme.primaryGreen)),
        ]),
      ),
    ]);
  }
}

class _DiseaseTab extends StatefulWidget {
  const _DiseaseTab();

  @override
  State<_DiseaseTab> createState() => _DiseaseTabState();
}

class _DiseaseTabState extends State<_DiseaseTab> {
  final _api = ApiService();
  final _picker = ImagePicker();
  Map<String, dynamic>? _result;
  bool _analyzing = false;
  String _crop = 'maize';

  Future<void> _pickAndAnalyze(ImageSource source) async {
    final image = await _picker.pickImage(source: source, maxWidth: 1024, imageQuality: 85);
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

  Color _severityColor(String? s) {
    switch (s) {
      case 'critical': return Colors.red.shade900;
      case 'high': return Colors.red;
      case 'medium': return Colors.orange;
      default: return AppTheme.primaryGreen;
    }
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        DropdownButtonFormField<String>(
          initialValue: _crop,
          decoration: const InputDecoration(labelText: 'Culture', border: OutlineInputBorder()),
          items: const [
            DropdownMenuItem(value: 'maize', child: Text('Maïs')),
            DropdownMenuItem(value: 'rice', child: Text('Riz')),
            DropdownMenuItem(value: 'cassava', child: Text('Manioc')),
          ],
          onChanged: (v) => setState(() => _crop = v ?? 'maize'),
        ),
        const SizedBox(height: 16),
        Row(children: [
          Expanded(child: ElevatedButton.icon(
            onPressed: _analyzing ? null : () => _pickAndAnalyze(ImageSource.camera),
            icon: const Icon(Icons.camera_alt),
            label: Text(_analyzing ? 'Analyse...' : 'Caméra'),
            style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGreen, foregroundColor: Colors.white, minimumSize: const Size(0, 48)),
          )),
          const SizedBox(width: 12),
          Expanded(child: OutlinedButton.icon(
            onPressed: _analyzing ? null : () => _pickAndAnalyze(ImageSource.gallery),
            icon: const Icon(Icons.photo_library),
            label: const Text('Galerie'),
            style: OutlinedButton.styleFrom(minimumSize: const Size(0, 48)),
          )),
        ]),
        const SizedBox(height: 24),
        if (_result != null) ...[
          if (_result!['error'] != null)
            Text(_result!['error'].toString(), style: const TextStyle(color: Colors.red))
          else ...[
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Row(children: [
                    Icon(Icons.biotech, color: _severityColor(_result!['diagnosis']?['severity']?.toString())),
                    const SizedBox(width: 8),
                    Expanded(child: Text(
                      _result!['diagnosis']?['name']?.toString() ?? 'Diagnostic',
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    )),
                  ]),
                  const SizedBox(height: 8),
                  Text('Confiance: ${(((_result!['confidence'] as num?) ?? 0) * 100).toInt()}%'),
                  const SizedBox(height: 8),
                  Text('Traitement: ${_result!['treatment']}'),
                  if (_result!['prevention'] != null) ...[
                    const SizedBox(height: 8),
                    Text('Prévention: ${_result!['prevention']}', style: TextStyle(color: Colors.grey.shade700, fontSize: 13)),
                  ],
                ]),
              ),
            ),
          ],
        ],
      ],
    );
  }
}

class _PlannerTab extends StatefulWidget {
  const _PlannerTab();

  @override
  State<_PlannerTab> createState() => _PlannerTabState();
}

class _PlannerTabState extends State<_PlannerTab> {
  final _api = ApiService();
  final _voiceController = TextEditingController();
  Map<String, dynamic> _plan = {};
  bool _loading = true;
  String? _voiceStatus;

  @override
  void initState() {
    super.initState();
    _loadPlan();
  }

  Future<void> _loadPlan() async {
    setState(() => _loading = true);
    try {
      final data = await _api.get('/ai/planner/');
      setState(() { _plan = parseApiMap(data); _loading = false; });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  Future<void> _saveVoiceJournal() async {
    final text = _voiceController.text.trim();
    if (text.isEmpty) return;
    setState(() => _voiceStatus = 'Enregistrement...');
    try {
      final resp = await _api.post('/ai/voice-journal/', {'text': text, 'save': true});
      setState(() {
        _voiceStatus = resp['saved'] == true ? 'Journal enregistré ✓' : 'Transcrit';
        _voiceController.clear();
      });
    } catch (e) {
      setState(() => _voiceStatus = 'Erreur: $e');
    }
  }

  Color _priorityColor(String? p) {
    switch (p) {
      case 'high': return AppTheme.sosRed;
      case 'medium': return AppTheme.accentOrange;
      default: return AppTheme.climateBlue;
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const Center(child: CircularProgressIndicator());
    final parcelPlans = parseApiList(_plan['parcel_plans']);
    final tasks = parseApiList(_plan['pending_tasks']);

    return RefreshIndicator(
      onRefresh: _loadPlan,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(_plan['summary']?.toString() ?? '', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          Text('Semaine du ${_plan['week_start']} au ${_plan['week_end']}', style: TextStyle(color: Colors.grey.shade600, fontSize: 12)),
          const SizedBox(height: 16),
          const Text('Actions IA par parcelle', style: TextStyle(fontWeight: FontWeight.w600)),
          ...parcelPlans.map((pp) {
            final m = pp as Map<String, dynamic>;
            final actions = parseApiList(m['actions']);
            return Card(
              margin: const EdgeInsets.symmetric(vertical: 6),
              child: ExpansionTile(
                title: Text(m['parcel_name']?.toString() ?? 'Parcelle'),
                subtitle: Text('${m['crop']} — humidité ${m['moisture']}%'),
                children: actions.map((a) {
                  final act = a as Map<String, dynamic>;
                  return ListTile(
                    dense: true,
                    leading: Icon(Icons.task_alt, color: _priorityColor(act['priority']?.toString()), size: 20),
                    title: Text(act['label']?.toString() ?? act['action']?.toString() ?? ''),
                    subtitle: Text('${act['when']} • ${act['priority']}'),
                  );
                }).toList(),
              ),
            );
          }),
          const SizedBox(height: 16),
          const Text('Tâches en attente', style: TextStyle(fontWeight: FontWeight.w600)),
          if (tasks.isEmpty)
            const Padding(padding: EdgeInsets.all(8), child: Text('Aucune tâche cette semaine'))
          else
            ...tasks.map((t) {
              final task = t as Map<String, dynamic>;
              return ListTile(
                leading: const Icon(Icons.check_circle_outline),
                title: Text(task['title']?.toString() ?? ''),
                subtitle: Text('${task['due_date']} ${task['parcel'] != null ? "• ${task['parcel']}" : ""}'),
              );
            }),
          const Divider(height: 32),
          const Text('Journal vocal', style: TextStyle(fontWeight: FontWeight.w600)),
          const SizedBox(height: 8),
          TextField(
            controller: _voiceController,
            maxLines: 3,
            decoration: const InputDecoration(
              hintText: 'Dictez ou tapez une observation de terrain...',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 8),
          ElevatedButton.icon(
            onPressed: _saveVoiceJournal,
            icon: const Icon(Icons.mic),
            label: const Text('Enregistrer au journal'),
            style: ElevatedButton.styleFrom(backgroundColor: AppTheme.climateBlue, foregroundColor: Colors.white),
          ),
          if (_voiceStatus != null) Padding(
            padding: const EdgeInsets.only(top: 8),
            child: Text(_voiceStatus!, style: TextStyle(color: AppTheme.primaryGreen)),
          ),
        ],
      ),
    );
  }
}
