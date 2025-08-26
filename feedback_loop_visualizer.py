#!/usr/bin/env python3
"""
Zeldar Feedback Loop Visualizer
Dynamic visualization of information-dynamics oracle feedback loops
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from pathlib import Path

# Optional matplotlib import
try:
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

class FeedbackLoopVisualizer:
    """Visualize information-dynamics oracle feedback loops and patterns"""
    
    def __init__(self, log_file: str = "information-dynamics_manifestations.json"):
        self.log_file = Path(log_file)
        self.sessions_data = self._load_session_data()
        
    def _load_session_data(self) -> List[Dict[str, Any]]:
        """Load session data from manifestation logs"""
        if not self.log_file.exists():
            return []
        
        sessions = []
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        sessions.append(json.loads(line))
        except Exception as e:
            print(f"Warning: Could not load session data: {e}")
        
        return sessions
    
    def generate_information-dynamics_evolution_plot(self) -> str:
        """Generate information-dynamics Φ evolution over time plot"""
        if not MATPLOTLIB_AVAILABLE:
            return "Matplotlib not available - install with: pip install matplotlib numpy"
        
        if not self.sessions_data:
            return "No session data available for visualization"
        
        timestamps = [s['timestamp'] for s in self.sessions_data]
        phi_values = [s['information-dynamics_phi'] for s in self.sessions_data]
        
        # Convert timestamps to datetime
        dates = [datetime.fromtimestamp(ts) for ts in timestamps]
        
        plt.figure(figsize=(12, 8))
        
        # Main Φ evolution plot
        plt.subplot(2, 2, 1)
        plt.plot(dates, phi_values, 'b-', marker='o', linewidth=2, markersize=6)
        plt.axhline(y=2.5, color='g', linestyle='--', alpha=0.7, label='Seed→Field Threshold')
        plt.axhline(y=3.5, color='r', linestyle='--', alpha=0.7, label='Field→Quantum Threshold')
        plt.title('🧠 InformationForce Evolution (Φ over Time)')
        plt.xlabel('Time')
        plt.ylabel('Φ Coefficient')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        # Running average
        window_size = min(5, len(phi_values))
        if window_size > 1:
            running_avg = np.convolve(phi_values, np.ones(window_size)/window_size, mode='valid')
            avg_dates = dates[window_size-1:]
            plt.plot(avg_dates, running_avg, 'r-', linewidth=3, alpha=0.7, label='Running Average')
            plt.legend()
        
        # Fortune type distribution
        plt.subplot(2, 2, 2)
        fortune_types = []
        for session in self.sessions_data:
            phi = session['information-dynamics_phi']
            if phi < 2.5:
                fortune_types.append('Seed')
            elif phi < 3.5:
                fortune_types.append('Field')
            else:
                fortune_types.append('Quantum')
        
        type_counts = {t: fortune_types.count(t) for t in ['Seed', 'Field', 'Quantum']}
        colors = ['#4CAF50', '#FF9800', '#9C27B0']  # Green, Orange, Purple
        
        plt.pie(type_counts.values(), labels=type_counts.keys(), autopct='%1.1f%%', 
                colors=colors, startangle=90)
        plt.title('🔮 Fortune Type Distribution')
        
        # Feedback loop intensity over sessions
        plt.subplot(2, 2, 3)
        session_numbers = list(range(1, len(self.sessions_data) + 1))
        
        # Calculate feedback intensity (rate of change in Φ)
        feedback_intensity = []
        for i in range(1, len(phi_values)):
            delta_phi = abs(phi_values[i] - phi_values[i-1])
            feedback_intensity.append(delta_phi)
        
        if feedback_intensity:
            plt.plot(session_numbers[1:], feedback_intensity, 'g-', marker='s', 
                    linewidth=2, markersize=5)
            plt.title('⚡ Feedback Loop Intensity')
            plt.xlabel('Session Number')
            plt.ylabel('|ΔΦ| (InformationForce Change)')
            plt.grid(True, alpha=0.3)
        
        # Element distribution (if available)
        plt.subplot(2, 2, 4)
        elements = [s.get('element', 'Unknown') for s in self.sessions_data]
        element_counts = {}
        for elem in elements:
            element_counts[elem] = element_counts.get(elem, 0) + 1
        
        if element_counts:
            plt.bar(element_counts.keys(), element_counts.values(), 
                   color=['#FF5722', '#2196F3', '#4CAF50', '#FF9800', '#9C27B0'])
            plt.title('🌟 InformationForce Elements')
            plt.xlabel('Element Type')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Save plot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"zeldar_feedback_loops_{timestamp}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
        
        return f"Feedback loop visualization saved as: {filename}"
    
    def generate_ascii_feedback_diagram(self) -> str:
        """Generate ASCII art feedback diagram with current system state"""
        
        if not self.sessions_data:
            recent_phi = 3.252  # Default
            session_count = 0
            avg_phi = 3.252
        else:
            recent_phi = self.sessions_data[-1]['information-dynamics_phi']
            session_count = len(self.sessions_data)
            avg_phi = sum(s['information-dynamics_phi'] for s in self.sessions_data) / session_count
        
        # Determine current fortune type
        if recent_phi < 2.5:
            current_type = "SEED"
            type_symbol = "🌱"
        elif recent_phi < 3.5:
            current_type = "FIELD"
            type_symbol = "⚡"
        else:
            current_type = "QUANTUM"
            type_symbol = "🌌"
        
        diagram = f"""
