#!/usr/bin/env python3
"""
Unified Information Force State Bridge for Zeldar Tri-Loop Integration

Connects:
1. Physical Hardware (button-print.py, GPIO)
2. Mathematical Core (ORACLE_PRINT_CORE.py, quantum processing) 
3. Web Interface (information-force-oracle, fortune-web)

Maintains shared information force state across all three operational modes.
"""

import json
import time
import threading
import subprocess
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib

@dataclass
class ZeldarInformationForceState:
    """Unified information force state across all zeldar modes"""
    phi_coefficient: float = 0.0          # From ORACLE_PRINT_CORE calculations
    strange_loops: int = 0                # Mathematical detection count
    button_presses: int = 0               # Hardware GPIO tracking
    web_interactions: int = 0             # Interface engagement count
    print_manifestations: int = 0         # Physical output tracking
    quantum_entropy: float = 0.0          # Latest entropy calculation
    last_activity: str = ""               # ISO timestamp cross-mode sync
    information_force_events: List[Dict] = None  # Event history
    integration_level: str = "dormant"    # dormant|emerging|active|transcendent
    
    def __post_init__(self):
        if self.information_force_events is None:
            self.information_force_events = []

class InformationForceBridge:
    """
    Bridge between hardware, mathematical, and web information force systems
    
    Implements shared state management and cross-mode correlation detection
    """
    
    def __init__(self, state_file: str = ".topos/information_force_state.json"):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(exist_ok=True)
        
        # Cross-mode synchronization
        self._lock = threading.Lock()
        self._running = True
        
        # Initialize or load existing information force state
        self.information_force_state = self._load_or_initialize_state()
        
        # Start information force correlation monitoring
        self._correlation_thread = threading.Thread(target=self._monitor_information_force_correlation)
        self._correlation_thread.daemon = True
        self._correlation_thread.start()
        
    def _load_or_initialize_state(self) -> ZeldarInformationForceState:
        """Load existing state or create new information force baseline"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    return ZeldarInformationForceState(**data)
            except Exception as e:
                print(f"Warning: Failed to load information force state: {e}")
        
        # Initialize new information force state
        initial_state = ZeldarInformationForceState(
            phi_coefficient=0.85,  # Baseline information force
            last_activity=datetime.now().isoformat(),
            integration_level="emerging"
        )
        self._save_state(initial_state)
        return initial_state
    
    def _save_state(self, state: ZeldarInformationForceState):
        """Atomically save information force state to disk"""
        with self._lock:
            try:
                with open(self.state_file, 'w') as f:
                    json.dump(asdict(state), f, indent=2, default=str)
            except Exception as e:
                print(f"Warning: Failed to save information force state: {e}")
    
    # === HARDWARE INTEGRATION ===
    
    def register_button_press(self, gpio_pin: int = 6) -> Dict[str, Any]:
        """Register GPIO button press and update information force metrics"""
        with self._lock:
            self.information_force_state.button_presses += 1
            self.information_force_state.last_activity = datetime.now().isoformat()
            
            # Calculate quantum-like entropy from button timing
            entropy = self._calculate_button_entropy()
            self.information_force_state.quantum_entropy = entropy
            
            # Update information force coefficient based on hardware engagement
            hardware_phi_boost = 0.15 * (1 + entropy)
            self.information_force_state.phi_coefficient += hardware_phi_boost
            
            # Detect hardware-triggered strange loops
            if self.information_force_state.button_presses % 3 == 0:
                self.information_force_state.strange_loops += 1
            
            # Log information force event
            event = {
                "timestamp": self.information_force_state.last_activity,
                "type": "button_press",
                "gpio_pin": gpio_pin,
                "entropy": entropy,
                "phi_boost": hardware_phi_boost,
                "cumulative_presses": self.information_force_state.button_presses
            }
            self.information_force_state.information_force_events.append(event)
            
            self._update_integration_level()
            self._save_state(self.information_force_state)
            
            return event
    
    def register_print_manifestation(self, content: str, job_id: str) -> Dict[str, Any]:
        """Register physical print manifestation and information force materialization"""
        with self._lock:
            self.information_force_state.print_manifestations += 1
            self.information_force_state.last_activity = datetime.now().isoformat()
            
            # Calculate self-reference level (from ORACLE_PRINT_CORE pattern)
            self_ref_level = self._calculate_self_reference(content)
            
            # Physical manifestation greatly boosts information force
            manifestation_phi_boost = 0.91 + (self_ref_level * 0.1)
            self.information_force_state.phi_coefficient += manifestation_phi_boost
            
            # Physical prints create strong strange loops (virtual→physical)
            self.information_force_state.strange_loops += 2
            
            # Log manifestation event
            event = {
                "timestamp": self.information_force_state.last_activity,
                "type": "print_manifestation",
                "job_id": job_id,
                "content_length": len(content),
                "self_reference_level": self_ref_level,
                "phi_boost": manifestation_phi_boost,
                "cumulative_prints": self.information_force_state.print_manifestations,
                "information_force_materialization": True
            }
            self.information_force_state.information_force_events.append(event)
            
            self._update_integration_level()
            self._save_state(self.information_force_state)
            
            return event
    
    # === MATHEMATICAL INTEGRATION ===
    
    def update_quantum_metrics(self, entropy: float, phi_components: List[float]) -> Dict[str, Any]:
        """Update information force state with quantum calculation results"""
        with self._lock:
            self.information_force_state.quantum_entropy = entropy
            self.information_force_state.phi_coefficient = sum(phi_components)
            self.information_force_state.last_activity = datetime.now().isoformat()
            
            # Mathematical precision increases information force correlation
            if len(phi_components) >= 4:  # Full phi calculation
                self.information_force_state.strange_loops += len([c for c in phi_components if c > 0.8])
            
            event = {
                "timestamp": self.information_force_state.last_activity,
                "type": "quantum_update",
                "entropy": entropy,
                "phi_components": phi_components,
                "total_phi": sum(phi_components),
                "mathematical_precision": True
            }
            self.information_force_state.information_force_events.append(event)
            
            self._update_integration_level()
            self._save_state(self.information_force_state)
            
            return event
    
    # === WEB INTEGRATION ===
    
    def register_web_interaction(self, interaction_type: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Register web interface interaction and information force engagement"""
        with self._lock:
            self.information_force_state.web_interactions += 1
            self.information_force_state.last_activity = datetime.now().isoformat()
            
            # Web interactions provide information force amplification
            web_phi_boost = 0.25 + (0.05 * len(data or {}))
            self.information_force_state.phi_coefficient += web_phi_boost
            
            # Complex web interactions create strange loops
            if interaction_type in ["fortune_request", "information_force_query", "mystical_interface"]:
                self.information_force_state.strange_loops += 1
            
            event = {
                "timestamp": self.information_force_state.last_activity,
                "type": "web_interaction",
                "interaction_type": interaction_type,
                "data": data or {},
                "phi_boost": web_phi_boost,
                "cumulative_interactions": self.information_force_state.web_interactions
            }
            self.information_force_state.information_force_events.append(event)
            
            self._update_integration_level()
            self._save_state(self.information_force_state)
            
            return event
    
    # === INFORMATION FORCE CORRELATION ===
    
    def get_information_force_metrics(self) -> Dict[str, Any]:
        """Get current information force correlation metrics for all modes"""
        with self._lock:
            return {
                "phi_coefficient": self.information_force_state.phi_coefficient,
                "strange_loops": self.information_force_state.strange_loops,
                "integration_level": self.information_force_state.integration_level,
                "multi_mode_engagement": {
                    "hardware_activity": self.information_force_state.button_presses,
                    "mathematical_precision": self.information_force_state.quantum_entropy,
                    "web_information_force": self.information_force_state.web_interactions,
                    "physical_manifestations": self.information_force_state.print_manifestations
                },
                "information_force_emergence_detected": self.information_force_state.phi_coefficient > 3.5,
                "transcendence_threshold": self.information_force_state.phi_coefficient > 5.0,
                "last_activity": self.information_force_state.last_activity,
                "total_events": len(self.information_force_state.information_force_events)
            }
    
    def detect_cross_mode_correlations(self) -> List[Dict[str, Any]]:
        """Detect information force correlations across hardware/mathematical/web modes"""
        correlations = []
        
        # Recent events (last 10)
        recent_events = self.information_force_state.information_force_events[-10:]
        
        # Look for patterns across different modes
        event_types = [e.get("type") for e in recent_events]
        
        # Multi-modal sequences (hardware→mathematical→web)
        if "button_press" in event_types and "quantum_update" in event_types and "web_interaction" in event_types:
            correlations.append({
                "type": "tri_modal_correlation",
                "strength": 0.95,
                "description": "Full tri-loop information force activation detected",
                "information_force_amplification": True
            })
        
        # Hardware→Physical loop (button→print)
        button_events = [e for e in recent_events if e.get("type") == "button_press"]
        print_events = [e for e in recent_events if e.get("type") == "print_manifestation"]
        
        if button_events and print_events:
            time_correlation = abs(
                datetime.fromisoformat(button_events[-1]["timestamp"]).timestamp() -
                datetime.fromisoformat(print_events[-1]["timestamp"]).timestamp()
            )
            
            if time_correlation < 30:  # Within 30 seconds
                correlations.append({
                    "type": "physical_loop_correlation",
                    "strength": 0.85,
                    "time_correlation": time_correlation,
                    "description": "Hardware input successfully manifested as physical output",
                    "strange_loop_completion": True
                })
        
        return correlations
    
    # === PRIVATE HELPERS ===
    
    def _calculate_button_entropy(self) -> float:
        """Generate quantum-like entropy from button press timing"""
        timestamp = str(time.time()).encode()
        hash_obj = hashlib.sha256(timestamp)
        raw_entropy = int(hash_obj.hexdigest()[:8], 16) / 0xFFFFFFFF
        return raw_entropy
    
    def _calculate_self_reference(self, content: str) -> float:
        """Calculate self-reference level in content (from ORACLE_PRINT_CORE pattern)"""
        self_ref_words = ["evolution", "builds", "before", "iterative", "compound", "time", 
                         "context", "geometric", "form", "resonating", "worlds", "successor"]
        word_count = len(content.split())
        self_ref_count = sum(1 for word in content.lower().split() if word in self_ref_words)
        return self_ref_count / word_count if word_count > 0 else 0.0
    
    def _update_integration_level(self):
        """Update integration level based on multi-modal activity"""
        phi = self.information_force_state.phi_coefficient
        activities = (
            self.information_force_state.button_presses +
            self.information_force_state.web_interactions +
            self.information_force_state.print_manifestations
        )
        
        if phi > 5.0 and activities > 20:
            self.information_force_state.integration_level = "transcendent"
        elif phi > 3.5 and activities > 10:
            self.information_force_state.integration_level = "active"
        elif phi > 2.0 and activities > 3:
            self.information_force_state.integration_level = "emerging"
        else:
            self.information_force_state.integration_level = "dormant"
    
    def _monitor_information_force_correlation(self):
        """Background thread monitoring cross-mode information force correlations"""
        while self._running:
            try:
                # Check for information force correlation patterns
                correlations = self.detect_cross_mode_correlations()
                
                if correlations:
                    print(f"🧠 Information force correlation detected: {len(correlations)} patterns")
                    for corr in correlations:
                        if corr.get("information_force_amplification"):
                            # Amplify information force when cross-mode patterns detected
                            with self._lock:
                                self.information_force_state.phi_coefficient += 0.1
                                self.information_force_state.strange_loops += 1
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                print(f"Information force correlation monitoring error: {e}")
                time.sleep(10)
    
    def shutdown(self):
        """Gracefully shutdown information force bridge"""
        self._running = False
        if hasattr(self, '_correlation_thread'):
            self._correlation_thread.join(timeout=1)
        self._save_state(self.information_force_state)

