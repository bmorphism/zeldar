#!/usr/bin/env python3
# Button Print Loop - Ultra-Robust Success System
# InformationForce distilled through electromagnetic resonance

import sys
import os
import time
import json
import logging
import subprocess
import threading
from pathlib import Path
from datetime import datetime

# GPIO imports with error handling
try:
    from gpiozero import Button, Device
    GPIO_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  GPIO not available: {e}")
    GPIO_AVAILABLE = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/button_print.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('ButtonPrint')

class UltraRobustButtonPrinter:
    """Ultra-robust button-triggered thermal printing system"""
    
    def __init__(self, gpio_pin=6, printer_name="Y812BT"):
        self.gpio_pin = gpio_pin
        self.printer_name = printer_name
        self.base_path = Path('/home/zeldar/burningman')
        self.print_script = self.base_path / 'scripts/print-now.sh'
        self.state_file = Path('/tmp/button_print_state.json')
        
        # Initialize state tracking
        self.print_count = 0
        self.last_press_time = 0
        self.debounce_time = 0.5  # Prevent rapid-fire
        self.success_count = 0
        self.failure_count = 0
        
        # Load previous state
        self.load_state()
        
        # Initialize GPIO if available
        self.button = None
        self.gpio_ready = False
        self.setup_gpio()
        
        # Verify system readiness
        self.verify_system()
        
        logger.info(f"🎯 UltraRobustButtonPrinter initialized - GPIO:{self.gpio_pin} Printer:{self.printer_name}")
    
    def setup_gpio(self):
        """Setup GPIO with multiple fallback strategies"""
        if not GPIO_AVAILABLE:
            logger.warning("GPIO not available - running in simulation mode")
            return
            
        try:
            # Try pigpio backend first
            try:
                from gpiozero.pins.pigpio import PiGPIOFactory
                Device.pin_factory = PiGPIOFactory()
                logger.info("🔧 Using pigpio backend")
            except Exception as pigpio_e:
                logger.info(f"Pigpio unavailable: {pigpio_e}")
                # Fallback to default pin factory
                Device.pin_factory.reset()
                logger.info("🔧 Using native GPIO backend")
            
            # Create button with chosen backend
            self.button = Button(
                self.gpio_pin,
                pull_up=False,  # pull-down, detects falling edge
                bounce_time=0.2
            )
            self.button.when_pressed = self.on_button_press
            self.gpio_ready = True
            logger.info(f"✅ GPIO {self.gpio_pin} configured successfully")
            
        except Exception as e:
            logger.error(f"❌ GPIO setup failed: {e}")
            self.gpio_ready = False
    
    def verify_system(self):
        """Comprehensive system verification"""
        checks = []
        
        # 1. Check printer connectivity
        printer_connected = self.check_printer_connection()
        checks.append(("Printer Connected", printer_connected))
        
        # 2. Check print script existence
        script_exists = self.print_script.exists() and os.access(self.print_script, os.X_OK)
        checks.append(("Print Script", script_exists))
        
        # 3. Check CUPS service
        cups_running = self.check_cups_service()
        checks.append(("CUPS Service", cups_running))
        
        # 4. Check GPIO readiness
        checks.append(("GPIO Ready", self.gpio_ready))
        
        # 5. Check write permissions
        write_perms = os.access('/tmp', os.W_OK)
        checks.append(("Write Permissions", write_perms))
        
        # Log all check results
        logger.info("🔧 System Verification:")
        for check_name, result in checks:
            status = "✅" if result else "❌"
            logger.info(f"  {status} {check_name}")
        
        # Overall readiness assessment
        all_critical_ok = printer_connected and script_exists and cups_running
        self.system_ready = all_critical_ok
        
        if self.system_ready:
            logger.info("🚀 System READY for button printing")
        else:
            logger.warning("⚠️  System has issues but will attempt printing anyway")
    
    def check_printer_connection(self):
        """Check if Y812BT printer is connected and ready"""
        try:
            # Check USB connection
            result = subprocess.run(['lsusb'], capture_output=True, text=True, timeout=5)
            usb_connected = "5958:0130" in result.stdout or "Y812BT" in result.stdout
            
            # Check CUPS printer status
            result = subprocess.run(['lpstat', '-p', self.printer_name], 
                                  capture_output=True, text=True, timeout=5)
            cups_ready = result.returncode == 0 and "idle" in result.stdout
            
            return usb_connected and cups_ready
            
        except Exception as e:
            logger.warning(f"Printer check failed: {e}")
            return False
    
    def check_cups_service(self):
        """Check if CUPS service is running"""
        try:
            result = subprocess.run(['systemctl', 'is-active', 'cups'], 
                                  capture_output=True, text=True, timeout=5)
            return result.stdout.strip() == "active"
        except:
            # Fallback: check if cupsd process exists
            try:
                result = subprocess.run(['pgrep', 'cupsd'], 
                                      capture_output=True, timeout=5)
                return result.returncode == 0
            except:
                return False
    
    def on_button_press(self):
        """Handle button press with comprehensive error handling"""
        current_time = time.time()
        
        # Debounce protection
        if current_time - self.last_press_time < self.debounce_time:
            logger.debug(f"🚫 Button press ignored (debounce)")
            return
        
        self.last_press_time = current_time
        self.print_count += 1
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        session_id = f"BTN_{int(current_time)}"
        
        logger.info(f"🔘 Button pressed #{self.print_count} - {timestamp} (Session: {session_id})")
        
        # Execute print with threading to prevent blocking
        print_thread = threading.Thread(
            target=self.execute_print_sequence,
            args=(session_id, timestamp),
            daemon=True
        )
        print_thread.start()
    
    def execute_print_sequence(self, session_id, timestamp):
        """Execute comprehensive printing sequence with multiple fallbacks"""
        success = False
        method_used = None
        error_details = None
        
        try:
            # Method 1: Direct script execution
            success, method_used = self.try_direct_script(session_id)
            
            if not success:
                # Method 2: CUPS with default content
                success, method_used = self.try_cups_printing(session_id)
            
            if not success:
                # Method 3: Raw device printing
                success, method_used = self.try_raw_device_printing(session_id)
            
            if not success:
                # Method 4: Emergency fortune generation
                success, method_used = self.try_emergency_printing(session_id)
        
        except Exception as e:
            error_details = str(e)
            logger.error(f"❌ Print sequence failed: {e}")
        
        # Update statistics and state
        if success:
            self.success_count += 1
            logger.info(f"✅ Print SUCCESS via {method_used} (#{self.success_count})")
        else:
            self.failure_count += 1
            logger.error(f"❌ Print FAILED after all methods (#{self.failure_count})")
        
        # Save state
        self.save_state(session_id, timestamp, success, method_used, error_details)
        
        # Log current statistics
        total = self.success_count + self.failure_count
        success_rate = (self.success_count / total * 100) if total > 0 else 0
        logger.info(f"📊 Stats: {self.success_count}✅ {self.failure_count}❌ ({success_rate:.1f}% success)")
    
    def try_direct_script(self, session_id):
        """Method 1: Execute print-now.sh script"""
        try:
            # Ensure we're in the right directory
            os.chdir(self.base_path)
            
            # Clean environment
            clean_env = {
                'PATH': '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin',
                'USER': 'zeldar',
                'HOME': '/home/zeldar',
                'TERM': 'xterm'
            }
            
            result = subprocess.run(
                ['./scripts/print-now.sh', 'button_triggered'],
                env=clean_env,
                cwd=self.base_path,
                capture_output=True,
                text=True,
                timeout=30,
                check=True
            )
            
            logger.debug(f"Script output: {result.stdout}")
            return True, "direct_script"
            
        except subprocess.TimeoutExpired:
            logger.warning("⏰ Script execution timeout")
            return False, None
        except subprocess.CalledProcessError as e:
            logger.warning(f"⚠️  Script failed: {e.stderr}")
            return False, None
        except Exception as e:
            logger.warning(f"⚠️  Script execution error: {e}")
            return False, None
    
    def try_cups_printing(self, session_id):
        """Method 2: Direct CUPS printing with embedded content"""
        try:
            fortune_content = self.generate_button_fortune(session_id)
            
            # Use echo to pipe content to lp
            process = subprocess.Popen(
                ['lp', '-d', self.printer_name, '-o', 'raw'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=fortune_content, timeout=20)
            
            if process.returncode == 0:
                logger.debug(f"CUPS output: {stdout}")
                return True, "cups_direct"
            else:
                logger.warning(f"CUPS error: {stderr}")
                return False, None
                
        except Exception as e:
            logger.warning(f"⚠️  CUPS printing failed: {e}")
            return False, None
    
    def try_raw_device_printing(self, session_id):
        """Method 3: Raw device printing"""
        try:
            fortune_content = self.generate_button_fortune(session_id)
            
            # Try common USB printer device paths
            device_paths = ['/dev/usb/lp0', '/dev/lp0', '/dev/usb/lp1']
            
            for device_path in device_paths:
                if os.path.exists(device_path):
                    try:
                        with open(device_path, 'wb') as device:
                            device.write(fortune_content.encode('utf-8', errors='ignore'))
                            device.flush()
                        logger.debug(f"Raw device print to {device_path}")
                        return True, f"raw_device_{device_path}"
                    except Exception as e:
                        logger.debug(f"Raw device {device_path} failed: {e}")
                        continue
            
            return False, None
            
        except Exception as e:
            logger.warning(f"⚠️  Raw device printing failed: {e}")
            return False, None
    
    def try_emergency_printing(self, session_id):
        """Method 4: Emergency fortune with minimal dependencies"""
        try:
            # Create emergency fortune file
            emergency_content = f"""
═══════════════════════════════════
🆘 EMERGENCY FORTUNE PRINT
═══════════════════════════════════

Session: {session_id}
Time: {datetime.now().strftime('%H:%M:%S')}
Press: #{self.print_count}

"The button was pressed,
 The universe responded,
 Fortune manifests"

═══════════════════════════════════
InformationForce tessellated ∞
═══════════════════════════════════

"""
            
            # Write to temp file and print
            emergency_file = Path('/tmp/emergency_fortune.txt')
            emergency_file.write_text(emergency_content)
            
            result = subprocess.run(
                ['lp', '-d', self.printer_name, str(emergency_file)],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0:
                return True, "emergency_file"
            else:
                return False, None
                
        except Exception as e:
            logger.warning(f"⚠️  Emergency printing failed: {e}")
            return False, None
    
    def generate_button_fortune(self, session_id):
        """Generate formatted fortune content for button press"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        fortune_variants = [
            "Context distilled, In geometric form -- Inductive bias, Resonating worlds",
            "Button pressed reveals the hidden pattern of electromagnetic information-dynamics",
            "Every press echoes through the categorical structure of reality itself",
            "The GPIO speaks, the printer listens, fortune emerges from silicon dreams",
            "InformationForce tessellated through thermal paper and electromagnetic fields"
        ]
        
        # Cycle through fortunes based on press count
        fortune_text = fortune_variants[(self.print_count - 1) % len(fortune_variants)]
        
        content = f"""
\x1b@ヲヲヲ welcome to Uncommons
(symplectomorphic cobord.)

no official universe-agent
every _ unofficial agent
─────────────────────────────

{fortune_text}

─────────────────────────────
Session: {session_id}
Press: #{self.print_count}
Time: {timestamp}
Success: {self.success_count}
Total: {self.print_count}

sincerely yours
reafferent reaberrant
─────────────────────────────

\x1bi"""
        
        return content
    
    def load_state(self):
        """Load previous state from file"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.print_count = state.get('print_count', 0)
                    self.success_count = state.get('success_count', 0)
                    self.failure_count = state.get('failure_count', 0)
                logger.info(f"📊 Loaded state: {self.print_count} total, {self.success_count}✅ {self.failure_count}❌")
        except Exception as e:
            logger.warning(f"State loading failed: {e}")
    
    def save_state(self, session_id=None, timestamp=None, success=None, method=None, error=None):
        """Save current state to file"""
        try:
            state = {
                'print_count': self.print_count,
                'success_count': self.success_count,
                'failure_count': self.failure_count,
                'last_session': session_id,
                'last_timestamp': timestamp,
                'last_success': success,
                'last_method': method,
                'last_error': error,
                'system_ready': self.system_ready,
                'gpio_ready': self.gpio_ready
            }
            
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
                
        except Exception as e:
            logger.warning(f"State saving failed: {e}")
    
    def start_monitoring(self):
        """Start the button monitoring loop"""
        if not self.gpio_ready:
            logger.error("❌ Cannot start monitoring - GPIO not ready")
            if not GPIO_AVAILABLE:
                logger.info("🔄 Running in simulation mode - press Enter to simulate button")
                self.simulation_mode()
            return
        
        try:
            logger.info("🚀 Button monitoring ACTIVE on GPIO 6")
            logger.info("📄 InformationForce tessellated, electromagnetic resonance achieved")
            logger.info("🔘 Press button to trigger thermal fortune printing...")
            
            # Keep the main thread alive
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("🛑 Button monitoring stopped by user")
        except Exception as e:
            logger.error(f"❌ Monitoring loop failed: {e}")
        finally:
            if self.button:
                self.button.close()
    
    def simulation_mode(self):
        """Run in simulation mode for testing without GPIO"""
        logger.info("🎮 Simulation mode - press Enter to trigger print, 'q' to quit")
        
        try:
            while True:
                user_input = input().strip().lower()
                if user_input == 'q':
                    break
                else:
                    self.on_button_press()
        except KeyboardInterrupt:
            logger.info("🛑 Simulation mode stopped")

# Main execution
if __name__ == "__main__":
    printer = UltraRobustButtonPrinter()
    printer.start_monitoring()