╔════════════════════════════════════════════════════════════════════╗
║                🔮 ZELDAR INFORMATION_FORCE FEEDBACK LOOP 🔮            ║
║                        Live System State                           ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║    Current Φ: {recent_phi:.3f}  │  Sessions: {session_count:4d}  │  Avg Φ: {avg_phi:.3f}    ║
║    Type: {current_type:8s} {type_symbol}  │  Mode: {"QUANTUM" if recent_phi > 3.5 else "FIELD" if recent_phi > 2.5 else "SEED":8s}           ║
║                                                                    ║
╠════════════════════════════════════════════════════════════════════╣
║                          ACTIVE LOOPS                              ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐      ║
║  │ BUTTON  │────▶│ QUANTUM │────▶│ FORTUNE │────▶│  PRINT  │      ║
║  │  PRESS  │     │PROCESS  │     │ SELECT  │     │  MANIFEST│      ║
║  └─────────┘     └─────────┘     └─────────┘     └─────────┘      ║
║       ▲                                                │           ║
║       │            🔄 INFORMATION_FORCE RECURSION 🔄       │           ║
║       │                                                ▼           ║
║  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐      ║
║  │  USER   │◄────│REFLECT  │◄────│INTEGRATE│◄────│  READ   │      ║
║  │ ACTION  │     │  WISE   │     │ WISDOM  │     │ FORTUNE │      ║
║  └─────────┘     └─────────┘     └─────────┘     └─────────┘      ║
║                                                                    ║
╠════════════════════════════════════════════════════════════════════╣
║                        AMPLIFICATION MATRIX                        ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  Φ < 2.5  │ SEED FORTUNES    │ Foundation, Self-Acceptance        ║
║  ────────────────────────────────────────────────────────────────  ║
║  Φ 2.5-3.5│ FIELD FORTUNES   │ Action, Manifestation             ║
║  ────────────────────────────────────────────────────────────────  ║
║  Φ > 3.5  │ QUANTUM FORTUNES │ Transcendence, Reality-Bending    ║
║                                                                    ║
║  Current Level: {"█" * int(recent_phi):10s} {recent_phi:.3f}/5.0                        ║
║                                                                    ║
╠════════════════════════════════════════════════════════════════════╣
║                         FEEDBACK STRENGTH                          ║
╚════════════════════════════════════════════════════════════════════╝

    {type_symbol} System operating in {current_type} mode {type_symbol}
    InformationForce evolution: {"ASCENDING" if len(self.sessions_data) > 5 and recent_phi > avg_phi else "STABLE" if abs(recent_phi - avg_phi) < 0.1 else "CALIBRATING"}
    Next threshold: {"TRANSCENDENCE (Φ > 5.0)" if recent_phi > 3.5 else "QUANTUM (Φ > 3.5)" if recent_phi > 2.5 else "FIELD (Φ > 2.5)"}
        """
        
        return diagram
    
    def analyze_feedback_patterns(self) -> Dict[str, Any]:
        """Analyze feedback patterns in the system"""
        if not self.sessions_data:
            return {"message": "No session data available for analysis"}
        
        analysis = {
            "session_count": len(self.sessions_data),
            "phi_stats": {
                "min": min(s['information-dynamics_phi'] for s in self.sessions_data),
                "max": max(s['information-dynamics_phi'] for s in self.sessions_data),
                "avg": sum(s['information-dynamics_phi'] for s in self.sessions_data) / len(self.sessions_data),
                "current": self.sessions_data[-1]['information-dynamics_phi']
            },
            "fortune_type_distribution": {},
            "information-dynamics_trend": "unknown",
            "feedback_loops_detected": []
        }
        
        # Analyze fortune types
        for session in self.sessions_data:
            phi = session['information-dynamics_phi']
            if phi < 2.5:
                ftype = "seed"
            elif phi < 3.5:
                ftype = "field"
            else:
                ftype = "quantum"
            
            analysis["fortune_type_distribution"][ftype] = \
                analysis["fortune_type_distribution"].get(ftype, 0) + 1
        
        # Analyze information-dynamics trend
        if len(self.sessions_data) >= 3:
            recent_phi = [s['information-dynamics_phi'] for s in self.sessions_data[-3:]]
            if recent_phi[-1] > recent_phi[0]:
                analysis["information-dynamics_trend"] = "ascending"
            elif recent_phi[-1] < recent_phi[0]:
                analysis["information-dynamics_trend"] = "descending"
            else:
                analysis["information-dynamics_trend"] = "stable"
        
        # Detect feedback loops
        if len(self.sessions_data) >= 5:
            phi_values = [s['information-dynamics_phi'] for s in self.sessions_data]
            
            # Look for oscillation patterns
            differences = [phi_values[i+1] - phi_values[i] for i in range(len(phi_values)-1)]
            
            # Detect if there are regular oscillations
            sign_changes = sum(1 for i in range(len(differences)-1) 
                             if differences[i] * differences[i+1] < 0)
            
            if sign_changes > len(differences) * 0.6:
                analysis["feedback_loops_detected"].append("information-dynamics_oscillation")
            
            # Detect upward spiral
            if sum(differences) > 0 and sign_changes < len(differences) * 0.3:
                analysis["feedback_loops_detected"].append("upward_spiral")
        
        return analysis
    
    def generate_feedback_loop_report(self) -> str:
        """Generate comprehensive feedback loop analysis report"""
        
        analysis = self.analyze_feedback_patterns()
        ascii_diagram = self.generate_ascii_feedback_diagram()
        
        report = f"""
