#!/usr/bin/env python3
# Button Print Loop - Ultra-Robust Edition
# Context distilled in geometric form with maximum reliability

import logging
import logging.handlers
import os
import sys
import time
import signal
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional
import json

# Import GPIO with fallback
try:
    from gpiozero import Button, Device
    from gpiozero.pins.mock import MockFactory
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("⚠️  GPIO not available - running in mock mode")

class UltraRobustButtonPrinter:
    def __init__(self, gpio_pin: int = 6, base_dir: str = "/home/zeldar/burningman"):
        self.gpio_pin = gpio_pin
        self.base_dir = Path(base_dir)
        self.log_dir = self.base_dir / "logs"
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # State tracking
        self.is_running = True
        self.last_press_time = 0
        self.debounce_time = 0.5  # Prevent rapid-fire presses
        self.button = None
        self.print_attempts = 0
        self.successful_prints = 0
        self.failed_prints = 0
        
        # Health monitoring
        self.last_health_check = 0
        self.health_check_interval = 60  # Check every minute
        
        # Signal handling
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        
        self.logger.info("🚀 UltraRobustButtonPrinter initializing...")
        
    def setup_logging(self):
        """Setup comprehensive logging with rotation"""
        self.logger = logging.getLogger('ButtonPrinter')
        self.logger.setLevel(logging.INFO)
        
        # File handler with rotation
        log_file = self.log_dir / "button_printer.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=1024*1024, backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def validate_environment(self) -> bool:
        """Validate that all required components are available"""
        self.logger.info("🔍 Validating environment...")
        
        # Check if we're in the right directory
        if not (self.base_dir / "scripts" / "print-now.sh").exists():
            self.logger.error(f"❌ print-now.sh not found in {self.base_dir}/scripts/")
            return False
            
        # Check printer availability
        if not self.check_printer_available():
            self.logger.warning("⚠️  Printer not immediately available, will retry later")
            
        # Check GPIO availability
        if not GPIO_AVAILABLE:
            self.logger.warning("⚠️  GPIO not available, using mock mode")
            
        self.logger.info("✅ Environment validation completed")
        return True
        
    def check_printer_available(self) -> bool:
        """Check if Y812BT printer is available"""
        try:
            # Check USB connection
            result = subprocess.run(['lsusb'], capture_output=True, text=True, timeout=5)
            if "5958:0130" in result.stdout:
                self.logger.info("✅ Y812BT printer detected via USB")
                return True
            else:
                self.logger.warning("⚠️  Y812BT printer not detected via USB")
                return False
        except Exception as e:
            self.logger.error(f"❌ Failed to check printer: {e}")
            return False
            
    def setup_gpio(self) -> bool:
        """Setup GPIO button with comprehensive error handling"""
        try:
            if GPIO_AVAILABLE:
                # Configure for maximum reliability
                self.button = Button(
                    self.gpio_pin, 
                    pull_up=True, 
                    bounce_time=0.2,  # Increased bounce time
                    hold_time=0.1
                )
                self.button.when_pressed = self.on_button_press
                self.logger.info(f"✅ GPIO {self.gpio_pin} configured successfully")
                return True
            else:
                self.logger.warning("⚠️  GPIO not available, creating mock button")
                return True
        except Exception as e:
            self.logger.error(f"❌ Failed to setup GPIO: {e}")
            return False
            
    def on_button_press(self):
        """Handle button press with debouncing and comprehensive error handling"""
        current_time = time.time()
        
        # Debounce protection
        if current_time - self.last_press_time < self.debounce_time:
            self.logger.info("⏱️  Button press ignored (debounce protection)")
            return
            
        self.last_press_time = current_time
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        
        self.logger.info(f"🔘 Button pressed - {timestamp}")
        
        # Start print in separate thread to avoid blocking GPIO
        print_thread = threading.Thread(target=self.execute_print, daemon=True)
        print_thread.start()
        
    def execute_print(self):
        """Execute print with multiple fallback methods and retries"""
        self.print_attempts += 1
        max_retries = 3
        
        for attempt in range(max_retries):
            if attempt > 0:
                self.logger.info(f"🔄 Print attempt {attempt + 1}/{max_retries}")
                time.sleep(2 ** attempt)  # Exponential backoff
                
            if self.try_print_methods():
                self.successful_prints += 1
                self.logger.info(f"✅ Print successful! (Success rate: {self.successful_prints}/{self.print_attempts})")
                self.save_status()
                return
                
        self.failed_prints += 1
        self.logger.error(f"❌ All print attempts failed! (Failure: {self.failed_prints}/{self.print_attempts})")
        self.save_status()
        
    def try_print_methods(self) -> bool:
        """Try multiple print methods with specific error handling"""
        methods = [
            ("Direct Script", self.print_via_script),
            ("CUPS Direct", self.print_via_cups_direct),
            ("Raw Device", self.print_via_raw_device),
            ("Echo Pipe", self.print_via_echo_pipe)
        ]
        
        for method_name, method in methods:
            try:
                self.logger.info(f"🖨️  Trying {method_name}...")
                if method():
                    self.logger.info(f"✅ {method_name} succeeded")
                    return True
                else:
                    self.logger.warning(f"⚠️  {method_name} returned false")
            except Exception as e:
                self.logger.error(f"❌ {method_name} failed: {e}")
                
        return False
        
    def print_via_script(self) -> bool:
        """Print using the print-now.sh script"""
        script_path = self.base_dir / "scripts" / "print-now.sh"
        
        clean_env = {
            'PATH': '/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin',
            'USER': 'zeldar',
            'HOME': str(Path.home()),
            'PWD': str(self.base_dir)
        }
        
        result = subprocess.run(
            [str(script_path)], 
            cwd=str(self.base_dir),
            env=clean_env,
            capture_output=True,
            text=True,
            timeout=30,
            close_fds=True
        )
        
        if result.returncode == 0:
            self.logger.info(f"📜 Script output: {result.stdout.strip()}")
            return True
        else:
            self.logger.error(f"📜 Script error: {result.stderr.strip()}")
            return False
            
    def print_via_cups_direct(self) -> bool:
        """Print directly via CUPS"""
        fortune_text = self.get_fortune_text()
        
        result = subprocess.run(
            ['lp', '-d', 'Y812BT', '-'],
            input=fortune_text,
            text=True,
            capture_output=True,
            timeout=20
        )
        
        return result.returncode == 0
        
    def print_via_raw_device(self) -> bool:
        """Print directly to thermal printer device"""
        device_paths = ['/dev/usb/lp0', '/dev/usb/lp1', '/dev/lp0']
        fortune_command = self.get_esc_pos_fortune()
        
        for device_path in device_paths:
            if Path(device_path).exists():
                try:
                    with open(device_path, 'wb') as printer:
                        printer.write(fortune_command)
                    self.logger.info(f"📟 Raw device {device_path} succeeded")
                    return True
                except Exception as e:
                    self.logger.error(f"📟 Raw device {device_path} failed: {e}")
                    
        return False
        
    def print_via_echo_pipe(self) -> bool:
        """Print via echo pipe to lp"""
        fortune_text = self.get_fortune_text()
        
        cmd = f'echo -e "{fortune_text}" | lp -d Y812BT'
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=20
        )
        
        return result.returncode == 0
        
    def get_fortune_text(self) -> str:
        """Get formatted fortune text"""
        return """ヲヲヲ welcome to Uncommons
(symplectomorphic cobord.)

no official universe-agent
every _ unofficial agent
-----
Context distilled,
In geometric form --
Inductive bias,
Resonating worlds

sincerely yours
reafferent reaberrant"""

    def get_esc_pos_fortune(self) -> bytes:
        """Get ESC/POS formatted fortune"""
        fortune = self.get_fortune_text()
        # ESC @ (initialize) + content + ESC i (cut)
        return b'\x1b@' + fortune.encode('utf-8', errors='ignore') + b'\n\n\x1bi'
        
    def health_check(self):
        """Periodic health monitoring"""
        current_time = time.time()
        if current_time - self.last_health_check > self.health_check_interval:
            self.last_health_check = current_time
            
            self.logger.info(f"❤️  Health check - Running: {self.is_running}")
            self.logger.info(f"📊 Stats: {self.successful_prints} success, {self.failed_prints} failed, {self.print_attempts} total")
            
            # Check printer periodically
            printer_ok = self.check_printer_available()
            if not printer_ok:
                self.logger.warning("⚠️  Printer health check failed")
                
    def save_status(self):
        """Save current status to file"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'print_attempts': self.print_attempts,
            'successful_prints': self.successful_prints,
            'failed_prints': self.failed_prints,
            'success_rate': self.successful_prints / max(self.print_attempts, 1),
            'is_running': self.is_running
        }
        
        try:
            with open(self.base_dir / 'button_printer_status.json', 'w') as f:
                json.dump(status, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save status: {e}")
            
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"🛑 Received signal {signum}, shutting down gracefully...")
        self.is_running = False
        self.save_status()
        sys.exit(0)
        
    def run(self):
        """Main run loop with comprehensive error handling"""
        try:
            if not self.validate_environment():
                self.logger.error("❌ Environment validation failed")
                return False
                
            if not self.setup_gpio():
                self.logger.error("❌ GPIO setup failed")
                return False
                
            self.logger.info("🚀 Ultra-robust button printer ready!")
            self.logger.info("📄 Context distilled, geometric form, resonating worlds")
            self.logger.info(f"🔘 Monitoring GPIO {self.gpio_pin} for button presses...")
            
            # Main loop with health monitoring
            while self.is_running:
                try:
                    self.health_check()
                    time.sleep(1)  # Small sleep to prevent busy waiting
                except KeyboardInterrupt:
                    self.logger.info("🛑 Keyboard interrupt received")
                    break
                except Exception as e:
                    self.logger.error(f"❌ Unexpected error in main loop: {e}")
                    time.sleep(5)  # Brief pause before continuing
                    
        except Exception as e:
            self.logger.error(f"❌ Fatal error in run(): {e}")
            return False
        finally:
            self.save_status()
            self.logger.info("🏁 Button printer stopped")
            
        return True

def main():
    """Main entry point"""
    printer = UltraRobustButtonPrinter()
    return printer.run()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
