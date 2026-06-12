import 'package:flutter/material.dart';

/// Compteur animé pour KPIs (effet count-up).
class AnimatedCount extends StatelessWidget {
  final num value;
  final TextStyle? style;
  final String suffix;
  final Duration duration;

  const AnimatedCount({
    super.key,
    required this.value,
    this.style,
    this.suffix = '',
    this.duration = const Duration(milliseconds: 800),
  });

  @override
  Widget build(BuildContext context) {
    return TweenAnimationBuilder<double>(
      tween: Tween(begin: 0, end: value.toDouble()),
      duration: duration,
      curve: Curves.easeOutCubic,
      builder: (context, v, child) => Text(
        '${v == v.roundToDouble() ? v.toInt() : v.toStringAsFixed(1)}$suffix',
        style: style,
      ),
    );
  }
}
