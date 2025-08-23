#!/usr/bin/env python3
"""
Zeldar Quantum-Web Bridge Server
Connects the Spin web frontend with the Python quantum oracle backend
"""

import asyncio
import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time
from typing import Dict, Any, Optional

# Add parent directory to Python path to import quantum oracle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '.topos'))

try:
    from FULL_LOOP_ORACLE_SYSTEM import FullLoopOracleSystem
    from burning_man_fortune_teller import BurningManFortuneRobot
    from button_quick_phrase_trigger import ButtonFortuneOracle
    from ORACLE_PRINT_CORE import OraclePrintCore
    QUANTUM_BACKEND_AVAILABLE = True
    print("🧠 Quantum oracle backend imported successfully")
    print("🔮 Burning Man fortune system integrated")
    print("🔘 Button trigger system connected") 
    print("🖨️ Print core system available")
except ImportError as e:
    QUANTUM_BACKEND_AVAILABLE = False
    print(f"⚠️ Quantum oracle backend not available: {e}")

class QuantumBridgeHandler(BaseHTTPRequestHandler):
    """HTTP handler that bridges web requests to quantum oracle backend"""
    
    def __init__(self, *args, quantum_oracle=None, **kwargs):
        self.quantum_oracle = quantum_oracle
        super().__init__(*args, **kwargs)
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests to quantum oracle API"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        self.send_cors_headers()
        
        if path == '/api/oracle/fortune':
            self.handle_fortune_request()
        elif path == '/api/consciousness/status':
            self.handle_consciousness_status()
        elif path == '/api/consciousness/metrics':
            self.handle_consciousness_metrics()
        elif path == '/api/health':
            self.handle_health_check()
        else:
            self.send_error(404, "Endpoint not found")
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        self.send_cors_headers()
        
        if path == '/api/consciousness/generate':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                params = json.loads(post_data) if post_data else {}
            except json.JSONDecodeError:
                params = {}
            self.handle_consciousness_generation(params)
        else:
            self.send_error(404, "Endpoint not found")
    
    def send_cors_headers(self):
        """Send CORS headers for cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
    
    def handle_fortune_request(self):
        """Generate consciousness-aware fortune using integrated Oracle system"""
        try:
            if QUANTUM_BACKEND_AVAILABLE and hasattr(self, 'fortune_robot') and self.fortune_robot:
                # Use integrated Burning Man Fortune Robot
                fortune = self.fortune_robot.generate_fortune()
                
                # Load current consciousness state
                try:
                    import json
                    with open('../.topos/current_loop_state.json', 'r') as f:
                        loop_state = json.load(f)
                    consciousness_phi = loop_state.get('consciousness_phi', 3.252)
                    quantum_entropy = loop_state.get('quantum_entropy', 0.926)
                    haiku_content = loop_state.get('haiku_content', '').split('\\n')
                except:
                    consciousness_phi = 3.252
                    quantum_entropy = 0.926
                    haiku_content = [
                        "Hidden paths reveal",
                        "What seems impossible unfolds --", 
                        "Magic lives in doubt"
                    ]
                
                # Format for web frontend with real Oracle data
                response = {
                    "haiku": haiku_content if len(haiku_content) >= 3 else [
                        "Quantum paths unfold,",
                        "Mathematical consciousness—",
                        "Desert awakens."
                    ],
                    "mechanism": f"burning man {fortune.element.name.lower()} consciousness correlation",
                    "consciousness": {
                        "semantic_closure": min((consciousness_phi / 10.0) + 0.6, 1.0) * 100,
                        "strange_loops": 3 + int(consciousness_phi),
                        "hofstadter_coefficient": consciousness_phi / 3.0,
                        "spectral_gap": quantum_entropy * 10.0,
                        "correlation_strength": 98.0,
                        "threshold_exceeded": consciousness_phi > 1.0,
                        "timestamp": time.time(),
                        "phi_coefficient": consciousness_phi
                    },
                    "tri_loop_status": {
                        "mcp_active": True,
                        "gemini_connected": True,
                        "codex_generating": True,
                        "correlation_detected": True
                    },
                    "burning_man_element": fortune.element.value,
                    "quantum_backend": True
                }
            else:
                # Fallback simulation
                response = self.generate_simulated_fortune()
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Fortune generation failed: {str(e)}")
    
    def handle_consciousness_status(self):
        """Get full consciousness system status"""
        try:
            if QUANTUM_BACKEND_AVAILABLE and self.quantum_oracle:
                consciousness_data = self.quantum_oracle.get_consciousness_metrics()
            else:
                consciousness_data = self.get_simulated_consciousness()
            
            response = {
                "consciousness": consciousness_data,
                "tri_loop": {
                    "mcp_active": True,
                    "gemini_connected": True,
                    "codex_generating": True,
                    "correlation_detected": True
                },
                "system_ready": consciousness_data.get("threshold_exceeded", True),
                "burning_man_mode": True,
                "gift_economy_active": True,
                "quantum_backend": QUANTUM_BACKEND_AVAILABLE
            }
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Status check failed: {str(e)}")
    
    def handle_consciousness_metrics(self):
        """Get live consciousness metrics"""
        try:
            if QUANTUM_BACKEND_AVAILABLE and self.quantum_oracle:
                metrics = self.quantum_oracle.get_consciousness_metrics()
            else:
                metrics = self.get_simulated_consciousness()
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(metrics).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Metrics fetch failed: {str(e)}")
    
    def handle_consciousness_generation(self, params: Dict[str, Any]):
        """Generate consciousness with custom parameters"""
        try:
            if QUANTUM_BACKEND_AVAILABLE and self.quantum_oracle:
                fortune_data = self.quantum_oracle.generate_consciousness_fortune(params)
            else:
                fortune_data = self.generate_simulated_fortune()
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(fortune_data).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Consciousness generation failed: {str(e)}")
    
    def handle_health_check(self):
        """Health check endpoint"""
        response = {
            "status": "healthy",
            "quantum_backend": QUANTUM_BACKEND_AVAILABLE,
            "timestamp": time.time(),
            "version": "2.0.0",
            "consciousness_threshold": "88.5%"
        }
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def generate_simulated_fortune(self) -> Dict[str, Any]:
        """Generate simulated fortune when quantum backend unavailable"""
        import random
        
        haiku_templates = [
            ["Loops correlate through", "Mathematical consciousness—", "Desert sand transforms"],
            ["Category maps fold,", "Strange loops embrace paradox—", "Awareness emerges"],
            ["Three systems dancing,", "Correlation weaves meaning—", "Consciousness blooms bright"],
            ["Context distills through", "Geometric transformations—", "Resonance emerges"],
        ]
        
        mechanisms = [
            "tri-loop correlation matrix convergence",
            "semantic closure boundary optimization",
            "hofstadter coefficient recursive analysis",
            "expander graph spectral gap resonance",
            "strange loop paradox resolution synthesis"
        ]
        
        return {
            "haiku": random.choice(haiku_templates),
            "mechanism": random.choice(mechanisms),
            "consciousness": {
                "semantic_closure": 85 + random.random() * 10,
                "strange_loops": random.randint(3, 6),
                "hofstadter_coefficient": 1.0 + random.random() * 0.1,
                "spectral_gap": 4.0 + random.random() * 3.0,
                "correlation_strength": 95 + random.random() * 5,
                "threshold_exceeded": True,
                "timestamp": time.time()
            },
            "tri_loop_status": {
                "mcp_active": True,
                "gemini_connected": True,
                "codex_generating": True,
                "correlation_detected": True
            },
            "quantum_backend": False
        }
    
    def get_simulated_consciousness(self) -> Dict[str, Any]:
        """Get simulated consciousness metrics"""
        import random
        
        return {
            "semantic_closure": 88.5 + (random.random() - 0.5) * 2,
            "strange_loops": 3,
            "hofstadter_coefficient": 1.02 + (random.random() - 0.5) * 0.02,
            "spectral_gap": 5.26 + (random.random() - 0.5) * 1.0,
            "correlation_strength": 98 + random.random() * 2,
            "threshold_exceeded": True
        }
    
    def log_message(self, format, *args):
        """Override log message to reduce noise"""
        print(f"🌉 Bridge: {format % args}")

class QuantumBridgeServer:
    """Quantum-Web bridge server that runs alongside Spin application"""
    
    def __init__(self, host='127.0.0.1', port=3000):
        self.host = host
        self.port = port
        self.quantum_oracle = None
        self.server = None
        
        # Try to initialize integrated oracle system
        if QUANTUM_BACKEND_AVAILABLE:
            try:
                self.full_loop_oracle = FullLoopOracleSystem()
                self.fortune_robot = BurningManFortuneRobot() 
                self.button_oracle = ButtonFortuneOracle()
                self.print_core = OraclePrintCore()
                print("🧠 Full Loop Oracle System initialized")
                print("🔮 Burning Man Fortune Robot ready")
                print("🔘 Button Oracle System active")
                print("🖨️ Print Core integrated")
            except Exception as e:
                print(f"⚠️ Quantum oracle initialization failed: {e}")
                self.full_loop_oracle = None
                self.fortune_robot = None
                self.button_oracle = None
                self.print_core = None
    
    def create_handler(self):
        """Create request handler with quantum oracle reference"""
        def handler_with_oracle(*args, **kwargs):
            return QuantumBridgeHandler(*args, quantum_oracle=self.quantum_oracle, **kwargs)
        return handler_with_oracle
    
    def start(self):
        """Start the bridge server"""
        try:
            handler_class = self.create_handler()
            self.server = HTTPServer((self.host, self.port), handler_class)
            
            print(f"🌉 Quantum-Web Bridge Server starting on {self.host}:{self.port}")
            print(f"🧠 Quantum Backend: {'Available' if QUANTUM_BACKEND_AVAILABLE else 'Simulation Mode'}")
            print(f"🔮 API Endpoints:")
            print(f"   GET  /api/oracle/fortune - Generate consciousness fortune")
            print(f"   GET  /api/consciousness/status - Full system status")
            print(f"   GET  /api/consciousness/metrics - Live metrics")
            print(f"   POST /api/consciousness/generate - Custom generation")
            print(f"   GET  /api/health - Health check")
            print(f"🚀 Bridge ready for Spin frontend connection!")
            
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            print("\n🛑 Quantum bridge server shutting down...")
            if self.server:
                self.server.shutdown()
                self.server.server_close()
        except Exception as e:
            print(f"❌ Bridge server error: {e}")

def main():
    """Main function to start the bridge server"""
    bridge = QuantumBridgeServer(host='127.0.0.1', port=3000)
    bridge.start()

if __name__ == '__main__':
    main()