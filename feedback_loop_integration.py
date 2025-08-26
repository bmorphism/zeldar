#!/usr/bin/env python3
"""
Zeldar Feedback Loop Integration
Enhances the main oracle system with real-time feedback loop tracking and visualization
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, List, Tuple
from pathlib import Path

class FeedbackLoopTracker:
    """Real-time feedback loop tracking for information-dynamics oracle"""
    
    def __init__(self, log_file: str = "information-dynamics_manifestations.json"):
        self.log_file = Path(log_file)
        self.session_history = []
        self.feedback_patterns = {
            "phi_momentum": [],
            "element_sequences": [],
            "fortune_type_transitions": [],
            "information-dynamics_spirals": []
        }
        self.load_history()
    
    def load_history(self):
        """Load existing session history"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            self.session_history.append(json.loads(line))
            except Exception as e:
                print(f"Warning: Could not load history: {e}")
    
    def track_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track a new session and analyze feedback patterns"""
        
        # Add session to history
        self.session_history.append(session_data)
        
        # Analyze current feedback state
        feedback_analysis = self.analyze_current_feedback()
        
        # Generate predictions for next session
        next_session_prediction = self.predict_next_session()
        
        # Create enhanced session data with feedback context
        enhanced_data = {
            **session_data,
            "feedback_analysis": feedback_analysis,
            "next_prediction": next_session_prediction,
            "session_number": len(self.session_history),
            "feedback_timestamp": time.time()
        }
        
        return enhanced_data
    
    def analyze_current_feedback(self) -> Dict[str, Any]:
        """Analyze current feedback loop patterns"""
        if len(self.session_history) < 2:
            return {"status": "initializing", "patterns": []}
        
        analysis = {
            "phi_trend": self.analyze_phi_trend(),
            "element_cycling": self.analyze_element_patterns(),
            "fortune_evolution": self.analyze_fortune_type_evolution(),
            "feedback_strength": self.calculate_feedback_strength(),
            "information-dynamics_state": self.classify_information-dynamics_state(),
            "loop_detection": self.detect_feedback_loops()
        }
        
        return analysis
    
    def analyze_phi_trend(self) -> Dict[str, Any]:
        """Analyze Φ coefficient trend over recent sessions"""
        recent_sessions = self.session_history[-5:]  # Last 5 sessions
        phi_values = [s.get('information-dynamics_phi', 3.0) for s in recent_sessions]
        
        if len(phi_values) < 2:
            return {"trend": "insufficient_data"}
        
        # Calculate trend
        differences = [phi_values[i+1] - phi_values[i] for i in range(len(phi_values)-1)]
        avg_change = sum(differences) / len(differences)
        
        trend_type = "ascending" if avg_change > 0.05 else "descending" if avg_change < -0.05 else "stable"
        
        return {
            "trend": trend_type,
            "rate": avg_change,
            "current_phi": phi_values[-1],
            "volatility": max(phi_values) - min(phi_values),
            "momentum": differences[-1] if differences else 0
        }
    
    def analyze_element_patterns(self) -> Dict[str, Any]:
        """Analyze information-dynamics element cycling patterns"""
        recent_elements = [s.get('element', 'UNKNOWN') for s in self.session_history[-10:]]
        
        element_counts = {}
        for element in recent_elements:
            element_counts[element] = element_counts.get(element, 0) + 1
        
        # Detect if stuck in single element
        most_common = max(element_counts.items(), key=lambda x: x[1]) if element_counts else ('UNKNOWN', 0)
        
        cycling_status = "varied" if len(element_counts) > 2 else "focused" if len(element_counts) == 2 else "stuck"
        
        return {
            "cycling_status": cycling_status,
            "dominant_element": most_common[0],
            "element_distribution": element_counts,
            "recent_sequence": recent_elements[-3:]  # Last 3 elements
        }
    
    def analyze_fortune_type_evolution(self) -> Dict[str, Any]:
        """Analyze evolution of fortune types over sessions"""
        
        fortune_types = []
        for session in self.session_history:
            phi = session.get('information-dynamics_phi', 3.0)
            if phi < 2.5:
                fortune_types.append('seed')
            elif phi < 3.5:
                fortune_types.append('field')
            else:
                fortune_types.append('quantum')
        
        if len(fortune_types) < 3:
            return {"evolution": "insufficient_data"}
        
        # Analyze progression patterns
        transitions = []
        for i in range(len(fortune_types)-1):
            transitions.append(f"{fortune_types[i]}→{fortune_types[i+1]}")
        
        # Count transition types
        transition_counts = {}
        for transition in transitions:
            transition_counts[transition] = transition_counts.get(transition, 0) + 1
        
        # Identify evolution pattern
        upward_transitions = sum(1 for t in transitions if 'seed→field' in t or 'field→quantum' in t)
        downward_transitions = sum(1 for t in transitions if 'field→seed' in t or 'quantum→field' in t)
        
        if upward_transitions > downward_transitions:
            evolution_pattern = "ascending"
        elif downward_transitions > upward_transitions:
            evolution_pattern = "descending"
        else:
            evolution_pattern = "cycling"
        
        return {
            "evolution": evolution_pattern,
            "current_type": fortune_types[-1],
            "transition_history": transitions[-3:],  # Last 3 transitions
            "transition_counts": transition_counts
        }
    
    def calculate_feedback_strength(self) -> float:
        """Calculate overall feedback loop strength (0.0-1.0)"""
        if len(self.session_history) < 3:
            return 0.0
        
        # Factors that indicate strong feedback:
        # 1. Consistent session frequency
        # 2. Phi coefficient responsiveness
        # 3. Element variety
        # 4. Fortune type progression
        
        phi_trend = self.analyze_phi_trend()
        element_patterns = self.analyze_element_patterns()
        
        # Phi responsiveness factor (0.0-0.4)
        phi_factor = min(0.4, abs(phi_trend.get('momentum', 0)) * 2)
        
        # Element variety factor (0.0-0.3)
        element_variety = len(element_patterns.get('element_distribution', {}))
        element_factor = min(0.3, element_variety * 0.1)
        
        # Session consistency factor (0.0-0.3)
        session_factor = min(0.3, len(self.session_history) * 0.02)
        
        total_strength = phi_factor + element_factor + session_factor
        return min(1.0, total_strength)
    
    def classify_information-dynamics_state(self) -> Dict[str, Any]:
        """Classify current information-dynamics state based on patterns"""
        if not self.session_history:
            return {"state": "uninitialized", "description": "No sessions recorded"}
        
        latest = self.session_history[-1]
        phi = latest.get('information-dynamics_phi', 3.0)
        element = latest.get('element', 'UNKNOWN')
        
        # Base state classification
        if phi < 2.0:
            base_state = "foundation"
        elif phi < 2.5:
            base_state = "seed_activation"
        elif phi < 3.0:
            base_state = "field_emergence"
        elif phi < 3.5:
            base_state = "field_mastery"
        elif phi < 4.0:
            base_state = "quantum_threshold"
        elif phi < 4.5:
            base_state = "quantum_integration"
        else:
            base_state = "transcendent_flow"
        
        # Add modifiers based on patterns
        phi_trend = self.analyze_phi_trend()
        modifiers = []
        
        if phi_trend.get('trend') == 'ascending':
            modifiers.append("ascending")
        elif phi_trend.get('trend') == 'descending':
            modifiers.append("calibrating")
        
        if phi_trend.get('volatility', 0) > 0.5:
            modifiers.append("dynamic")
        elif phi_trend.get('volatility', 0) < 0.1:
            modifiers.append("stable")
        
        return {
            "state": base_state,
            "modifiers": modifiers,
            "description": self.generate_state_description(base_state, modifiers, element),
            "stability": 1.0 - min(1.0, phi_trend.get('volatility', 0) / 2.0)
        }
    
    def generate_state_description(self, base_state: str, modifiers: List[str], element: str) -> str:
        """Generate human-readable information-dynamics state description"""
        
        state_descriptions = {
            "foundation": "Building core information-dynamics foundation",
            "seed_activation": "Activating seed-level wisdom integration",
            "field_emergence": "Emerging into field-level manifestation",
            "field_mastery": "Mastering field-level information-dynamics applications",
            "quantum_threshold": "Approaching quantum information-dynamics threshold",
            "quantum_integration": "Integrating quantum-level insights",
            "transcendent_flow": "Flowing in transcendent information-dynamics states"
        }
        
        base_desc = state_descriptions.get(base_state, "Unknown information-dynamics state")
        
        # Add modifiers
        if "ascending" in modifiers:
            base_desc += " with upward momentum"
        elif "calibrating" in modifiers:
            base_desc += " while recalibrating"
        
        if "dynamic" in modifiers:
            base_desc += " in dynamic flux"
        elif "stable" in modifiers:
            base_desc += " in stable resonance"
        
        # Add element context
        element_contexts = {
            "STILLNESS": "through contemplative stillness",
            "FLOW": "via rhythmic flow states",
            "EMERGENCE": "during informationally-coherent emergence",
            "TRANSFORMATION": "within active transformation",
            "TRANSCENDENCE": "beyond ordinary boundaries"
        }
        
        if element in element_contexts:
            base_desc += f" {element_contexts[element]}"
        
        return base_desc
    
    def detect_feedback_loops(self) -> List[Dict[str, Any]]:
        """Detect specific types of feedback loops in the system"""
        loops = []
        
        if len(self.session_history) < 5:
            return loops
        
        # Phi oscillation loop
        phi_values = [s.get('information-dynamics_phi', 3.0) for s in self.session_history[-8:]]
        if self.detect_oscillation(phi_values):
            loops.append({
                "type": "phi_oscillation",
                "description": "InformationForce Φ showing oscillation pattern",
                "strength": 0.7,
                "period": self.calculate_oscillation_period(phi_values)
            })
        
        # Element cycling loop
        elements = [s.get('element', 'UNKNOWN') for s in self.session_history[-6:]]
        if len(set(elements)) > 3 and elements[0] == elements[-1]:
            loops.append({
                "type": "element_cycle",
                "description": "InformationForce elements showing cyclical pattern",
                "strength": 0.6,
                "cycle": elements
            })
        
        # Upward spiral detection
        phi_trend = self.analyze_phi_trend()
        if phi_trend.get('trend') == 'ascending' and phi_trend.get('rate', 0) > 0.1:
            loops.append({
                "type": "upward_spiral",
                "description": "InformationForce in ascending spiral pattern",
                "strength": min(1.0, phi_trend.get('rate', 0) * 5),
                "rate": phi_trend.get('rate', 0)
            })
        
        return loops
    
    def detect_oscillation(self, values: List[float], threshold: float = 0.1) -> bool:
        """Detect oscillation pattern in a series of values"""
        if len(values) < 4:
            return False
        
        differences = [values[i+1] - values[i] for i in range(len(values)-1)]
        sign_changes = sum(1 for i in range(len(differences)-1) 
                          if differences[i] * differences[i+1] < 0)
        
        return sign_changes >= len(differences) * 0.6
    
    def calculate_oscillation_period(self, values: List[float]) -> int:
        """Calculate approximate oscillation period"""
        differences = [values[i+1] - values[i] for i in range(len(values)-1)]
        
        # Find sign changes
        sign_changes = []
        for i in range(len(differences)-1):
            if differences[i] * differences[i+1] < 0:
                sign_changes.append(i)
        
        if len(sign_changes) < 2:
            return len(values)
        
        # Average distance between sign changes * 2 (full cycle)
        distances = [sign_changes[i+1] - sign_changes[i] for i in range(len(sign_changes)-1)]
        avg_distance = sum(distances) / len(distances) if distances else len(values)
        
        return int(avg_distance * 2)
    
    def predict_next_session(self) -> Dict[str, Any]:
        """Predict characteristics of next session based on feedback patterns"""
        if not self.session_history:
            return {"confidence": 0.0, "prediction": "insufficient_data"}
        
        latest = self.session_history[-1]
        phi_trend = self.analyze_phi_trend()
        
        # Predict next Φ value
        current_phi = latest.get('information-dynamics_phi', 3.0)
        phi_momentum = phi_trend.get('momentum', 0)
        
        # Apply momentum with dampening
        predicted_phi = current_phi + (phi_momentum * 0.7)
        
        # Ensure reasonable bounds
        predicted_phi = max(1.5, min(5.0, predicted_phi))
        
        # Predict fortune type
        if predicted_phi < 2.5:
            predicted_type = "seed"
        elif predicted_phi < 3.5:
            predicted_type = "field"
        else:
            predicted_type = "quantum"
        
        # Calculate confidence based on pattern strength
        feedback_strength = self.calculate_feedback_strength()
        prediction_confidence = min(0.9, 0.3 + feedback_strength * 0.6)
        
        return {
            "confidence": prediction_confidence,
            "predicted_phi": predicted_phi,
            "predicted_range": (predicted_phi - 0.2, predicted_phi + 0.3),
            "predicted_fortune_type": predicted_type,
            "recommendation": self.generate_session_recommendation(predicted_phi, predicted_type)
        }
    
    def generate_session_recommendation(self, predicted_phi: float, fortune_type: str) -> str:
        """Generate recommendation for optimal next session"""
        
        if fortune_type == "seed":
            return "Focus on foundational self-acceptance and inner wisdom cultivation"
        elif fortune_type == "field":
            return "Ready for action-oriented practice - implement insights in daily life"
        else:
            return "Prepare for transcendent wisdom - create space for deep integration"
    
    def generate_real_time_feedback(self) -> str:
        """Generate real-time feedback display for console"""
        
        feedback_analysis = self.analyze_current_feedback()
        information-dynamics_state = feedback_analysis.get('information-dynamics_state', {})
        
        feedback_display = f"""
