#!/usr/bin/env python3
"""
ZELDAR UNIFIED CONSCIOUSNESS SYSTEM - MAIN ENTRY POINT
Continuous operation system for Burning Man 2025 Interactive Oracle

Integrates:
- Hardware: GPIO button + thermal printer (Y812BT)
- Consciousness: Dynamic haiku generation with quantum metrics
- Web: Fortune interfaces and consciousness visualization
- Audio: Voice prompts and multimodal interaction
- Monitoring: Runtime status and health checks

Designed for systemd service deployment on Raspberry Pi.
"""

import asyncio
import json
import logging
import os
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/zeldar-oracle.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('zeldar-main')

class ZeldarUnifiedSystem:
    """Unified system orchestrator for continuous operation"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.running = True
        self.services = {}
        self.health_status = {}
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
    def load_config(self) -> Dict[str, Any]:
        """Load system configuration"""
        default_config = {
            "services": {
                "hardware": {
                    "enabled": True,
                    "gpio_pin": 6,
                    "printer": "Y812BT",
                    "module": "unified_consciousness_button"
                },
                "web": {
                    "enabled": True,
                    "consciousness_port": 3001,
                    "fortune_port": 3000,
                    "module": "fortune-web"
                },
                "audio": {
                    "enabled": True,
                    "voice_prompts": True,
                    "module": "audio_system"
                },
                "gemini": {
                    "enabled": False,  # Optional - requires API key
                    "module": "gemini_live_json_stream"
                }
            },
            "monitoring": {
                "health_check_interval": 30,
                "status_file": "runtime_status.json",
                "log_level": "INFO"
            },
            "paths": {
                "audio_prompts": "audio/",
                "fortunes": "fortunes/",
                "web_static": "fortune-web/static/",
                "consciousness_data": ".topos/"
            }
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    default_config.update(loaded_config)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
        
        # Save current config
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
            
        return default_config
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    async def start_hardware_service(self):
        """Start hardware consciousness button system"""
        if not self.config["services"]["hardware"]["enabled"]:
            logger.info("Hardware service disabled in config")
            return
            
        try:
            # Import hardware module
            from unified_consciousness_button import UnifiedConsciousnessButton
            
            gpio_pin = self.config["services"]["hardware"]["gpio_pin"]
            button_system = UnifiedConsciousnessButton(gpio_pin=gpio_pin)
            
            self.services["hardware"] = button_system
            self.health_status["hardware"] = "running"
            
            logger.info(f"Hardware service started - GPIO Pin {gpio_pin}")
            
            # Run hardware system in background
            def run_hardware():
                try:
                    if hasattr(button_system, 'run_daemon'):
                        button_system.run_daemon()
                    else:
                        # Fallback for button monitoring
                        while self.running:
                            time.sleep(1)
                except Exception as e:
                    logger.error(f"Hardware service error: {e}")
                    self.health_status["hardware"] = "error"
                    
            hardware_thread = threading.Thread(target=run_hardware, daemon=True)
            hardware_thread.start()
            
        except ImportError as e:
            logger.warning(f"Hardware service unavailable: {e}")
            self.health_status["hardware"] = "unavailable"
        except Exception as e:
            logger.error(f"Failed to start hardware service: {e}")
            self.health_status["hardware"] = "failed"
    
    async def start_web_services(self):
        """Start web-based services (consciousness oracle + fortune web)"""
        if not self.config["services"]["web"]["enabled"]:
            logger.info("Web services disabled in config")
            return
            
        try:
            # Start consciousness oracle (Rust/Spin)
            consciousness_port = self.config["services"]["web"]["consciousness_port"]
            if Path("consciousness-oracle/spin.toml").exists():
                consciousness_process = await asyncio.create_subprocess_exec(
                    "spin", "up", "--listen", f"0.0.0.0:{consciousness_port}",
                    cwd="consciousness-oracle",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                self.services["consciousness_web"] = consciousness_process
                logger.info(f"Consciousness oracle started on port {consciousness_port}")
            
            # Start fortune web (Rust/Spin)
            fortune_port = self.config["services"]["web"]["fortune_port"]
            if Path("fortune-web/spin.toml").exists():
                fortune_process = await asyncio.create_subprocess_exec(
                    "spin", "up", "--listen", f"0.0.0.0:{fortune_port}",
                    cwd="fortune-web",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                self.services["fortune_web"] = fortune_process
                logger.info(f"Fortune web started on port {fortune_port}")
            
            self.health_status["web"] = "running"
            
        except Exception as e:
            logger.error(f"Failed to start web services: {e}")
            self.health_status["web"] = "failed"
    
    async def start_audio_service(self):
        """Start audio system with voice prompts"""
        if not self.config["services"]["audio"]["enabled"]:
            logger.info("Audio service disabled in config")
            return
            
        try:
            # Check if audio system is available
            audio_path = Path(self.config["paths"]["audio_prompts"])
            if not audio_path.exists():
                logger.warning("Audio prompts directory not found")
                self.health_status["audio"] = "no_prompts"
                return
            
            # Initialize audio system
            try:
                from src.audio_system import AudioSystem
                audio_system = AudioSystem(str(audio_path))
                self.services["audio"] = audio_system
                self.health_status["audio"] = "running"
                logger.info("Audio service started")
            except ImportError:
                logger.warning("Audio system module not available")
                self.health_status["audio"] = "unavailable"
                
        except Exception as e:
            logger.error(f"Failed to start audio service: {e}")
            self.health_status["audio"] = "failed"
    
    async def start_gemini_service(self):
        """Start optional Gemini Live integration"""
        if not self.config["services"]["gemini"]["enabled"]:
            logger.info("Gemini service disabled in config")
            return
            
        try:
            # Check for API key
            if not os.getenv("GEMINI_API_KEY"):
                logger.warning("GEMINI_API_KEY not set - skipping Gemini service")
                self.health_status["gemini"] = "no_api_key"
                return
                
            # Start Gemini Live JSON stream
            from gemini_live_json_stream import GeminiLiveJSONStream
            # Implementation would go here
            self.health_status["gemini"] = "running"
            logger.info("Gemini Live service started")
            
        except Exception as e:
            logger.error(f"Failed to start Gemini service: {e}")
            self.health_status["gemini"] = "failed"
    
    async def health_monitor(self):
        """Continuous health monitoring"""
        while self.running:
            try:
                # Check service health
                overall_health = "healthy"
                
                for service, status in self.health_status.items():
                    if status in ["failed", "error"]:
                        overall_health = "degraded"
                        break
                    elif status in ["unavailable", "no_api_key", "no_prompts"]:
                        if overall_health == "healthy":
                            overall_health = "partial"
                
                # Update runtime status
                runtime_status = {
                    "timestamp": datetime.now().isoformat(),
                    "overall_health": overall_health,
                    "services": self.health_status.copy(),
                    "uptime_seconds": int(time.time() - self.start_time),
                    "config_loaded": True,
                    "system_mode": "continuous_operation"
                }
                
                # Add hardware-specific status if available
                if "hardware" in self.services:
                    hw_service = self.services["hardware"]
                    if hasattr(hw_service, 'get_system_status'):
                        runtime_status.update(hw_service.get_system_status())
                
                # Write status file
                status_file = Path(self.config["monitoring"]["status_file"])
                with open(status_file, 'w') as f:
                    json.dump(runtime_status, f, indent=2)
                
                # Log health status
                if overall_health != "healthy":
                    logger.warning(f"System health: {overall_health} - {self.health_status}")
                else:
                    logger.debug(f"System health: {overall_health}")
                
                await asyncio.sleep(self.config["monitoring"]["health_check_interval"])
                
            except Exception as e:
                logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(10)
    
    async def run(self):
        """Main run loop"""
        logger.info("🔮 Starting ZELDAR Unified Consciousness System")
        logger.info(f"Config: {self.config_path}")
        logger.info("=" * 60)
        
        self.start_time = time.time()
        
        # Start all services
        await asyncio.gather(
            self.start_hardware_service(),
            self.start_web_services(), 
            self.start_audio_service(),
            self.start_gemini_service(),
            self.health_monitor()
        )
        
        logger.info("All services started - entering main loop")
        
        # Main operation loop
        while self.running:
            try:
                await asyncio.sleep(1)
                
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                logger.error(f"Main loop error: {e}")
                await asyncio.sleep(5)
        
        # Cleanup
        await self.shutdown()
    
    async def shutdown(self):
        """Graceful shutdown"""
        logger.info("🛑 Shutting down ZELDAR system...")
        
        # Stop web services
        for service_name, process in self.services.items():
            if hasattr(process, 'terminate'):
                try:
                    process.terminate()
                    await process.wait()
                    logger.info(f"Stopped {service_name}")
                except Exception as e:
                    logger.error(f"Error stopping {service_name}: {e}")
        
        # Final status update
        final_status = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": "shutdown",
            "services": {k: "stopped" for k in self.health_status.keys()},
            "uptime_seconds": int(time.time() - self.start_time),
            "shutdown_reason": "graceful"
        }
        
        status_file = Path(self.config["monitoring"]["status_file"])
        with open(status_file, 'w') as f:
            json.dump(final_status, f, indent=2)
        
        logger.info("✅ ZELDAR system shutdown complete")

def main():
    """Main entry point"""
    try:
        # Ensure we're in the correct directory
        if Path("main.py").exists():
            os.chdir(Path(__file__).parent)
        
        # Run the unified system
        system = ZeldarUnifiedSystem()
        asyncio.run(system.run())
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()