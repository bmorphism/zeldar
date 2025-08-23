#!/usr/bin/env python3
"""
Deploy Research Oracle - Complete System Integration
Combines web interface, quantum backend, and physical button printing
"""

import subprocess
import threading
import time
import json
import os
import signal
import sys
from pathlib import Path

class ResearchOracleDeployment:
    """Complete deployment orchestration for the Zeldar research oracle"""
    
    def __init__(self):
        self.processes = {}
        self.running = True
        self.deployment_log = []
        
    def log_deployment(self, message: str, level: str = "INFO"):
        """Log deployment events"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        print(log_entry)
        self.deployment_log.append(log_entry)
    
    def check_prerequisites(self) -> bool:
        """Check all system prerequisites"""
        self.log_deployment("Checking system prerequisites...", "INFO")
        
        checks = {
            "Python 3": self._check_python(),
            "Node.js/npm": self._check_node(),
            "Spin CLI": self._check_spin(),
            "CUPS printing": self._check_cups(),
            "GPIO hardware": self._check_gpio()
        }
        
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            self.log_deployment(f"{status} {check_name}: {'Available' if result else 'Not available'}")
        
        return all(checks.values())
    
    def _check_python(self) -> bool:
        """Check Python 3 availability"""
        try:
            result = subprocess.run(['python3', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def _check_node(self) -> bool:
        """Check Node.js/npm availability"""
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def _check_spin(self) -> bool:
        """Check Spin CLI availability"""
        try:
            result = subprocess.run(['spin', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def _check_cups(self) -> bool:
        """Check CUPS printing system"""
        try:
            result = subprocess.run(['lpstat', '-d'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def _check_gpio(self) -> bool:
        """Check GPIO hardware availability"""
        try:
            import gpiozero
            return True
        except ImportError:
            return False
    
    def deploy_quantum_backend(self) -> bool:
        """Deploy the Python quantum oracle backend"""
        self.log_deployment("Starting quantum oracle backend...", "INFO")
        
        try:
            # Start the full loop oracle system in simulation mode
            cmd = [sys.executable, "FULL_LOOP_ORACLE_SYSTEM.py", "--daemon"]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes['quantum_backend'] = process
            self.log_deployment("Quantum backend started successfully", "SUCCESS")
            return True
            
        except Exception as e:
            self.log_deployment(f"Failed to start quantum backend: {e}", "ERROR")
            return False
    
    def deploy_web_frontend(self) -> bool:
        """Deploy the Spin web frontend"""
        self.log_deployment("Starting web frontend...", "INFO")
        
        try:
            # Change to fortune-web directory
            web_dir = Path("fortune-web")
            if not web_dir.exists():
                self.log_deployment("fortune-web directory not found", "ERROR")
                return False
            
            # Start Spin application
            cmd = ["spin", "up", "--listen", "127.0.0.1:3001"]
            process = subprocess.Popen(
                cmd,
                cwd=web_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes['web_frontend'] = process
            self.log_deployment("Web frontend started on http://127.0.0.1:3001", "SUCCESS")
            return True
            
        except Exception as e:
            self.log_deployment(f"Failed to start web frontend: {e}", "ERROR")
            return False
    
    def deploy_bridge_server(self) -> bool:
        """Deploy the quantum-web bridge server"""
        self.log_deployment("Starting quantum-web bridge...", "INFO")
        
        try:
            # Start the bridge server
            cmd = [sys.executable, "fortune-web/quantum_bridge.py"]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes['bridge_server'] = process
            self.log_deployment("Bridge server started on http://127.0.0.1:3000", "SUCCESS")
            return True
            
        except Exception as e:
            self.log_deployment(f"Failed to start bridge server: {e}", "ERROR")
            return False
    
    def deploy_physical_interface(self) -> bool:
        """Deploy physical button interface if GPIO available"""
        self.log_deployment("Checking physical interface...", "INFO")
        
        if not self._check_gpio():
            self.log_deployment("GPIO not available - skipping physical interface", "WARN")
            return True
        
        try:
            # Start button interface
            cmd = [sys.executable, "button_quick_phrase_trigger.py"]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes['physical_interface'] = process
            self.log_deployment("Physical button interface started (GPIO Pin 6)", "SUCCESS")
            return True
            
        except Exception as e:
            self.log_deployment(f"Failed to start physical interface: {e}", "ERROR")
            return False
    
    def monitor_system_health(self):
        """Monitor all deployed components"""
        self.log_deployment("Starting system health monitoring...", "INFO")
        
        while self.running:
            try:
                # Check each process
                for name, process in self.processes.items():
                    if process.poll() is not None:
                        self.log_deployment(f"{name} process terminated unexpectedly", "ERROR")
                        # Attempt restart
                        self._restart_component(name)
                
                # Wait before next check
                time.sleep(30)
                
            except KeyboardInterrupt:
                self.log_deployment("Health monitoring interrupted", "INFO")
                break
    
    def _restart_component(self, component_name: str):
        """Attempt to restart a failed component"""
        self.log_deployment(f"Attempting to restart {component_name}...", "INFO")
        
        # Remove failed process
        if component_name in self.processes:
            del self.processes[component_name]
        
        # Restart based on component type
        if component_name == 'quantum_backend':
            self.deploy_quantum_backend()
        elif component_name == 'web_frontend':
            self.deploy_web_frontend()
        elif component_name == 'bridge_server':
            self.deploy_bridge_server()
        elif component_name == 'physical_interface':
            self.deploy_physical_interface()
    
    def create_system_status_endpoint(self):
        """Create a simple status endpoint"""
        status = {
            "deployment_time": time.time(),
            "components": {
                name: "running" if process.poll() is None else "stopped"
                for name, process in self.processes.items()
            },
            "endpoints": {
                "web_interface": "http://127.0.0.1:3001",
                "api_bridge": "http://127.0.0.1:3000/api/health",
                "consciousness_status": "http://127.0.0.1:3000/api/consciousness/status"
            },
            "physical_interface": self._check_gpio(),
            "printing_available": self._check_cups()
        }
        
        # Write status file
        with open("deployment_status.json", "w") as f:
            json.dump(status, f, indent=2)
        
        return status
    
    def deploy_complete_system(self):
        """Deploy the complete research oracle system"""
        self.log_deployment("🔮 Starting Zeldar Research Oracle Deployment", "INFO")
        self.log_deployment("=" * 60, "INFO")
        
        # Check prerequisites
        if not self.check_prerequisites():
            self.log_deployment("Prerequisites not met - deployment aborted", "ERROR")
            return False
        
        # Deploy components
        deployment_steps = [
            ("Quantum Backend", self.deploy_quantum_backend),
            ("Bridge Server", self.deploy_bridge_server),
            ("Web Frontend", self.deploy_web_frontend),
            ("Physical Interface", self.deploy_physical_interface)
        ]
        
        success_count = 0
        for step_name, deploy_func in deployment_steps:
            if deploy_func():
                success_count += 1
            else:
                self.log_deployment(f"Deployment step failed: {step_name}", "ERROR")
        
        # Create status endpoint
        status = self.create_system_status_endpoint()
        
        # Summary
        self.log_deployment("=" * 60, "INFO")
        self.log_deployment(f"Deployment Summary: {success_count}/{len(deployment_steps)} components started", "INFO")
        
        if success_count >= 2:  # At least basic functionality
            self.log_deployment("🚀 Zeldar Research Oracle is OPERATIONAL!", "SUCCESS")
            self.log_deployment("Web Interface: http://127.0.0.1:3001", "INFO")
            self.log_deployment("API Bridge: http://127.0.0.1:3000/api/health", "INFO")
            
            # Start monitoring
            monitor_thread = threading.Thread(target=self.monitor_system_health, daemon=True)
            monitor_thread.start()
            
            return True
        else:
            self.log_deployment("❌ Deployment failed - insufficient components started", "ERROR")
            return False
    
    def shutdown_system(self):
        """Gracefully shutdown all components"""
        self.log_deployment("🛑 Shutting down Zeldar Research Oracle...", "INFO")
        self.running = False
        
        for name, process in self.processes.items():
            try:
                self.log_deployment(f"Stopping {name}...", "INFO")
                process.terminate()
                
                # Wait for graceful shutdown
                try:
                    process.wait(timeout=10)
                    self.log_deployment(f"{name} stopped gracefully", "INFO")
                except subprocess.TimeoutExpired:
                    # Force kill if needed
                    process.kill()
                    self.log_deployment(f"{name} force killed", "WARN")
                    
            except Exception as e:
                self.log_deployment(f"Error stopping {name}: {e}", "ERROR")
        
        # Save deployment log
        with open(f"deployment_log_{int(time.time())}.txt", "w") as f:
            f.write("\n".join(self.deployment_log))
        
        self.log_deployment("🌙 Zeldar Research Oracle shutdown complete", "INFO")

def main():
    """Main deployment function"""
    deployment = ResearchOracleDeployment()
    
    def signal_handler(signum, frame):
        deployment.shutdown_system()
        sys.exit(0)
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        if deployment.deploy_complete_system():
            print("\n🎯 System deployed successfully!")
            print("Press Ctrl+C to shutdown...")
            
            # Keep main thread alive
            while deployment.running:
                time.sleep(1)
        else:
            print("\n❌ Deployment failed!")
            return 1
            
    except KeyboardInterrupt:
        deployment.shutdown_system()
        return 0

if __name__ == "__main__":
    exit(main())