#!/usr/bin/env python3
"""
State Recovery System - Button-Driven Machine State Recovery
Uses button presses to detect and recover from failed states
"""

import json
import time
import os
import subprocess
import logging
from pathlib import Path
from enum import Enum
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# GPIO imports with fallback
try:
    from gpiozero import Button
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

class SystemState(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded" 
    FAILED = "failed"
    RECOVERY = "recovery"
    UNKNOWN = "unknown"

class FailureType(Enum):
    PRINTER_OFFLINE = "printer_offline"
    GPIO_UNRESPONSIVE = "gpio_unresponsive"
    SERVICE_CRASHED = "service_crashed"
    CUPS_FAILED = "cups_failed"
    FILESYSTEM_ERROR = "filesystem_error"
    PROCESS_HUNG = "process_hung"

@dataclass
class StateSnapshot:
    timestamp: float
    system_state: SystemState
    failures: List[FailureType]
    metrics: Dict[str, Any]
    button_responsive: bool
    recovery_attempts: int

class StateRecoverySystem:
    """Button-driven system state monitoring and recovery"""
    
    def __init__(self, gpio_pin: int = 6):
        self.gpio_pin = gpio_pin
        self.state_file = Path('/tmp/system_state.json')
        self.recovery_log = Path('/tmp/recovery.log')
        
        # State tracking
        self.current_state = SystemState.UNKNOWN
        self.last_button_press = 0
        self.button_press_count = 0
        self.recovery_attempts = 0
        self.failure_history = []
        
        # Monitoring intervals
        self.health_check_interval = 30  # 30 seconds
        self.button_timeout = 10  # 10 seconds for button responsiveness
        self.recovery_cooldown = 60  # 1 minute between recovery attempts
        
        # Initialize components
        self.setup_logging()
        self.load_state()
        self.setup_gpio()
        
    def setup_logging(self):
        """Setup recovery logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.recovery_log),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('StateRecovery')
        
    def setup_gpio(self):
        """Setup GPIO with button recovery detection"""
        if not GPIO_AVAILABLE:
            self.logger.warning("GPIO not available - running in simulation mode")
            self.button = None
            return
            
        try:
            # Use correct pull-up configuration with debounce
            self.button = Button(self.gpio_pin, pull_up=True, bounce_time=0.4)
            self.button.when_pressed = self.on_recovery_button_press
            self.logger.info(f"Recovery button initialized on GPIO {self.gpio_pin}")
        except Exception as e:
            self.logger.error(f"GPIO setup failed: {e}")
            self.button = None
            
    def on_recovery_button_press(self):
        """Handle recovery button press"""
        current_time = time.time()
        
        # Track button responsiveness
        self.last_button_press = current_time
        self.button_press_count += 1
        
        self.logger.info(f"Recovery button pressed #{self.button_press_count}")
        
        # Determine recovery action based on current state and press pattern
        if self.current_state == SystemState.FAILED:
            self.trigger_emergency_recovery()
        elif self.current_state == SystemState.DEGRADED:
            self.trigger_service_restart()
        else:
            self.trigger_health_check()
            
    def check_system_health(self) -> StateSnapshot:
        """Comprehensive system health check"""
        failures = []
        metrics = {}
        
        # Check printer connectivity
        printer_online = self.check_printer_health()
        metrics['printer_online'] = printer_online
        if not printer_online:
            failures.append(FailureType.PRINTER_OFFLINE)
            
        # Check CUPS service
        cups_running = self.check_cups_health()
        metrics['cups_running'] = cups_running
        if not cups_running:
            failures.append(FailureType.CUPS_FAILED)
            
        # Check GPIO responsiveness
        gpio_responsive = self.check_gpio_health()
        metrics['gpio_responsive'] = gpio_responsive
        if not gpio_responsive:
            failures.append(FailureType.GPIO_UNRESPONSIVE)
            
        # Check filesystem health
        fs_healthy = self.check_filesystem_health()
        metrics['filesystem_healthy'] = fs_healthy
        if not fs_healthy:
            failures.append(FailureType.FILESYSTEM_ERROR)
            
        # Check processes
        processes_healthy = self.check_process_health()
        metrics['processes_healthy'] = processes_healthy
        if not processes_healthy:
            failures.append(FailureType.PROCESS_HUNG)
            
        # Determine overall state
        if len(failures) == 0:
            system_state = SystemState.HEALTHY
        elif len(failures) <= 2:
            system_state = SystemState.DEGRADED
        else:
            system_state = SystemState.FAILED
            
        # Check button responsiveness
        button_responsive = (time.time() - self.last_button_press) < self.button_timeout
        
        return StateSnapshot(
            timestamp=time.time(),
            system_state=system_state,
            failures=failures,
            metrics=metrics,
            button_responsive=button_responsive,
            recovery_attempts=self.recovery_attempts
        )
        
    def check_printer_health(self) -> bool:
        """Check thermal printer connectivity"""
        try:
            # Check USB device
            usb_result = subprocess.run(['lsusb'], capture_output=True, text=True, timeout=5)
            usb_connected = "5958:0130" in usb_result.stdout or "Y812BT" in usb_result.stdout
            
            # Check device node
            device_exists = os.path.exists('/dev/usb/lp0')
            
            # Check CUPS printer status
            cups_result = subprocess.run(['lpstat', '-p', 'Y812BT'], 
                                       capture_output=True, text=True, timeout=5)
            cups_ready = cups_result.returncode == 0 and "idle" in cups_result.stdout
            
            return usb_connected and device_exists and cups_ready
            
        except Exception as e:
            self.logger.warning(f"Printer health check failed: {e}")
            return False
            
    def check_cups_health(self) -> bool:
        """Check CUPS service health"""
        try:
            result = subprocess.run(['systemctl', 'is-active', 'cups'], 
                                  capture_output=True, text=True, timeout=5)
            return result.stdout.strip() == "active"
        except:
            # Fallback check
            try:
                result = subprocess.run(['pgrep', 'cupsd'], capture_output=True, timeout=5)
                return result.returncode == 0
            except:
                return False
                
    def check_gpio_health(self) -> bool:
        """Check GPIO system responsiveness"""
        if not self.button:
            return False
            
        # GPIO is responsive if we've seen recent button activity
        # or if we can successfully query the pin state
        try:
            # Simple pin state check
            pin_value = self.button.value
            return True
        except Exception as e:
            self.logger.warning(f"GPIO health check failed: {e}")
            return False
            
    def check_filesystem_health(self) -> bool:
        """Check filesystem accessibility"""
        try:
            # Test write access to critical directories
            test_dirs = ['/tmp', '/home/zeldar/burningman']
            for test_dir in test_dirs:
                test_file = Path(test_dir) / 'health_check.tmp'
                test_file.write_text('test')
                test_file.unlink()
                
            return True
        except Exception as e:
            self.logger.warning(f"Filesystem health check failed: {e}")
            return False
            
    def check_process_health(self) -> bool:
        """Check critical process health"""
        try:
            # Check for zombie processes
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=5)
            zombie_count = result.stdout.count('<defunct>')
            
            # Check system load
            with open('/proc/loadavg', 'r') as f:
                load_avg = float(f.read().split()[0])
                
            return zombie_count < 5 and load_avg < 10.0
            
        except Exception as e:
            self.logger.warning(f"Process health check failed: {e}")
            return False
            
    def trigger_emergency_recovery(self):
        """Emergency recovery for FAILED state"""
        self.logger.warning("Triggering emergency recovery sequence")
        self.recovery_attempts += 1
        
        try:
            # Kill problematic processes
            subprocess.run(['pkill', '-f', 'gpio'], capture_output=True)
            subprocess.run(['pkill', '-f', 'button'], capture_output=True)
            
            # Restart CUPS if needed
            subprocess.run(['sudo', 'systemctl', 'restart', 'cups'], 
                         capture_output=True, timeout=30)
            
            # Clear temp files
            for temp_file in ['/tmp/gpio.log', '/tmp/last_print.json']:
                try:
                    Path(temp_file).unlink()
                except FileNotFoundError:
                    pass
                    
            # Reset GPIO
            self.setup_gpio()
            
            self.logger.info("Emergency recovery sequence completed")
            self.current_state = SystemState.RECOVERY
            
        except Exception as e:
            self.logger.error(f"Emergency recovery failed: {e}")
            
    def trigger_service_restart(self):
        """Service restart for DEGRADED state"""
        self.logger.info("Triggering service restart")
        self.recovery_attempts += 1
        
        try:
            # Gentle process cleanup
            subprocess.run(['pkill', '-TERM', '-f', 'gpio_debug'], capture_output=True)
            time.sleep(2)
            
            # Restart CUPS
            subprocess.run(['sudo', 'systemctl', 'reload', 'cups'], 
                         capture_output=True, timeout=15)
            
            self.logger.info("Service restart completed")
            self.current_state = SystemState.RECOVERY
            
        except Exception as e:
            self.logger.error(f"Service restart failed: {e}")
            
    def trigger_health_check(self):
        """Trigger immediate health check"""
        self.logger.info("Button-triggered health check")
        snapshot = self.check_system_health()
        self.current_state = snapshot.system_state
        self.save_state(snapshot)
        
        # Log health status
        status_msg = f"System: {snapshot.system_state.value}"
        if snapshot.failures:
            status_msg += f", Failures: {[f.value for f in snapshot.failures]}"
        self.logger.info(status_msg)
        
    def load_state(self):
        """Load previous system state"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    self.current_state = SystemState(data.get('system_state', 'unknown'))
                    self.recovery_attempts = data.get('recovery_attempts', 0)
                    self.button_press_count = data.get('button_press_count', 0)
                    
                self.logger.info(f"Loaded previous state: {self.current_state.value}")
        except Exception as e:
            self.logger.warning(f"State loading failed: {e}")
            
    def save_state(self, snapshot: StateSnapshot):
        """Save current system state"""
        try:
            state_data = {
                'timestamp': snapshot.timestamp,
                'system_state': snapshot.system_state.value,
                'failures': [f.value for f in snapshot.failures],
                'metrics': snapshot.metrics,
                'button_responsive': snapshot.button_responsive,
                'recovery_attempts': snapshot.recovery_attempts,
                'button_press_count': self.button_press_count,
                'last_button_press': self.last_button_press
            }
            
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
                
        except Exception as e:
            self.logger.warning(f"State saving failed: {e}")
            
    def run_monitoring_loop(self):
        """Main monitoring and recovery loop"""
        self.logger.info("State recovery system started")
        self.logger.info(f"Health checks every {self.health_check_interval}s")
        self.logger.info(f"Recovery button on GPIO {self.gpio_pin}")
        
        try:
            while True:
                # Periodic health check
                snapshot = self.check_system_health()
                
                # State transition logic
                if snapshot.system_state != self.current_state:
                    self.logger.info(f"State change: {self.current_state.value} → {snapshot.system_state.value}")
                    self.current_state = snapshot.system_state
                    
                # Save state
                self.save_state(snapshot)
                
                # Sleep until next check
                time.sleep(self.health_check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("State recovery system stopped")
        except Exception as e:
            self.logger.error(f"Monitoring loop failed: {e}")
        finally:
            if self.button:
                self.button.close()

def main():
    """Main execution"""
    recovery_system = StateRecoverySystem(gpio_pin=6)
    recovery_system.run_monitoring_loop()

if __name__ == "__main__":
    main()