import 'package:flutter/material.dart';
import '../config/theme.dart';

class SOSButton extends StatefulWidget {
  final VoidCallback onPressed;
  final bool isLoading;

  const SOSButton({super.key, required this.onPressed, this.isLoading = false});

  @override
  State<SOSButton> createState() => _SOSButtonState();
}

class _SOSButtonState extends State<SOSButton> with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _pulseController,
      builder: (context, child) {
        return Container(
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(
                color: AppTheme.sosRed.withValues(alpha: 0.3 + _pulseController.value * 0.3),
                blurRadius: 12 + _pulseController.value * 8,
                spreadRadius: 2 + _pulseController.value * 4,
              ),
            ],
          ),
          child: child,
        );
      },
      child: FloatingActionButton.large(
        onPressed: widget.isLoading ? null : () => _confirmSOS(context),
        backgroundColor: AppTheme.sosRed,
        child: widget.isLoading
            ? const CircularProgressIndicator(color: Colors.white)
            : const Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.sos, size: 32),
                  Text('SOS', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                ],
              ),
      ),
    );
  }

  void _confirmSOS(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        icon: const Icon(Icons.warning_amber_rounded, color: AppTheme.sosRed, size: 48),
        title: const Text('Déclencher SOS'),
        content: const Text(
          'Vous allez signaler une urgence à votre position actuelle. '
          'Les équipes de secours seront alertées immédiatement.',
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Annuler')),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(ctx);
              widget.onPressed();
            },
            style: ElevatedButton.styleFrom(backgroundColor: AppTheme.sosRed),
            child: const Text('Confirmer SOS'),
          ),
        ],
      ),
    );
  }
}