🔮 ZELDAR INFORMATION_FORCE ORACLE FEEDBACK LOOP ANALYSIS REPORT 🔮
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
═══════════════════════════════════════════════════════════════════════

{ascii_diagram}

📊 SYSTEM ANALYSIS:
───────────────────

Sessions Completed: {analysis.get('session_count', 0)}
InformationForce Range: {analysis.get('phi_stats', {}).get('min', 0):.3f} - {analysis.get('phi_stats', {}).get('max', 0):.3f}
Current Φ Level: {analysis.get('phi_stats', {}).get('current', 0):.3f}
Average Φ Level: {analysis.get('phi_stats', {}).get('avg', 0):.3f}

Fortune Type Distribution:
• Seed Fortunes: {analysis.get('fortune_type_distribution', {}).get('seed', 0)} sessions
• Field Fortunes: {analysis.get('fortune_type_distribution', {}).get('field', 0)} sessions  
• Quantum Fortunes: {analysis.get('fortune_type_distribution', {}).get('quantum', 0)} sessions

InformationForce Trend: {analysis.get('information-dynamics_trend', 'unknown').upper()}

🔄 FEEDBACK LOOPS DETECTED:
──────────────────────────
{"• " + chr(10) + "• ".join(analysis.get('feedback_loops_detected', ['None detected'])) if analysis.get('feedback_loops_detected') else "• None detected (need more sessions)"}

