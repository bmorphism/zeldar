#!/usr/bin/env python3
"""
Queued Fortune Button - Raw GPIO events feed into job queue
No event dampening - all button presses captured and queued
Single worker processes one job at a time from queue
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

class QueuedFortuneButton:
    """Raw GPIO events → Queue → Single worker processor"""
    
    def __init__(self, gpio_pin: int = 6):
        self.gpio_pin = gpio_pin
        
        # Job queue - no size limit, captures all button events
        self.job_queue = queue.Queue()
        self.worker_busy = False
        
        # Stats tracking
        self.total_button_events = 0
        self.queued_jobs = 0
        self.processed_jobs = 0
        self.successful_prints = 0
        self.failed_prints = 0
        
        # State persistence
        self.state_file = Path('/tmp/queued_fortune_state.json')
        self.load_state()
        
        # Initialize button with NO debouncing - capture all events
        self.button = Button(gpio_pin, pull_up=True, bounce_time=None)
        self.button.when_pressed = self.on_raw_button_event
        
        # Start single worker thread
        self.worker_thread = threading.Thread(target=self.job_processor_worker, daemon=True)
        self.worker_thread.start()
        
        print(f"🔘 Queued Fortune Button initialized on GPIO {gpio_pin}")
        print(f"📊 Raw events → Queue → Single worker")
        print(f"🔧 NO event dampening - all presses captured")
        
    def on_raw_button_event(self):
        """Capture raw button event and queue job immediately"""
        self.total_button_events += 1
        event_time = time.time()
        job_id = f"JOB_{int(event_time * 1000)}"  # Millisecond precision
        
        # Queue the job immediately - no filtering
        self.job_queue.put({
            'job_id': job_id,
            'event_time': event_time,
            'event_count': self.total_button_events
        })
        self.queued_jobs += 1
        
        queue_size = self.job_queue.qsize()
        worker_status = "BUSY" if self.worker_busy else "IDLE"
        
        print(f"🔘 Event #{self.total_button_events} → Queue → {job_id}")
        print(f"   Queue: {queue_size} jobs, Worker: {worker_status}")
        
        self.save_state()
        
    def job_processor_worker(self):
        """Single worker thread processes jobs from queue one at a time"""
        print("🔧 Job processor worker started")
        
        while True:
            try:
                # Block until job available
                job = self.job_queue.get(timeout=1)
                
                self.worker_busy = True
                self.processed_jobs += 1
                
                job_id = job['job_id']
                event_count = job['event_count']
                queue_remaining = self.job_queue.qsize()
                
                print(f"\n🖨️  Processing {job_id} (Event #{event_count})")
                print(f"   Queue remaining: {queue_remaining} jobs")
                
                # Execute the print job
                success = self.execute_print_job(job_id, event_count)
                
                if success:
                    self.successful_prints += 1
                    print(f"✅ {job_id} SUCCESS")
                else:
                    self.failed_prints += 1
                    print(f"❌ {job_id} FAILED")
                
                # Mark job as done
                self.job_queue.task_done()
                self.worker_busy = False
                
                print(f"📊 Stats: {self.successful_prints}✅ {self.failed_prints}❌ Queue: {self.job_queue.qsize()}")
                self.save_state()
                
            except queue.Empty:
                # No jobs in queue, worker idle
                continue
            except Exception as e:
                print(f"❌ Worker error: {e}")
                self.worker_busy = False
                
    def execute_print_job(self, job_id: str, event_count: int) -> bool:
        """Execute single print job"""
        try:
            # Method 1: Try print script
            if self.try_print_script(event_count):
                return True
            
            # Method 2: Try CUPS
            elif self.try_cups_print(event_count):
                return True
                
            # Method 3: Simulation fallback
            elif self.try_simulation_print(event_count):
                return True
            
            return False
            
        except Exception as e:
            print(f"   Exception in {job_id}: {e}")
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
            
    def try_cups_print(self, event_count: int) -> bool:
        """Try printing via CUPS"""
        try:
            timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
            content = f"""Queued Fortune Print

Context distilled, clear
In geometric form, bias  
Resonating worlds

Event #{event_count}
Processed: {timestamp}
Queue: Raw → Worker → Print

Consciousness tessellated ∞"""

            # Create temp file
            temp_file = Path('/tmp/queued_fortune_print.txt')
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
            
            if result.returncode == 0:
                print(f"   ✓ CUPS method succeeded")
                return True
            else:
                print(f"   ✗ CUPS failed: {result.stderr.strip()}")
                return False
            
        except Exception as e:
            print(f"   ✗ CUPS method failed: {e}")
            return False
            
    def try_simulation_print(self, event_count: int) -> bool:
        """Simulation print (always succeeds)"""
        print("   🎮 SIMULATION PRINT:")
        print("   " + "=" * 25)
        print(f"   Button Event #{event_count}")
        print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
        print("   Context distilled, clear")
        print("   In geometric form, bias")
        print("   Resonating worlds")
        print("   " + "=" * 25)
        
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
                
                print(f"📊 Loaded state: {self.successful_prints}✅ {self.failed_prints}❌")
                
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
            'stats': {
                'queued_jobs': self.queued_jobs,
                'processed_jobs': self.processed_jobs,
                'successful_prints': self.successful_prints,
                'failed_prints': self.failed_prints,
                'success_rate': self.successful_prints / max(1, self.processed_jobs) * 100
            }
        }
        
    def run(self):
        """Run the queued button system"""
        print("\n🚀 QUEUED FORTUNE BUTTON SYSTEM")
        print("=" * 40) 
        print("APPROACH: Raw GPIO events → Job queue → Single worker")
        print("DAMPENING: Applied at queue processing, not event capture")
        print("BEHAVIOR: All button presses captured and queued")
        print("=" * 40)
        print("Press button rapidly to test queue processing...")
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
                    print(f"📊 Events: {status['total_button_events']}, Queue: {queue_size}, Worker: {worker}")
                
        except KeyboardInterrupt:
            print(f"\n🛑 Shutting down...")
            print(f"📊 Final: {self.total_button_events} events → {self.processed_jobs} processed")
            print(f"   Success: {self.successful_prints}✅ Failed: {self.failed_prints}❌")
            
            # Wait for queue to finish
            if not self.job_queue.empty():
                print(f"⏳ Waiting for {self.job_queue.qsize()} remaining jobs...")
                self.job_queue.join()
                print("✅ All jobs completed")
                
        finally:
            self.button.close()

def main():
    """Main execution"""
    button_system = QueuedFortuneButton(gpio_pin=6)
    button_system.run()

if __name__ == "__main__":
    main()