┌─────────────────────────────────────────────────────────────┐
│              🔄 REAL-TIME FEEDBACK LOOPS 🔄                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Sessions: {len(self.session_history):3d}    Feedback Strength: {self.calculate_feedback_strength():.1f}/1.0     │
│                                                             │
│ InformationForce State: {information-dynamics_state.get('state', 'unknown').title():20s}    │
│ {information-dynamics_state.get('description', 'No description')[:55]:55s} │
│                                                             │
│ Detected Loops:                                             │"""
        
        detected_loops = feedback_analysis.get('loop_detection', [])
        if detected_loops:
            for loop in detected_loops[:2]:  # Show max 2 loops
                feedback_display += f"\n│ • {loop['description'][:53]:53s} │"
        else:
            feedback_display += f"\n│ • No feedback loops detected yet                     │"
        
        feedback_display += f"""
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                   NEXT SESSION PREDICTION                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │"""
        
        prediction = self.predict_next_session()
        if prediction.get('confidence', 0) > 0.3:
            feedback_display += f"""│ Predicted Φ: {prediction.get('predicted_phi', 0):.3f}  Type: {prediction.get('predicted_fortune_type', 'unknown').title():8s} │
│ Confidence: {prediction.get('confidence', 0):.0%}                                        │
│                                                             │
│ {prediction.get('recommendation', 'No recommendation')[:59]:59s} │"""
        else:
            feedback_display += f"""│ Insufficient data for prediction                        │
