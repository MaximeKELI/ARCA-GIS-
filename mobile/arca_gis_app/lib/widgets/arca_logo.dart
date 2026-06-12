import 'dart:math' as math;
import 'package:flutter/material.dart';
import '../config/assets.dart';
import '../config/theme.dart';

/// Logo ARCA-GIS — continent africain entier (image + repli vectoriel).
class ArcaLogo extends StatelessWidget {
  final double size;
  final bool showText;
  final Color? foreground;
  final bool onDark;

  const ArcaLogo({
    super.key,
    this.size = 72,
    this.showText = true,
    this.foreground,
    this.onDark = false,
  });

  @override
  Widget build(BuildContext context) {
    final fg = foreground ?? (onDark ? Colors.white : AppTheme.primaryGreen);
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: size,
          height: size,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(size * 0.22),
            boxShadow: onDark
                ? [BoxShadow(color: Colors.black.withValues(alpha: 0.25), blurRadius: 12, offset: const Offset(0, 4))]
                : null,
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(size * 0.22),
            child: Image.asset(
              AppAssets.logo,
              width: size,
              height: size,
              fit: BoxFit.cover,
              errorBuilder: (context, error, stackTrace) => CustomPaint(
                painter: _ArcaLogoPainter(fg: fg, onDark: onDark),
              ),
            ),
          ),
        ),
        if (showText) ...[
          SizedBox(height: size * 0.12),
          Text(
            'ARCA-GIS',
            style: TextStyle(
              fontSize: size * 0.28,
              fontWeight: FontWeight.w800,
              letterSpacing: 1.2,
              color: fg,
            ),
          ),
          Text(
            'Agro · Rescue · Climate',
            style: TextStyle(
              fontSize: size * 0.11,
              letterSpacing: 0.5,
              color: fg.withValues(alpha: 0.75),
            ),
          ),
        ],
      ],
    );
  }
}

class _ArcaLogoPainter extends CustomPainter {
  final Color fg;
  final bool onDark;

  _ArcaLogoPainter({required this.fg, required this.onDark});

  @override
  void paint(Canvas canvas, Size size) {
    final cx = size.width / 2;
    final cy = size.height / 2;
    final r = size.width * 0.46;

    final bg = Paint()
      ..shader = RadialGradient(
        colors: onDark
            ? [Colors.white.withValues(alpha: 0.22), Colors.white.withValues(alpha: 0.05)]
            : [fg.withValues(alpha: 0.18), fg.withValues(alpha: 0.04)],
      ).createShader(Rect.fromCircle(center: Offset(cx, cy), radius: r));
    canvas.drawCircle(Offset(cx, cy), r, bg);

    final ring = Paint()
      ..color = fg.withValues(alpha: 0.35)
      ..style = PaintingStyle.stroke
      ..strokeWidth = size.width * 0.025;
    canvas.drawCircle(Offset(cx, cy), r * 0.92, ring);

    _drawAfrica(canvas, size, fg);
    _drawLeaf(canvas, size, fg);
  }

  void _drawAfrica(Canvas canvas, Size size, Color color) {
    final w = size.width;
    final h = size.height;
    final paint = Paint()..color = color.withValues(alpha: 0.88);

    // Silhouette simplifiée de tout le continent africain
    final path = Path()
      ..moveTo(w * 0.40, h * 0.20)
      ..lineTo(w * 0.56, h * 0.18)
      ..quadraticBezierTo(w * 0.66, h * 0.19, w * 0.72, h * 0.24)
      ..quadraticBezierTo(w * 0.80, h * 0.28, w * 0.78, h * 0.36)
      ..quadraticBezierTo(w * 0.76, h * 0.48, w * 0.72, h * 0.58)
      ..quadraticBezierTo(w * 0.66, h * 0.72, w * 0.54, h * 0.80)
      ..quadraticBezierTo(w * 0.44, h * 0.82, w * 0.36, h * 0.74)
      ..quadraticBezierTo(w * 0.28, h * 0.64, w * 0.30, h * 0.52)
      ..quadraticBezierTo(w * 0.32, h * 0.40, w * 0.36, h * 0.30)
      ..quadraticBezierTo(w * 0.38, h * 0.24, w * 0.40, h * 0.20)
      ..close();
    canvas.drawPath(path, paint);

    // Madagascar
    canvas.drawOval(
      Rect.fromCenter(center: Offset(w * 0.76, h * 0.66), width: w * 0.07, height: h * 0.11),
      Paint()..color = color.withValues(alpha: 0.75),
    );
  }

  void _drawLeaf(Canvas canvas, Size size, Color color) {
    final w = size.width;
    final h = size.height;
    final leaf = Path()
      ..moveTo(w * 0.48, h * 0.46)
      ..quadraticBezierTo(w * 0.54, h * 0.38, w * 0.50, h * 0.54)
      ..quadraticBezierTo(w * 0.42, h * 0.58, w * 0.48, h * 0.46);
    canvas.drawPath(leaf, Paint()..color = AppTheme.accentOrange.withValues(alpha: 0.9));
  }

  @override
  bool shouldRepaint(covariant _ArcaLogoPainter old) => old.fg != fg || old.onDark != onDark;
}

/// En-tête drawer avec logo et image de fond.
class ArcaDrawerHeader extends StatelessWidget {
  const ArcaDrawerHeader({super.key});

  @override
  Widget build(BuildContext context) {
    return DrawerHeader(
      decoration: const BoxDecoration(color: AppTheme.primaryDark),
      child: Stack(
        fit: StackFit.expand,
        children: [
          Image.asset(
            AppAssets.carouselAgriculture,
            fit: BoxFit.cover,
            color: Colors.black.withValues(alpha: 0.55),
            colorBlendMode: BlendMode.darken,
            errorBuilder: (context, error, stackTrace) => const DecoratedBox(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [AppTheme.primaryDark, AppTheme.primaryGreen],
                ),
              ),
            ),
          ),
          Positioned(
            right: -24,
            top: -8,
            child: Transform.rotate(
              angle: math.pi / 10,
              child: Opacity(
                opacity: 0.35,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(20),
                  child: Image.asset(AppAssets.logo, width: 100, height: 100, fit: BoxFit.cover),
                ),
              ),
            ),
          ),
          const Align(
            alignment: Alignment.bottomLeft,
            child: ArcaLogo(size: 64, onDark: true),
          ),
        ],
      ),
    );
  }
}
