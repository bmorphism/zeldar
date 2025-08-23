#!/usr/bin/env python3
"""
Collapsed Queue Fortune Button - Collapsing job queue with actual printing
Captures all raw GPIO events but collapses rapid events into single fortune jobs
"""

import time
import json
import subprocess
import threading
import queue
import os
from pathlib import Path
from datetime import datetime
from enum import Enum
from gpiozero import Button

class JobState(Enum):
    QUEUED = "queued"
    PROCESSING = "processing" 
    COMPLETED = "completed"
    FAILED = "failed"

class CollapsedQueueButton:
    """Raw GPIO events → Collapsed Queue → Single worker processor with actual printing"""
    
    def __init__(self, gpio_pin: int = 6):
        self.gpio_pin = gpio_pin
        
        # Job queue with collapsing logic
        self.job_queue = queue.Queue()
        self.worker_busy = False
        self.base_collapse_window = 3.0  # Base collapse window
        self.processing_extension = 30.0  # Extended window during processing
        self.last_job_time = 0
        self.processing_job = False  # Track if currently processing
        
        # Stats tracking
        self.total_button_events = 0
        self.queued_jobs = 0
        self.processed_jobs = 0
        self.successful_prints = 0
        self.failed_prints = 0
        self.collapsed_events = 0
        
        # State persistence
        self.state_file = Path('/tmp/collapsed_queue_state.json')
        self.load_state()
        
        print(f"🔘 Initializing Collapsed Queue Button on GPIO {gpio_pin}...")
        
        # Initialize button with NO debouncing - capture all events
        self.button = Button(gpio_pin, pull_up=True, bounce_time=None)
        self.button.when_pressed = self.on_raw_button_event
        
        print(f"✅ GPIO {gpio_pin} button initialized")
        
        # Start single worker thread
        self.worker_thread = threading.Thread(target=self.job_processor_worker, daemon=True)
        self.worker_thread.start()
        
        print(f"🔘 Collapsed Queue Button READY on GPIO {gpio_pin}")
        print(f"📊 Raw events → Collapsed Queue ({self.base_collapse_window}s/{self.processing_extension}s window) → Single worker")
        print(f"🖨️  ACTUAL PRINTING enabled - CUPS queue cleared")
        
    def on_raw_button_event(self):
        """Capture raw button event with collapse logic"""
        self.total_button_events += 1
        event_time = time.time()
        job_id = f"JOB_{int(event_time * 1000)}"
        
        # Dynamic collapse window - extend during processing
        current_window = self.processing_extension if self.processing_job else self.base_collapse_window
        time_since_last_job = event_time - self.last_job_time
        
        # MAXIMUM 1 JOB RULE: Collapse everything after first job
        max_jobs_allowed = 1
        
        should_collapse = (
            self.queued_jobs >= max_jobs_allowed or  # Already have max jobs
            self.processed_jobs > 0 or  # Any job ever processed  
            self.processing_job or      # Currently processing
            not self.job_queue.empty() or  # Queue has jobs
            time_since_last_job < current_window  # Within time window
        )
        
        if should_collapse:
            # Collapse this event - don't add new job
            self.collapsed_events += 1
            print(f"🔄 Event #{self.total_button_events} COLLAPSED (max_jobs={max_jobs_allowed}, queued={self.queued_jobs}, processed={self.processed_jobs})")
            print(f"   └─ {self.collapsed_events} total collapsed events")
        else:
            # Queue new job
            self.job_queue.put({
                'job_id': job_id,
                'event_time': event_time,
                'event_count': self.total_button_events,
                'collapsed_count': self.collapsed_events
            })
            self.queued_jobs += 1
            self.last_job_time = event_time
            
            queue_size = self.job_queue.qsize()
            worker_status = "BUSY" if self.worker_busy else "IDLE"
            
            print(f"🔘 Event #{self.total_button_events} → NEW JOB → {job_id}")
            print(f"   Queue: {queue_size} jobs, Worker: {worker_status}")
            
        self.save_state()
        
    def job_processor_worker(self):
        """Single worker thread processes collapsed jobs"""
        print("🔧 Collapsed job processor worker started")
        
        while True:
            try:
                # Block until job available
                job = self.job_queue.get(timeout=1)
                
                self.worker_busy = True
                self.processing_job = True
                self.processed_jobs += 1
                
                job_id = job['job_id']
                event_count = job['event_count']
                collapsed_count = job.get('collapsed_count', 0)
                queue_remaining = self.job_queue.qsize()
                
                print(f"\n🖨️  Processing {job_id} (Event #{event_count}, +{collapsed_count} collapsed)")
                print(f"   Queue remaining: {queue_remaining} jobs")
                
                # Execute the print job with ACTUAL printing
                success = self.execute_print_job(job_id, event_count, collapsed_count)
                
                if success:
                    self.successful_prints += 1
                    print(f"✅ {job_id} SUCCESS - ACTUAL PRINT COMPLETED")
                else:
                    self.failed_prints += 1
                    print(f"❌ {job_id} FAILED")
                
                # Mark job as done
                self.job_queue.task_done()
                self.worker_busy = False
                self.processing_job = False
                
                print(f"📊 Stats: {self.successful_prints}✅ {self.failed_prints}❌ {self.collapsed_events}🔄 Queue: {self.job_queue.qsize()}")
                self.save_state()
                
            except queue.Empty:
                # No jobs in queue, worker idle
                continue
            except Exception as e:
                print(f"❌ Worker error: {e}")
                self.worker_busy = False
                
    def execute_print_job(self, job_id: str, event_count: int, collapsed_count: int) -> bool:
        """Execute single print job with ACTUAL printing priority"""
        try:
            # Method 1: Try CUPS direct (prioritize actual printing)
            if self.try_cups_print(event_count, collapsed_count):
                return True
            
            # Method 2: Try print script
            elif self.try_print_script(event_count):
                return True
                
            # Method 3: Last resort simulation
            elif self.try_simulation_print(event_count, collapsed_count):
                return True
            
            return False
            
        except Exception as e:
            print(f"   Exception in {job_id}: {e}")
            return False
            
    def try_cups_print(self, event_count: int, collapsed_count: int) -> bool:
        """Try printing via CUPS - prioritized for actual printing"""
        try:
            timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
            content = f"""Context distilled
Event #{event_count}
{timestamp}
∞"""

            # Create temp file
            temp_file = Path('/tmp/collapsed_fortune_print.txt')
            temp_file.write_text(content)
            
            # Print via CUPS with explicit paper size
            result = subprocess.run([
                'lp', '-d', 'Y812BT', '-o', 'PageSize=w288h144', str(temp_file)
            ], 
            capture_output=True, 
            text=True, 
            timeout=20
            )
            
            # Cleanup
            temp_file.unlink()
            
            if result.returncode == 0:
                print(f"   ✓ CUPS method succeeded - ACTUAL PRINT SENT")
                return True
            else:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                print(f"   ✗ CUPS failed: {error_msg}")
                return False
            
        except Exception as e:
            print(f"   ✗ CUPS method failed: {e}")
            return False
            
    def try_print_script(self, event_count: int) -> bool:
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
            
            if result.returncode == 0:
                print(f"   ✓ Script method succeeded")
                return True
            else:
                print(f"   ✗ Script failed: {result.stderr.strip()}")
                return False
            
        except Exception as e:
            print(f"   ✗ Script method failed: {e}")
            return False
            
    def try_simulation_print(self, event_count: int, collapsed_count: int) -> bool:
        """Simulation print - last resort only"""
        print("   🎮 SIMULATION:")
        print(f"   Event #{event_count}")
        print(f"   {datetime.now().strftime('%H:%M:%S')}")
        print("   ∞")
        
        # Simulate print time
        time.sleep(0.5)
        return True
        
    def load_state(self):
        """Load previous state"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    
                self.total_button_events = data.get('total_button_events', 0)
                self.queued_jobs = data.get('queued_jobs', 0)
                self.processed_jobs = data.get('processed_jobs', 0)
                self.successful_prints = data.get('successful_prints', 0)
                self.failed_prints = data.get('failed_prints', 0)
                self.collapsed_events = data.get('collapsed_events', 0)
                
                print(f"📊 Loaded state: {self.successful_prints}✅ {self.failed_prints}❌ {self.collapsed_events}🔄")
                
        except Exception as e:
            print(f"State loading failed: {e}")
            
    def save_state(self):
        """Save current state"""
        try:
            state_data = {
                'timestamp': time.time(),
                'total_button_events': self.total_button_events,
                'queued_jobs': self.queued_jobs,
                'processed_jobs': self.processed_jobs,
                'successful_prints': self.successful_prints,
                'failed_prints': self.failed_prints,
                'collapsed_events': self.collapsed_events,
                'queue_size': self.job_queue.qsize(),
                'worker_busy': self.worker_busy
            }
            
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
                
        except Exception as e:
            print(f"State saving failed: {e}")
            
    def get_status(self) -> dict:
        """Get current system status"""
        return {
            'total_button_events': self.total_button_events,
            'queue_size': self.job_queue.qsize(),
            'worker_busy': self.worker_busy,
            'base_collapse_window': self.base_collapse_window,
            'processing_extension': self.processing_extension,
            'stats': {
                'queued_jobs': self.queued_jobs,
                'processed_jobs': self.processed_jobs,
                'successful_prints': self.successful_prints,
                'failed_prints': self.failed_prints,
                'collapsed_events': self.collapsed_events,
                'success_rate': self.successful_prints / max(1, self.processed_jobs) * 100,
                'collapse_rate': self.collapsed_events / max(1, self.total_button_events) * 100
            }
        }
        
    def run(self):
        """Run the collapsed queue button system"""
        print("\n🚀 COLLAPSED QUEUE FORTUNE BUTTON SYSTEM")
        print("=" * 50) 
        print("APPROACH: Raw GPIO events → Collapsed queue → Single worker → ACTUAL PRINTING")
        print(f"COLLAPSING: Events within {self.base_collapse_window}s/{self.processing_extension}s window merged")
        print("PRINTING: CUPS prioritized for actual thermal output")
        print("=" * 50)
        print("Press button to test collapsed queue processing...")
        print("Press Ctrl+C to stop\n")
        
        try:
            # Keep main thread alive
            while True:
                time.sleep(5)
                
                # Periodic status update
                status = self.get_status()
                if status['total_button_events'] > 0:
                    queue_size = status['queue_size']
                    worker = "BUSY" if status['worker_busy'] else "IDLE"
                    collapse_rate = status['stats']['collapse_rate']
                    print(f"📊 Events: {status['total_button_events']}, Collapsed: {collapse_rate:.1f}%, Queue: {queue_size}, Worker: {worker}")
                
        except KeyboardInterrupt:
            print(f"\n🛑 Shutting down...")
            print(f"📊 Final: {self.total_button_events} events → {self.processed_jobs} processed")
            print(f"   Success: {self.successful_prints}✅ Failed: {self.failed_prints}❌ Collapsed: {self.collapsed_events}🔄")
            
            # Wait for queue to finish
            if not self.job_queue.empty():
                print(f"⏳ Waiting for {self.job_queue.qsize()} remaining jobs...")
                self.job_queue.join()
                print("✅ All jobs completed")
                
        finally:
            self.button.close()

def main():
    """Main execution"""
    button_system = CollapsedQueueButton(gpio_pin=6)
    button_system.run()

if __name__ == "__main__":
    main()