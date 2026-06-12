import 'dart:math';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import '../config/theme.dart';
import 'animated_count.dart';

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
    bool isDark = false,
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
        Text(label, style: TextStyle(color: isDark ? Colors.white70 : Colors.grey.shade600, fontSize: 12)),
        const SizedBox(height: 4),
        Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
          _animatedKpiValue(value, color),
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

  static Widget _animatedKpiValue(String value, Color color) {
    final style = TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: color);
    final numVal = num.tryParse(value);
    if (numVal != null) return AnimatedCount(value: numVal, style: style);
    return Text(value, style: style);
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
    bool isDark = false,
  }) {
    final spots = data.asMap().entries.map((e) =>
      FlSpot(e.key.toDouble(), (e.value['value'] as num?)?.toDouble() ?? 0)).toList();
    return _chartCard(title, color, SizedBox(
      height: 220,
      child: LineChart(LineChartData(
        gridData: FlGridData(show: true, drawVerticalLine: false,
            getDrawingHorizontalLine: (v) => FlLine(
              color: (isDark ? Colors.white : Colors.grey).withValues(alpha: 0.12), strokeWidth: 1)),
        titlesData: FlTitlesData(
          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 40,
              getTitlesWidget: (v, _) => Text('${v.toInt()}$valueSuffix',
                  style: TextStyle(fontSize: 10, color: isDark ? Colors.white70 : Colors.black54)))),
          bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true,
              getTitlesWidget: (v, meta) {
                final i = v.toInt();
                if (i < 0 || i >= data.length) return const SizedBox();
                return Padding(
                  padding: const EdgeInsets.only(top: 8),
                  child: Text(data[i]['label']?.toString() ?? '',
                      style: TextStyle(fontSize: 10, color: isDark ? Colors.white70 : Colors.black54)),
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
    ), isDark: isDark);
  }

  static Widget barChart({
    required List<Map<String, dynamic>> data,
    required Color color,
    required String title,
    bool horizontal = false,
    bool isDark = false,
  }) {
    return _chartCard(title, color, SizedBox(
      height: 220,
      child: BarChart(BarChartData(
        alignment: BarChartAlignment.spaceAround,
        maxY: _maxY(data) * 1.2,
        gridData: FlGridData(show: true, drawVerticalLine: false,
            getDrawingHorizontalLine: (v) => FlLine(
              color: (isDark ? Colors.white : Colors.grey).withValues(alpha: 0.12), strokeWidth: 1)),
        titlesData: FlTitlesData(
          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 36,
              getTitlesWidget: (v, _) => Text(v.toInt().toString(),
                  style: TextStyle(fontSize: 10, color: isDark ? Colors.white70 : Colors.black54)))),
          bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true,
              getTitlesWidget: (v, meta) {
                final i = v.toInt();
                if (i < 0 || i >= data.length) return const SizedBox();
                return Text(data[i]['label']?.toString() ?? '',
                    style: TextStyle(fontSize: 9, color: isDark ? Colors.white70 : Colors.black54));
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
    ), isDark: isDark);
  }

  static Widget groupedBarChart({
    required List<Map<String, dynamic>> income,
    required List<Map<String, dynamic>> expense,
    required String title,
    bool isDark = false,
  }) {
    return _chartCard(title, AppTheme.primaryGreen, SizedBox(
      height: 240,
      child: BarChart(BarChartData(
        alignment: BarChartAlignment.spaceAround,
        maxY: max(_maxY(income), _maxY(expense)) * 1.3,
        gridData: FlGridData(show: true, drawVerticalLine: false,
            getDrawingHorizontalLine: (v) => FlLine(
              color: (isDark ? Colors.white : Colors.grey).withValues(alpha: 0.12), strokeWidth: 1)),
        titlesData: FlTitlesData(
          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 48,
              getTitlesWidget: (v, _) => Text('${(v / 1000).toInt()}k',
                  style: TextStyle(fontSize: 10, color: isDark ? Colors.white70 : Colors.black54)))),
          bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true,
              getTitlesWidget: (v, meta) {
                final i = v.toInt();
                if (i < 0 || i >= income.length) return const SizedBox();
                return Text(income[i]['label']?.toString() ?? '',
                    style: TextStyle(fontSize: 10, color: isDark ? Colors.white70 : Colors.black54));
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
    ), isDark: isDark);
  }

  static Widget donutChart({
    required List<Map<String, dynamic>> data,
    required String title,
    bool isDark = false,
  }) {
    final total = data.fold<double>(0, (s, d) => s + ((d['value'] as num?)?.toDouble() ?? 0));
    if (total == 0) return _chartCard(title, AppTheme.primaryGreen, const Center(child: Text('Aucune donnée')), isDark: isDark);
    final legendStyle = TextStyle(fontSize: 11, color: isDark ? Colors.white70 : Colors.black87);
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
                Expanded(child: Text(e.value['name']?.toString() ?? '', style: legendStyle, overflow: TextOverflow.ellipsis)),
              ]),
            );
          }).toList(),
        )),
      ]),
    ), isDark: isDark);
  }

  static Widget radarChart({
    required List<String> labels,
    required List<double> values,
    required String title,
    bool isDark = false,
  }) {
    final gridColor = (isDark ? Colors.white : Colors.grey).withValues(alpha: isDark ? 0.15 : 0.2);
    return _chartCard(title, AppTheme.climateBlue, SizedBox(
      height: 260,
      child: RadarChart(RadarChartData(
        radarShape: RadarShape.polygon,
        tickCount: 4,
        ticksTextStyle: const TextStyle(fontSize: 0),
        radarBorderData: BorderSide(color: gridColor),
        gridBorderData: BorderSide(color: gridColor),
        tickBorderData: BorderSide(color: gridColor),
        getTitle: (i, _) => RadarChartTitle(text: i < labels.length ? labels[i] : '', angle: 0),
        dataSets: [RadarDataSet(
          fillColor: AppTheme.climateBlue.withValues(alpha: 0.25),
          borderColor: AppTheme.climateBlue,
          borderWidth: 2,
          entryRadius: 3,
          dataEntries: values.map((v) => RadarEntry(value: v)).toList(),
        )],
      )),
    ), isDark: isDark);
  }

  static Widget _chartCard(String title, Color accent, Widget chart, {bool isDark = false}) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF2A2A2A) : Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: isDark ? null : [BoxShadow(color: Colors.black.withValues(alpha: 0.06), blurRadius: 16, offset: const Offset(0, 4))],
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 16, 16, 0),
          child: Row(children: [
            Container(width: 4, height: 20, decoration: BoxDecoration(color: accent, borderRadius: BorderRadius.circular(2))),
            const SizedBox(width: 10),
            Text(title, style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600, color: isDark ? Colors.white : Colors.black87)),
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

  static Widget chartCard({required String title, required Color accent, required Widget child, bool isDark = false}) =>
      _chartCard(title, accent, child, isDark: isDark);

  static Widget sankeyChart({required String title, required Map<String, dynamic> data, bool isDark = false}) {
    final nodes = (data['nodes'] as List?)?.cast<String>() ?? [];
    final links = (data['links'] as List?)?.cast<Map<String, dynamic>>() ?? [];
    final total = (data['total_income'] as num?)?.toDouble() ?? links.fold<double>(0, (s, l) => s + ((l['value'] as num?)?.toDouble() ?? 0));
    return _chartCard(title, AppTheme.primaryGreen, Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (total > 0) Text('Revenus: ${total.toInt()} XOF', style: TextStyle(fontWeight: FontWeight.bold, color: isDark ? Colors.white : Colors.black87)),
        const SizedBox(height: 12),
        ...links.map((link) {
          final target = (link['target'] as int?) ?? 0;
          final val = (link['value'] as num?)?.toDouble() ?? 0;
          final label = target < nodes.length ? nodes[target] : '';
          final pct = total > 0 ? val / total : 0;
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 4),
            child: Row(children: [
              SizedBox(width: 80, child: Text(label, style: TextStyle(fontSize: 11, color: isDark ? Colors.white70 : Colors.black87))),
              Expanded(child: ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: LinearProgressIndicator(value: pct, minHeight: 16, color: palette[(link['target'] as int? ?? 0) % palette.length]),
              )),
              const SizedBox(width: 8),
              Text('${val.toInt()}', style: const TextStyle(fontSize: 11)),
            ]),
          );
        }),
      ],
    ), isDark: isDark);
  }

  static Widget seasonCompareChart({required String title, required Map<String, dynamic> data, bool isDark = false}) {
    final rows = (data['data'] as List?)?.cast<Map<String, dynamic>>() ?? [];
    final crops = (data['crops'] as List?)?.cast<String>() ?? [];
    if (rows.isEmpty) return chartCard(title: title, accent: AppTheme.accentOrange, child: const Text('Aucune donnée'), isDark: isDark);
    return _chartCard(title, AppTheme.accentOrange, SizedBox(
      height: 220,
      child: BarChart(BarChartData(
        alignment: BarChartAlignment.spaceAround,
        maxY: rows.expand((r) => (r['values'] as List?)?.cast<num>() ?? []).fold<double>(0, (m, v) => v.toDouble() > m ? v.toDouble() : m) * 1.2,
        gridData: FlGridData(show: true, drawVerticalLine: false,
            getDrawingHorizontalLine: (v) => FlLine(color: (isDark ? Colors.white : Colors.grey).withValues(alpha: 0.12), strokeWidth: 1)),
        titlesData: FlTitlesData(
          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true,
              getTitlesWidget: (v, _) {
                final i = v.toInt();
                if (i < 0 || i >= rows.length) return const SizedBox();
                return Text('${rows[i]['year']}', style: TextStyle(fontSize: 10, color: isDark ? Colors.white70 : Colors.black54));
              })),
          leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 40,
              getTitlesWidget: (v, _) => Text(v.toInt().toString(), style: TextStyle(fontSize: 10, color: isDark ? Colors.white70 : Colors.black54)))),
        ),
        borderData: FlBorderData(show: false),
        barGroups: List.generate(rows.length, (i) {
          final vals = (rows[i]['values'] as List?)?.cast<num>() ?? [];
          return BarChartGroupData(x: i, barsSpace: 4, barRods: List.generate(vals.length, (j) {
            return BarChartRodData(
              toY: vals[j].toDouble(),
              width: 8,
              color: palette[j % palette.length],
              borderRadius: const BorderRadius.vertical(top: Radius.circular(3)),
            );
          }));
        }),
      )),
    ), isDark: isDark);
  }
}