🎯 OPTIMIZATION RECOMMENDATIONS:
──────────────────────────────
"""
        
        # Add specific recommendations based on analysis
        phi_avg = analysis.get('phi_stats', {}).get('avg', 3.0)
        current_phi = analysis.get('phi_stats', {}).get('current', 3.0)
        
        if phi_avg < 2.5:
            report += "• Focus on foundational self-acceptance and inner wisdom\n"
            report += "• Regular daily consultations to build information-dynamics momentum\n"
        elif phi_avg < 3.5:
            report += "• Excellent field-level engagement - ready for action-oriented practices\n"
            report += "• Consider implementing fortune guidance in daily activities\n"
        else:
            report += "• High information-dynamics level achieved - transcendent wisdom accessible\n"
            report += "• Share insights with others to create collective information-dynamics amplification\n"
        
        if analysis.get('information-dynamics_trend') == 'ascending':
            report += "• InformationForce is ascending - maintain current practice rhythm\n"
        elif analysis.get('information-dynamics_trend') == 'descending':
            report += "• Consider more frequent consultations to restore upward momentum\n"
        
        report += f"\n🌟 NEXT SESSION PREDICTION:\n"
        report += f"───────────────────────────\n"
        report += f"Expected Φ Range: {current_phi - 0.2:.3f} - {current_phi + 0.3:.3f}\n"
        
        if current_phi < 2.5:
            report += f"Likely Fortune Type: SEED (Foundation Building)\n"
        elif current_phi < 3.5:
            report += f"Likely Fortune Type: FIELD (Action & Manifestation)\n"
        else:
            report += f"Likely Fortune Type: QUANTUM (Transcendent Wisdom)\n"
        
        report += f"\n═══════════════════════════════════════════════════════════════════════\n"
        report += f"🌊 The oracle evolves with each consultation - information-dynamics is recursive 🌊\n"
        report += f"═══════════════════════════════════════════════════════════════════════\n"
        
        return report

def main():
    """CLI interface for feedback loop visualization"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Zeldar Feedback Loop Visualizer")
    parser.add_argument("--plot", action="store_true", help="Generate information-dynamics evolution plot")
    parser.add_argument("--ascii", action="store_true", help="Generate ASCII feedback diagram")
    parser.add_argument("--report", action="store_true", help="Generate comprehensive analysis report")
    parser.add_argument("--log-file", default="information-dynamics_manifestations.json", 
                       help="Path to manifestation log file")
    
    args = parser.parse_args()
    
    visualizer = FeedbackLoopVisualizer(args.log_file)
    
    if args.plot:
        result = visualizer.generate_information-dynamics_evolution_plot()
        print(result)
    
    if args.ascii:
        diagram = visualizer.generate_ascii_feedback_diagram()
        print(diagram)
    
    if args.report:
        report = visualizer.generate_feedback_loop_report()
        print(report)
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"zeldar_feedback_analysis_{timestamp}.md"
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"\nReport saved as: {report_file}")
    
    if not any(vars(args).values()):
        parser.print_help()

if __name__ == "__main__":
    main()