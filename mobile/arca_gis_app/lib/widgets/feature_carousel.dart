import 'dart:async';
import 'package:flutter/material.dart';
import '../config/app_config.dart';
import 'arca_logo.dart';

class CarouselSlide {
  final String title;
  final String subtitle;
  final IconData icon;
  final List<Color> gradient;

  const CarouselSlide({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.gradient,
  });
}

/// Carrousel auto-défilant avec logo ARCA-GIS.
class FeatureCarousel extends StatefulWidget {
  final double height;
  final bool compact;
  final VoidCallback? onDismiss;

  const FeatureCarousel({
    super.key,
    this.height = 160,
    this.compact = false,
    this.onDismiss,
  });

  @override
  State<FeatureCarousel> createState() => _FeatureCarouselState();
}

class _FeatureCarouselState extends State<FeatureCarousel> {
  static const _slides = [
    CarouselSlide(
      title: 'Agriculture intelligente',
      subtitle: 'Parcelles, récoltes, calendrier cultural & IA terrain',
      icon: Icons.agriculture,
      gradient: [Color(0xFF1B5E20), Color(0xFF43A047)],
    ),
    CarouselSlide(
      title: 'SOS & secours',
      subtitle: 'Urgence GPS, alertes temps réel, refuges & radio HF',
      icon: Icons.emergency,
      gradient: [Color(0xFFB71C1C), Color(0xFFE53935)],
    ),
    CarouselSlide(
      title: 'Climat & résilience',
      subtitle: 'Prévisions, sécheresse 90j, simulation inondation',
      icon: Icons.cloud,
      gradient: [Color(0xFF0D47A1), Color(0xFF42A5F5)],
    ),
    CarouselSlide(
      title: 'Coop & formation',
      subtitle: 'Votes coop, quiz certifiants, crédits carbone',
      icon: Icons.groups,
      gradient: [Color(0xFFE65100), Color(0xFFFFB300)],
    ),
  ];

  final _controller = PageController();
  int _index = 0;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 4), (_) {
      if (!mounted || !_controller.hasClients) return;
      final next = (_index + 1) % _slides.length;
      _controller.animateToPage(next, duration: const Duration(milliseconds: 450), curve: Curves.easeInOut);
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: widget.height,
      child: Stack(
        children: [
          PageView.builder(
            controller: _controller,
            onPageChanged: (i) => setState(() => _index = i),
            itemCount: _slides.length,
            itemBuilder: (_, i) => _SlideCard(slide: _slides[i], compact: widget.compact),
          ),
          if (widget.onDismiss != null)
            Positioned(
              top: 4,
              right: 4,
              child: IconButton(
                icon: const Icon(Icons.close, color: Colors.white70, size: 20),
                onPressed: widget.onDismiss,
                tooltip: 'Masquer',
              ),
            ),
          Positioned(
            bottom: 10,
            left: 0,
            right: 0,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(_slides.length, (i) {
                final active = i == _index;
                return AnimatedContainer(
                  duration: const Duration(milliseconds: 250),
                  margin: const EdgeInsets.symmetric(horizontal: 3),
                  width: active ? 18 : 6,
                  height: 6,
                  decoration: BoxDecoration(
                    color: active ? Colors.white : Colors.white.withValues(alpha: 0.45),
                    borderRadius: BorderRadius.circular(3),
                  ),
                );
              }),
            ),
          ),
        ],
      ),
    );
  }
}

class _SlideCard extends StatelessWidget {
  final CarouselSlide slide;
  final bool compact;

  const _SlideCard({required this.slide, required this.compact});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(16),
        gradient: LinearGradient(begin: Alignment.topLeft, end: Alignment.bottomRight, colors: slide.gradient),
        boxShadow: [
          BoxShadow(color: slide.gradient.first.withValues(alpha: 0.35), blurRadius: 12, offset: const Offset(0, 4)),
        ],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(16),
        child: Stack(
          children: [
            Positioned(
              right: -16,
              bottom: -16,
              child: Icon(slide.icon, size: compact ? 80 : 100, color: Colors.white.withValues(alpha: 0.12)),
            ),
            Padding(
              padding: EdgeInsets.fromLTRB(compact ? 14 : 18, compact ? 12 : 16, compact ? 14 : 18, compact ? 24 : 28),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (!compact)
                    Padding(
                      padding: const EdgeInsets.only(right: 12, top: 2),
                      child: ArcaLogo(size: 44, showText: false, onDark: true),
                    ),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(children: [
                          Icon(slide.icon, color: Colors.white, size: compact ? 18 : 22),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              slide.title,
                              style: TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                                fontSize: compact ? 14 : 16,
                              ),
                            ),
                          ),
                        ]),
                        SizedBox(height: compact ? 4 : 8),
                        Text(
                          slide.subtitle,
                          style: TextStyle(
                            color: Colors.white.withValues(alpha: 0.9),
                            fontSize: compact ? 11 : 12,
                            height: 1.35,
                          ),
                          maxLines: compact ? 2 : 3,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