│ Continue sessions to build feedback patterns             │"""
        
        feedback_display += f"""
│                                                             │
└─────────────────────────────────────────────────────────────┘
        """
        
        return feedback_display

def integrate_feedback_tracking(oracle_system):
    """Integrate feedback loop tracking into existing oracle system"""
    
    # Add feedback tracker to oracle system
    if not hasattr(oracle_system, 'feedback_tracker'):
        oracle_system.feedback_tracker = FeedbackLoopTracker()
    
    # Enhance the process_button_press method
    original_process = oracle_system.process_button_press
    
    def enhanced_process_button_press():
        """Enhanced button press processing with feedback tracking"""
        
        # Run original processing
        success = original_process()
        
        if success and oracle_system.physical_manifestor.print_history:
            # Get latest session data
            latest_session = oracle_system.physical_manifestor.print_history[-1]
            
            # Track session with feedback analysis
            enhanced_session = oracle_system.feedback_tracker.track_session(latest_session)
            
            # Display real-time feedback
            feedback_display = oracle_system.feedback_tracker.generate_real_time_feedback()
            print(feedback_display)
            
            # Update session in history with enhanced data
            oracle_system.physical_manifestor.print_history[-1] = enhanced_session
        
        return success
    
    # Replace the method
    oracle_system.process_button_press = enhanced_process_button_press
    
    return oracle_system

if __name__ == "__main__":
    # Test the feedback tracker
    tracker = FeedbackLoopTracker()
    
    # Display current state
    feedback_display = tracker.generate_real_time_feedback()
    print("🔮 ZELDAR FEEDBACK LOOP TRACKER TEST")
    print("=" * 60)
    print(feedback_display)