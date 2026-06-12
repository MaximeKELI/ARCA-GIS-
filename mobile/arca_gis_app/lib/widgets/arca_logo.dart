import 'dart:math' as math;
import 'package:flutter/material.dart';
import '../config/theme.dart';

/// Logo ARCA-GIS vectoriel (Afrique + feuille + pin GPS).
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
        SizedBox(
          width: size,
          height: size,
          child: CustomPaint(
            painter: _ArcaLogoPainter(fg: fg, onDark: onDark),
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
    _drawPin(canvas, size, AppTheme.sosRed);
  }

  void _drawAfrica(Canvas canvas, Size size, Color color) {
    final path = Path()
      ..moveTo(size.width * 0.38, size.height * 0.28)
      ..quadraticBezierTo(size.width * 0.52, size.height * 0.22, size.width * 0.62, size.height * 0.32)
      ..quadraticBezierTo(size.width * 0.72, size.height * 0.38, size.width * 0.68, size.height * 0.48)
      ..quadraticBezierTo(size.width * 0.74, size.height * 0.58, size.width * 0.65, size.height * 0.62)
      ..quadraticBezierTo(size.width * 0.58, size.height * 0.72, size.width * 0.48, size.height * 0.68)
      ..quadraticBezierTo(size.width * 0.38, size.height * 0.74, size.width * 0.34, size.height * 0.62)
      ..quadraticBezierTo(size.width * 0.28, size.height * 0.52, size.width * 0.32, size.height * 0.42)
      ..close();
    canvas.drawPath(path, Paint()..color = color.withValues(alpha: 0.85));
  }

  void _drawLeaf(Canvas canvas, Size size, Color color) {
    final leaf = Path()
      ..moveTo(size.width * 0.52, size.height * 0.44)
      ..quadraticBezierTo(size.width * 0.58, size.height * 0.36, size.width * 0.54, size.height * 0.52)
      ..quadraticBezierTo(size.width * 0.46, size.height * 0.56, size.width * 0.52, size.height * 0.44);
    canvas.drawPath(leaf, Paint()..color = AppTheme.accentOrange.withValues(alpha: 0.9));
    canvas.drawLine(
      Offset(size.width * 0.52, size.height * 0.44),
      Offset(size.width * 0.50, size.height * 0.54),
      Paint()
        ..color = color.withValues(alpha: 0.6)
        ..strokeWidth = size.width * 0.012,
    );
  }

  void _drawPin(Canvas canvas, Size size, Color color) {
    final px = size.width * 0.56;
    final py = size.height * 0.40;
    final pinR = size.width * 0.055;
    canvas.drawCircle(Offset(px, py), pinR, Paint()..color = color);
    canvas.drawCircle(Offset(px, py), pinR * 0.4, Paint()..color = Colors.white);
    final tail = Path()
      ..moveTo(px, py + pinR)
      ..lineTo(px - pinR * 0.6, py + pinR * 2.2)
      ..lineTo(px + pinR * 0.6, py + pinR * 2.2)
      ..close();
    canvas.drawPath(tail, Paint()..color = color);
  }

  @override
  bool shouldRepaint(covariant _ArcaLogoPainter old) => old.fg != fg || old.onDark != onDark;
}

/// En-tête drawer avec logo.
class ArcaDrawerHeader extends StatelessWidget {
  const ArcaDrawerHeader({super.key});

  @override
  Widget build(BuildContext context) {
    return DrawerHeader(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [AppTheme.primaryDark, AppTheme.primaryGreen],
        ),
      ),
      child: Stack(
        children: [
          Positioned(
            right: -20,
            top: -10,
            child: Transform.rotate(
              angle: math.pi / 8,
              child: Opacity(
                opacity: 0.08,
                child: ArcaLogo(size: 120, showText: false, onDark: true),
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
