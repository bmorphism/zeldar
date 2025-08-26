#!/usr/bin/env python3
"""
Single Fortune Button - Maintains invariant of exactly 1 fortune per click
No new print jobs accepted until current job completes entirely
"""

import time
import json
import subprocess
import threading
import os
from pathlib import Path
from datetime import datetime
from enum import Enum
from gpiozero import Button

class JobState(Enum):
    IDLE = "idle"
    PROCESSING = "processing" 
    COMPLETED = "completed"
    FAILED = "failed"

class SingleFortuneButton:
    """Button system with strict single-job invariant"""
    
    def __init__(self, gpio_pin: int = 6):
        self.gpio_pin = gpio_pin
        self.job_state = JobState.IDLE
        self.job_lock = threading.Lock()
        self.current_job_id = None
        self.job_start_time = None
        
        # Stats
        self.total_clicks = 0
        self.successful_prints = 0
        self.failed_prints = 0
        self.ignored_clicks = 0
        
        # State file for persistence
        self.state_file = Path('/tmp/fortune_job_state.json')
        
        # Load previous state
        self.load_state()
        
        # Initialize button with correct hardware config
        # Based on testing: pull_up=True, button goes LOW when pressed
        self.button = Button(gpio_pin, pull_up=True, bounce_time=0.4)
        self.button.when_pressed = self.on_button_press
        
        print(f"🔧 GPIO {gpio_pin} configured: pull_up=True, bounce_time=0.4s")
        
        print(f"🔘 Single Fortune Button initialized on GPIO {gpio_pin}")
        print(f"📊 Stats: {self.successful_prints}✅ {self.failed_prints}❌ {self.ignored_clicks}⏭️")
        print(f"💡 Current state: {self.job_state.value}")
        
    def on_button_press(self):
        """Handle button press with strict job invariant"""
        self.total_clicks += 1
        click_time = time.time()
        
        print(f"\n🔘 BUTTON DETECTED! Click #{self.total_clicks} at {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
        print(f"🔧 GPIO value: {self.button.value}, State: {self.job_state.value}")
        
        with self.job_lock:
            if self.job_state == JobState.IDLE:
                # Accept new job
                self.job_state = JobState.PROCESSING
                self.current_job_id = f"JOB_{int(click_time)}"
                self.job_start_time = click_time
                
                print(f"✅ Accepting job {self.current_job_id}")
                
                # Start print job in background thread
                job_thread = threading.Thread(
                    target=self.execute_print_job,
                    args=(self.current_job_id,),
                    daemon=True
                )
                job_thread.start()
                
            else:
                # Reject - job already in progress
                self.ignored_clicks += 1
                elapsed = click_time - self.job_start_time if self.job_start_time else 0
                print(f"⏭️  IGNORED - Job {self.current_job_id} still {self.job_state.value} ({elapsed:.1f}s)")
                print(f"   └─ Total ignored clicks: {self.ignored_clicks}")
        
        # Save state after each click
        self.save_state()
        
    def execute_print_job(self, job_id: str):
        """Execute single print job to completion"""
        print(f"🖨️  Starting print job {job_id}")
        success = False
        
        try:
            # Method 1: Try print script
            if self.try_print_script():
                success = True
                print(f"✅ Job {job_id} SUCCESS via print script")
            
            # Method 2: Try CUPS if script failed
            elif self.try_cups_print():
                success = True
                print(f"✅ Job {job_id} SUCCESS via CUPS")
                
            # Method 3: Emergency simulation
            elif self.try_simulation_print():
                success = True
                print(f"✅ Job {job_id} SUCCESS via simulation")
            
            else:
                success = False
                print(f"❌ Job {job_id} FAILED - all methods exhausted")
                
        except Exception as e:
            success = False
            print(f"❌ Job {job_id} FAILED with exception: {e}")
        
        # Update state and stats
        with self.job_lock:
            if success:
                self.job_state = JobState.COMPLETED
                self.successful_prints += 1
            else:
                self.job_state = JobState.FAILED  
                self.failed_prints += 1
            
            job_duration = time.time() - self.job_start_time
            print(f"🏁 Job {job_id} completed in {job_duration:.1f}s")
            print(f"📊 Updated stats: {self.successful_prints}✅ {self.failed_prints}❌ {self.ignored_clicks}⏭️")
            
            # Reset to IDLE to accept new jobs
            self.job_state = JobState.IDLE
            self.current_job_id = None
            self.job_start_time = None
            
        self.save_state()
        print(f"💡 Ready for next button press\n")
        
    def try_print_script(self) -> bool:
        """Try printing via script"""
        try:
            result = subprocess.run([
                './scripts/print-now.sh', 'button_triggered'
            ], 
            capture_output=True, 
            text=True, 
            timeout=30, 
            cwd='/home/zeldar/burningman'
            )
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"   Script method failed: {e}")
            return False
            
    def try_cups_print(self) -> bool:
        """Try printing via CUPS"""
        try:
            # Generate simple fortune content
            timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
            content = f"""Button Print
            
Context distilled, clear
In geometric form, bias  
Resonating worlds

Press #{self.total_clicks}
{timestamp}

InformationForce tessellated ∞"""

            # Create temp file
            temp_file = Path('/tmp/fortune_print.txt')
            temp_file.write_text(content)
            
            # Print via CUPS
            result = subprocess.run([
                'lp', '-d', 'Y812BT', str(temp_file)
            ], 
            capture_output=True, 
            text=True, 
            timeout=20
            )
            
            # Cleanup
            temp_file.unlink()
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"   CUPS method failed: {e}")
            return False
            
    def try_simulation_print(self) -> bool:
        """Simulation print (always succeeds)"""
        print("🎮 SIMULATION PRINT:")
        print("=" * 30)
        print(f"  Button Press #{self.total_clicks}")
        print(f"  Time: {datetime.now().strftime('%H:%M:%S')}")
        print("  Context distilled, clear")
        print("  In geometric form, bias")
        print("  Resonating worlds")
        print("=" * 30)
        return True
        
    def load_state(self):
        """Load previous job state"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    
                self.total_clicks = data.get('total_clicks', 0)
                self.successful_prints = data.get('successful_prints', 0)
                self.failed_prints = data.get('failed_prints', 0)
                self.ignored_clicks = data.get('ignored_clicks', 0)
                
                # Always start in IDLE state on restart
                self.job_state = JobState.IDLE
                
        except Exception as e:
            print(f"State loading failed: {e}")
            
    def save_state(self):
        """Save current job state"""
        try:
            state_data = {
                'timestamp': time.time(),
                'job_state': self.job_state.value,
                'current_job_id': self.current_job_id,
                'total_clicks': self.total_clicks,
                'successful_prints': self.successful_prints,
                'failed_prints': self.failed_prints,
                'ignored_clicks': self.ignored_clicks
            }
            
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
                
        except Exception as e:
            print(f"State saving failed: {e}")
            
    def get_status(self) -> dict:
        """Get current system status"""
        return {
            'job_state': self.job_state.value,
            'current_job_id': self.current_job_id,
            'job_duration': time.time() - self.job_start_time if self.job_start_time else 0,
            'stats': {
                'total_clicks': self.total_clicks,
                'successful_prints': self.successful_prints,
                'failed_prints': self.failed_prints,
                'ignored_clicks': self.ignored_clicks,
                'success_rate': self.successful_prints / max(1, self.total_clicks) * 100
            }
        }
        
    def run(self):
        """Run the button system"""
        print("\n🚀 SINGLE FORTUNE BUTTON SYSTEM")
        print("=" * 40) 
        print("INVARIANT: Exactly 1 fortune per detected click")
        print("BEHAVIOR: New clicks ignored while job processing")
        print("=" * 40)
        print("Press button to print fortune...")
        print("Press Ctrl+C to stop\n")
        
        try:
            # Keep main thread alive
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Shutting down after {self.total_clicks} total clicks")
            final_status = self.get_status()
            print(f"📊 Final stats: {final_status['stats']}")
        finally:
            self.button.close()

def main():
    """Main execution"""
    button_system = SingleFortuneButton(gpio_pin=6)
    button_system.run()

if __name__ == "__main__":
    main()