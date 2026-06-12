import 'dart:math';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import '../config/theme.dart';

class ModernCharts {
  static List<Color> get palette => [
    AppTheme.primaryGreen,
    AppTheme.climateBlue,
    AppTheme.accentOrange,
    const Color(0xFF6A1B9A),
    const Color(0xFF00838F),
    AppTheme.sosRed,
    const Color(0xFF4527A0),
    const Color(0xFFEF6C00),
  ];

  static Widget kpiCard({
    required String label,
    required String value,
    required String unit,
    required Color color,
    required IconData icon,
    double? delta,
    List<double>? sparkline,
  }) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(20),
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [color.withValues(alpha: 0.15), color.withValues(alpha: 0.05)],
        ),
        border: Border.all(color: color.withValues(alpha: 0.2)),
      ),
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(color: color.withValues(alpha: 0.2), borderRadius: BorderRadius.circular(12)),
            child: Icon(icon, color: color, size: 20),
          ),
          const Spacer(),
          if (delta != null)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(
                color: (delta >= 0 ? Colors.green : Colors.red).withValues(alpha: 0.15),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(mainAxisSize: MainAxisSize.min, children: [
                Icon(delta >= 0 ? Icons.trending_up : Icons.trending_down,
                    size: 14, color: delta >= 0 ? Colors.green : Colors.red),
                Text('${delta.abs()}%', style: TextStyle(fontSize: 11, color: delta >= 0 ? Colors.green : Colors.red)),
              ]),
            ),
        ]),
        const SizedBox(height: 12),
        Text(label, style: TextStyle(color: Colors.grey.shade600, fontSize: 12)),
        const SizedBox(height: 4),
        Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
          Text(value, style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: color)),
          if (unit.isNotEmpty) ...[
            const SizedBox(width: 4),
            Padding(
              padding: const EdgeInsets.only(bottom: 3),
              child: Text(unit, style: TextStyle(fontSize: 12, color: Colors.grey.shade500)),
            ),
          ],
        ]),
        if (sparkline != null && sparkline.isNotEmpty) ...[
          const SizedBox(height: 8),
          SizedBox(height: 32, child: sparklineChart(sparkline, color)),
        ],
      ]),
    );
  }

  static Widget sparklineChart(List<double> data, Color color) {
    if (data.isEmpty) return const SizedBox();
    final maxV = data.reduce(max);
    final minV = data.reduce(min);
    final range = max(maxV - minV, 1.0);
    return LineChart(LineChartData(
      gridData: const FlGridData(show: false),
      titlesData: const FlTitlesData(show: false),
      borderData: FlBorderData(show: false),
      lineTouchData: const LineTouchData(enabled: false),
      lineBarsData: [LineChartBarData(
        spots: data.asMap().entries.map((e) => FlSpot(e.key.toDouble(), (e.value - minV) / range)).toList(),
        isCurved: true,
        color: color,
        barWidth: 2,
        dotData: const FlDotData(show: false),
        belowBarData: BarAreaData(show: true, color: color.withValues(alpha: 0.15)),
      )],
    ));
  }

  static Widget gradientLineChart({
    required List<Map<String, dynamic>> data,
    required Color color,
    required String title,
    String valueSuffix = '',
  }) {
    final spots = data.asMap().entries.map((e) =>
      FlSpot(e.key.toDouble(), (e.value['value'] as num?)?.toDouble() ?? 0)).toList();
    return _chartCard(title, color, SizedBox(
      height: 220,
      child: LineChart(LineChartData(
        gridData: FlGridData(show: true, drawVerticalLine: false,
            getDrawingHorizontalLine: (v) => FlLine(color: Colors.grey.withValues(alpha: 0.15), strokeWidth: 1)),
        titlesData: FlTitlesData(
          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 40,
              getTitlesWidget: (v, _) => Text('${v.toInt()}$valueSuffix', style: const TextStyle(fontSize: 10)))),
          bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true,
              getTitlesWidget: (v, meta) {
                final i = v.toInt();
                if (i < 0 || i >= data.length) return const SizedBox();
                return Padding(
                  padding: const EdgeInsets.only(top: 8),
                  child: Text(data[i]['label']?.toString() ?? '', style: const TextStyle(fontSize: 10)),
                );
              })),
        ),
        borderData: FlBorderData(show: false),
        lineBarsData: [LineChartBarData(
          spots: spots,
          isCurved: true,
          curveSmoothness: 0.35,
          color: color,
          barWidth: 3,
          dotData: FlDotData(show: true, getDotPainter: (s, p, bar, i) => FlDotCirclePainter(
            radius: 4, color: Colors.white, strokeWidth: 2, strokeColor: color)),
          belowBarData: BarAreaData(show: true, gradient: LinearGradient(
            begin: Alignment.topCenter, end: Alignment.bottomCenter,
            colors: [color.withValues(alpha: 0.35), color.withValues(alpha: 0.02)])),
        )],
      )),
    ));
  }

  static Widget barChart({
    required List<Map<String, dynamic>> data,
    required Color color,
    required String title,
    bool horizontal = false,
  }) {
    return _chartCard(title, color, SizedBox(
      height: 220,
      child: BarChart(BarChartData(
        alignment: BarChartAlignment.spaceAround,
        maxY: _maxY(data) * 1.2,
        gridData: FlGridData(show: true, drawVerticalLine: false,
            getDrawingHorizontalLine: (v) => FlLine(color: Colors.grey.withValues(alpha: 0.15), strokeWidth: 1)),
        titlesData: FlTitlesData(
          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 36,
              getTitlesWidget: (v, _) => Text(v.toInt().toString(), style: const TextStyle(fontSize: 10)))),
          bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true,
              getTitlesWidget: (v, meta) {
                final i = v.toInt();
                if (i < 0 || i >= data.length) return const SizedBox();
                return Text(data[i]['label']?.toString() ?? '', style: const TextStyle(fontSize: 9));
              })),
        ),
        borderData: FlBorderData(show: false),
        barGroups: data.asMap().entries.map((e) {
          final val = (e.value['value'] as num?)?.toDouble() ?? 0;
          return BarChartGroupData(x: e.key, barRods: [BarChartRodData(
            toY: val,
            width: horizontal ? 14 : 18,
            borderRadius: const BorderRadius.vertical(top: Radius.circular(6)),
            gradient: LinearGradient(begin: Alignment.bottomCenter, end: Alignment.topCenter,
                colors: [color.withValues(alpha: 0.6), color]),
          )]);
        }).toList(),
      )),
    ));
  }

  static Widget groupedBarChart({
    required List<Map<String, dynamic>> income,
    required List<Map<String, dynamic>> expense,
    required String title,
  }) {
    return _chartCard(title, AppTheme.primaryGreen, SizedBox(
      height: 240,
      child: BarChart(BarChartData(
        alignment: BarChartAlignment.spaceAround,
        maxY: max(_maxY(income), _maxY(expense)) * 1.3,
        gridData: FlGridData(show: true, drawVerticalLine: false,
            getDrawingHorizontalLine: (v) => FlLine(color: Colors.grey.withValues(alpha: 0.15), strokeWidth: 1)),
        titlesData: FlTitlesData(
          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 48,
              getTitlesWidget: (v, _) => Text('${(v / 1000).toInt()}k', style: const TextStyle(fontSize: 10)))),
          bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true,
              getTitlesWidget: (v, meta) {
                final i = v.toInt();
                if (i < 0 || i >= income.length) return const SizedBox();
                return Text(income[i]['label']?.toString() ?? '', style: const TextStyle(fontSize: 10));
              })),
        ),
        borderData: FlBorderData(show: false),
        barGroups: List.generate(income.length, (i) {
          final inc = (income[i]['value'] as num?)?.toDouble() ?? 0;
          final exp = i < expense.length ? (expense[i]['value'] as num?)?.toDouble() ?? 0 : 0.0;
          return BarChartGroupData(x: i, barsSpace: 4, barRods: [
            BarChartRodData(toY: inc, width: 10, color: AppTheme.primaryGreen,
                borderRadius: const BorderRadius.vertical(top: Radius.circular(4))),
            BarChartRodData(toY: exp, width: 10, color: AppTheme.sosRed,
                borderRadius: const BorderRadius.vertical(top: Radius.circular(4))),
          ]);
        }),
      )),
    ));
  }

  static Widget donutChart({
    required List<Map<String, dynamic>> data,
    required String title,
  }) {
    final total = data.fold<double>(0, (s, d) => s + ((d['value'] as num?)?.toDouble() ?? 0));
    if (total == 0) return _chartCard(title, AppTheme.primaryGreen, const Center(child: Text('Aucune donnée')));
    return _chartCard(title, AppTheme.primaryGreen, SizedBox(
      height: 220,
      child: Row(children: [
        Expanded(flex: 3, child: PieChart(PieChartData(
          sectionsSpace: 2,
          centerSpaceRadius: 45,
          sections: data.asMap().entries.map((e) {
            final val = (e.value['value'] as num?)?.toDouble() ?? 0;
            final color = palette[e.key % palette.length];
            return PieChartSectionData(
              value: val, color: color, radius: 50,
              title: '${(val / total * 100).toInt()}%',
              titleStyle: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.white),
            );
          }).toList(),
        ))),
        Expanded(flex: 2, child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: data.asMap().entries.map((e) {
            final color = palette[e.key % palette.length];
            return Padding(
              padding: const EdgeInsets.symmetric(vertical: 3),
              child: Row(children: [
                Container(width: 10, height: 10, decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(3))),
                const SizedBox(width: 6),
                Expanded(child: Text(e.value['name']?.toString() ?? '', style: const TextStyle(fontSize: 11), overflow: TextOverflow.ellipsis)),
              ]),
            );
          }).toList(),
        )),
      ]),
    ));
  }

  static Widget radarChart({
    required List<String> labels,
    required List<double> values,
    required String title,
  }) {
    return _chartCard(title, AppTheme.climateBlue, SizedBox(
      height: 260,
      child: RadarChart(RadarChartData(
        radarShape: RadarShape.polygon,
        tickCount: 4,
        ticksTextStyle: const TextStyle(fontSize: 0),
        radarBorderData: BorderSide(color: Colors.grey.withValues(alpha: 0.2)),
        gridBorderData: BorderSide(color: Colors.grey.withValues(alpha: 0.15)),
        tickBorderData: BorderSide(color: Colors.grey.withValues(alpha: 0.1)),
        getTitle: (i, _) => RadarChartTitle(text: i < labels.length ? labels[i] : '', angle: 0),
        dataSets: [RadarDataSet(
          fillColor: AppTheme.climateBlue.withValues(alpha: 0.25),
          borderColor: AppTheme.climateBlue,
          borderWidth: 2,
          entryRadius: 3,
          dataEntries: values.map((v) => RadarEntry(value: v)).toList(),
        )],
      )),
    ));
  }

  static Widget _chartCard(String title, Color accent, Widget chart) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.06), blurRadius: 16, offset: const Offset(0, 4))],
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 16, 16, 0),
          child: Row(children: [
            Container(width: 4, height: 20, decoration: BoxDecoration(color: accent, borderRadius: BorderRadius.circular(2))),
            const SizedBox(width: 10),
            Text(title, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
          ]),
        ),
        Padding(padding: const EdgeInsets.all(12), child: chart),
      ]),
    );
  }

  static double _maxY(List<Map<String, dynamic>> data) {
    if (data.isEmpty) return 100;
    return data.map((d) => (d['value'] as num?)?.toDouble() ?? 0).reduce(max);
  }

  static IconData iconFromName(String? name) => switch (name) {
    'agriculture' => Icons.agriculture,
    'grass' => Icons.grass,
    'water_drop' => Icons.water_drop,
    'account_balance' => Icons.account_balance,
    'task_alt' => Icons.task_alt,
    'notifications' => Icons.notifications,
    _ => Icons.analytics,
  };

  static Color colorFromHex(String? hex) {
    if (hex == null || hex.length < 7) return AppTheme.primaryGreen;
    return Color(int.parse(hex.replaceFirst('#', '0xFF')));
  }
}
