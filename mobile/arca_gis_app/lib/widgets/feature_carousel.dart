import 'dart:async';
import 'package:flutter/material.dart';
import '../config/assets.dart';

class CarouselSlide {
  final String title;
  final String subtitle;
  final IconData icon;
  final String imageAsset;
  final List<Color> gradient;

  const CarouselSlide({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.imageAsset,
    required this.gradient,
  });
}

/// Carrousel auto-défilant avec images générées + logo ARCA-GIS.
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
      imageAsset: AppAssets.carouselAgriculture,
      gradient: [Color(0xFF1B5E20), Color(0xFF43A047)],
    ),
    CarouselSlide(
      title: 'SOS & secours',
      subtitle: 'Urgence GPS, alertes temps réel, refuges & radio HF',
      icon: Icons.emergency,
      imageAsset: AppAssets.carouselSos,
      gradient: [Color(0xFFB71C1C), Color(0xFFE53935)],
    ),
    CarouselSlide(
      title: 'Climat & météo',
      subtitle: 'Prévisions, sécheresse 90j, simulation inondation',
      icon: Icons.cloud,
      imageAsset: AppAssets.carouselClimate,
      gradient: [Color(0xFF0D47A1), Color(0xFF42A5F5)],
    ),
    CarouselSlide(
      title: 'Coopératives',
      subtitle: 'Votes, réservations équipement, annuaire membres',
      icon: Icons.groups,
      imageAsset: AppAssets.carouselCoop,
      gradient: [Color(0xFFE65100), Color(0xFFFFB300)],
    ),
    CarouselSlide(
      title: 'IA terrain',
      subtitle: 'Conseiller contextuel, diagnostic photo, planificateur',
      icon: Icons.psychology,
      imageAsset: AppAssets.carouselIa,
      gradient: [Color(0xFF00695C), Color(0xFF26A69A)],
    ),
    CarouselSlide(
      title: 'Analytiques',
      subtitle: 'KPIs, heatmap, Sankey budget, comparaison saisons',
      icon: Icons.bar_chart,
      imageAsset: AppAssets.carouselAnalytics,
      gradient: [Color(0xFF4A148C), Color(0xFF7B1FA2)],
    ),
    CarouselSlide(
      title: 'Carbone & traçabilité',
      subtitle: 'Crédits CO₂, QR parcelle, chaîne de valeur',
      icon: Icons.eco,
      imageAsset: AppAssets.carouselCarbon,
      gradient: [Color(0xFF1B5E20), Color(0xFF66BB6A)],
    ),
    CarouselSlide(
      title: 'Formation',
      subtitle: 'Quiz certifiants, cours, badges & mentorat',
      icon: Icons.school,
      imageAsset: AppAssets.carouselTraining,
      gradient: [Color(0xFF1565C0), Color(0xFF42A5F5)],
    ),
    CarouselSlide(
      title: 'Gestion de l\'eau',
      subtitle: 'Irrigation, bassins, puits & ressources hydriques',
      icon: Icons.water_drop,
      imageAsset: AppAssets.carouselWater,
      gradient: [Color(0xFF01579B), Color(0xFF29B6F6)],
    ),
    CarouselSlide(
      title: 'Marchés & prix',
      subtitle: 'Prix en temps réel, enchères live, comparateur',
      icon: Icons.store,
      imageAsset: AppAssets.carouselMarket,
      gradient: [Color(0xFFBF360C), Color(0xFFFF7043)],
    ),
    CarouselSlide(
      title: 'Résilience',
      subtitle: 'Refuges, EWS, mode catastrophe & radio HF',
      icon: Icons.shield,
      imageAsset: AppAssets.carouselResilience,
      gradient: [Color(0xFF37474F), Color(0xFF78909C)],
    ),
    CarouselSlide(
      title: 'Élevage & apiculture',
      subtitle: 'Bétail, ruches, aquaculture & semencier',
      icon: Icons.pets,
      imageAsset: AppAssets.carouselLivestock,
      gradient: [Color(0xFF5D4037), Color(0xFF8D6E63)],
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
              right: 16,
              child: Material(
                color: Colors.black38,
                shape: const CircleBorder(),
                child: IconButton(
                  icon: const Icon(Icons.close, color: Colors.white, size: 18),
                  onPressed: widget.onDismiss,
                  tooltip: 'Masquer',
                ),
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
                    boxShadow: active ? [const BoxShadow(color: Colors.black26, blurRadius: 4)] : null,
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
        boxShadow: [
          BoxShadow(color: slide.gradient.first.withValues(alpha: 0.4), blurRadius: 14, offset: const Offset(0, 5)),
        ],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(16),
        child: Stack(
          fit: StackFit.expand,
          children: [
            Image.asset(
              slide.imageAsset,
              fit: BoxFit.cover,
              errorBuilder: (_, __, ___) => DecoratedBox(
                decoration: BoxDecoration(
                  gradient: LinearGradient(colors: slide.gradient),
                ),
              ),
            ),
            DecoratedBox(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.centerLeft,
                  end: Alignment.centerRight,
                  colors: [
                    Colors.black.withValues(alpha: 0.78),
                    Colors.black.withValues(alpha: 0.45),
                    Colors.black.withValues(alpha: 0.15),
                  ],
                  stops: const [0.0, 0.55, 1.0],
                ),
              ),
            ),
            Padding(
              padding: EdgeInsets.fromLTRB(compact ? 14 : 18, compact ? 12 : 16, compact ? 14 : 18, compact ? 28 : 32),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (!compact)
                    Padding(
                      padding: const EdgeInsets.only(right: 10, top: 2),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(10),
                        child: Image.asset(AppAssets.logo, width: 42, height: 42, fit: BoxFit.cover),
                      ),
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
                                shadows: const [Shadow(color: Colors.black45, blurRadius: 6)],
                              ),
                            ),
                          ),
                        ]),
                        SizedBox(height: compact ? 4 : 8),
                        Text(
                          slide.subtitle,
                          style: TextStyle(
                            color: Colors.white.withValues(alpha: 0.95),
                            fontSize: compact ? 11 : 12,
                            height: 1.35,
                            shadows: const [Shadow(color: Colors.black38, blurRadius: 4)],
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