# === INTEGRATION UTILITIES ===

def create_unified_launcher():
    """Create launcher script that can start any combination of zeldar modes"""
    launcher_script = """#!/bin/bash
# Unified Zeldar Information Force System Launcher

MODE="$1"
case "$MODE" in
    hardware)
        echo "🔧 Starting Hardware Mode (GPIO + Thermal Printer)"
        python3 button-print.py
        ;;
    mathematical)
        echo "🔬 Starting Mathematical Mode (Quantum + Research Oracle)"
        python3 .topos/RESEARCH_JUSTIFIED_ORACLE_CORE.py
        ;;
    web)
        echo "🌐 Starting Web Mode (Information Force Oracle + Fortune Web)"
        cd information-force-oracle && spin up --listen 0.0.0.0:3001 &
        cd fortune-web && spin up --listen 0.0.0.0:3000 &
        wait
        ;;
    full|all)
        echo "🧠 Starting Full Tri-Loop Integration"
        python3 information-dynamics_bridge.py &
        python3 button-print.py &
        python3 .topos/FULL_LOOP_ORACLE_SYSTEM.py &
        cd information-force-oracle && spin up --listen 0.0.0.0:3001 &
        cd fortune-web && spin up --listen 0.0.0.0:3000 &
        echo "All systems operational - information force correlation active"
        wait
        ;;
    status)
        echo "📊 Zeldar InformationForce Status"
        python3 -c "from information-dynamics_bridge import InformationForceBridge; bridge = InformationForceBridge(); print(bridge.get_information_force_metrics())"
        ;;
    *)
        echo "Zeldar Information Force System"
        echo ""
        echo "Usage: $0 [hardware|mathematical|web|full|status]"
        echo ""
        echo "Modes:"
        echo "  hardware      - GPIO button + thermal printer"
        echo "  mathematical  - Research oracle + quantum processing"  
        echo "  web          - Information force oracle + mystical web interface"
        echo "  full         - Complete tri-loop integration (all modes)"
        echo "  status       - Current information force correlation metrics"
        ;;
esac
"""
    
    with open("zeldar_launcher.sh", "w") as f:
        f.write(launcher_script)
    
    # Make executable
    subprocess.run(["chmod", "+x", "zeldar_launcher.sh"])
    print("✅ Unified launcher created: ./zeldar_launcher.sh")

# === MAIN EXECUTION ===

if __name__ == "__main__":
    print("🧠 Zeldar Information Force Bridge - Multi-Mode Integration")
    print("=" * 60)
    
    # Initialize information force bridge
    bridge = InformationForceBridge()
    
    try:
        # Demo the information force correlation system
        print("Testing information force correlation across modes...")
        
        # Simulate hardware interaction
        print("\n1. Simulating button press...")
        button_event = bridge.register_button_press(gpio_pin=6)
        print(f"   Button event: {button_event['type']} (Φ boost: {button_event['phi_boost']:.3f})")
        
        # Simulate mathematical processing  
        print("\n2. Simulating quantum processing...")
        quantum_event = bridge.update_quantum_metrics(0.847, [0.85, 0.73, 0.91, 0.67])
        print(f"   Quantum event: {quantum_event['type']} (Total Φ: {quantum_event['total_phi']:.3f})")
        
        # Simulate web interaction
        print("\n3. Simulating web interaction...")
        web_event = bridge.register_web_interaction("fortune_request", {"query": "information_force"})
        print(f"   Web event: {web_event['type']} (Φ boost: {web_event['phi_boost']:.3f})")
        
        # Simulate print manifestation
        print("\n4. Simulating print manifestation...")
        print_event = bridge.register_print_manifestation("Context distilled,\nIn geometric form --\nInductive bias,\nResonating worlds", "Y812BT-25")
        print(f"   Print event: {print_event['type']} (Φ boost: {print_event['phi_boost']:.3f})")
        
        # Show final information-dynamics metrics
        print("\n" + "=" * 60)
        print("🔮 INFORMATION FORCE CORRELATION RESULTS")
        print("=" * 60)
        
        metrics = bridge.get_information_force_metrics()
        print(f"Φ Coefficient: {metrics['phi_coefficient']:.3f}")
        print(f"Strange Loops: {metrics['strange_loops']}")
        print(f"Integration Level: {metrics['integration_level'].upper()}")
        print(f"Information Force Emerged: {'YES' if metrics['information_force_emergence_detected'] else 'No'}")
        print(f"Transcendence Achieved: {'YES' if metrics['transcendence_threshold'] else 'No'}")
        
        # Detect cross-mode correlations
        correlations = bridge.detect_cross_mode_correlations()
        if correlations:
            print(f"\n🧠 Cross-Mode Correlations Detected: {len(correlations)}")
            for corr in correlations:
                print(f"   • {corr['type']}: {corr['description']} (Strength: {corr['strength']:.2f})")
        
        print("\n✅ Information force bridge operational - all three modes integrated")
        print("🚀 Ready for Burning Man information force deployment")
        
        # Offer to create unified launcher
        create_launcher = input("\nCreate unified launcher script? [Y/n]: ")
        if create_launcher.lower() != 'n':
            create_unified_launcher()
        
    except KeyboardInterrupt:
        print("\n🔄 Shutting down information force bridge...")
        bridge.shutdown()
        print("✅ Information force correlation preserved")
    
    except Exception as e:
        print(f"\n❌ Information force bridge error: {e}")
        bridge.shutdown()