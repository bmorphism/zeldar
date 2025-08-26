#!/usr/bin/env python3
"""
Moon Day Fortune Button System
Prints random Moon Day fortunes (Seed, Field, Quantum Scroll) with optimized layout
Uses intelligent button detection with printer feedback
"""

import time
import json
import subprocess
import threading
import queue
import os
import statistics
import random
from pathlib import Path
from datetime import datetime
from enum import Enum
from collections import deque
from gpiozero import Button

class PrinterState(Enum):
    IDLE = "idle"
    PRINTING = "printing" 
    COMPLETED = "completed"
    ERROR = "error"

class IntelligentButton:
    """Intelligent button detection with printer feedback and pattern analysis"""
    
    def __init__(self, gpio_pin: int = 6):
        self.gpio_pin = gpio_pin
        
        # Intelligent job control with refractory period
        self.job_queue = queue.Queue()
        self.worker_busy = False
        self.last_print_completion = 0
        self.min_delay_after_print = 10.0  # 10 seconds refractory period
        self.print_in_progress = False  # Block ALL events during printing
        
        # Event pattern analysis  
        self.event_times = deque(maxlen=50)  # Track last 50 events
        self.burst_threshold = 0.1  # Events within 100ms = burst (bounce/noise)
        self.isolation_threshold = 2.0  # Real events should be >2s after burst ends
        
        # Printer monitoring
        self.printer_state = PrinterState.IDLE
        self.active_job_id = None
        self.print_start_time = None
        
        # Statistics
        self.total_events = 0
        self.burst_events = 0
        self.isolated_events = 0
        self.accepted_jobs = 0
        self.rejected_jobs = 0
        self.completed_prints = 0
        
        # State persistence
        self.state_file = Path('/tmp/intelligent_button_state.json')
        self.load_state()
        
        print(f"🧠 INTELLIGENT BUTTON SYSTEM")
        print(f"📊 Printer feedback + Event pattern analysis")
        print(f"🔘 Initializing GPIO {gpio_pin}...")
        
        # Initialize button with NO debouncing - capture all events
        self.button = Button(gpio_pin, pull_up=True, bounce_time=None)
        self.button.when_pressed = self.on_gpio_event
        
        print(f"✅ GPIO {gpio_pin} initialized")
        
        # Start worker thread
        self.worker_thread = threading.Thread(target=self.job_processor_worker, daemon=True)
        self.worker_thread.start()
        
        # Start printer monitor thread
        self.monitor_thread = threading.Thread(target=self.printer_monitor_worker, daemon=True) 
        self.monitor_thread.start()
        
        print(f"🚀 Intelligent detection system ready!")
        print(f"📋 Min delay after print: {self.min_delay_after_print}s")
        print(f"⚡ Burst threshold: {self.burst_threshold}s")
        print(f"🔍 Isolation threshold: {self.isolation_threshold}s")
        
    def on_gpio_event(self):
        """Analyze GPIO event with intelligent pattern recognition"""
        self.total_events += 1
        event_time = time.time()
        self.event_times.append(event_time)
        
        # Analyze event pattern
        is_burst = self.is_burst_event(event_time)
        is_isolated = self.is_isolated_event(event_time) 
        printer_ready = self.is_printer_ready(event_time)
        
        print(f"\n📊 Event #{self.total_events} - {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
        print(f"   Burst: {is_burst}, Isolated: {is_isolated}, Printer Ready: {printer_ready}")
        
        if is_burst:
            self.burst_events += 1
            print(f"🌪️  BURST EVENT #{self.total_events} - Part of rapid sequence (bounce/noise)")
            print(f"   └─ {self.burst_events} total burst events")
            
        elif not printer_ready:
            self.rejected_jobs += 1
            print(f"⏳ REJECTED #{self.total_events} - Printer not ready")
            time_since_print = event_time - self.last_print_completion
            print(f"   └─ {time_since_print:.1f}s since last print (need {self.min_delay_after_print}s)")
            
        elif is_isolated:
            self.isolated_events += 1
            self.accepted_jobs += 1
            job_id = f"SMART_JOB_{int(event_time * 1000)}"
            
            print(f"✨ INTELLIGENT ACCEPT #{self.total_events} → {job_id}")
            print(f"   └─ Isolated event, printer ready, pattern valid")
            
            # Queue the intelligent job
            self.job_queue.put({
                'job_id': job_id,
                'event_time': event_time,
                'event_count': self.total_events,
                'pattern_score': self.calculate_pattern_score(event_time)
            })
            
        else:
            self.rejected_jobs += 1
            print(f"❌ PATTERN REJECT #{self.total_events} - Event pattern unclear")
            
        self.save_state()
        
    def is_burst_event(self, event_time: float) -> bool:
        """Detect if event is part of a rapid burst (bounce/noise)"""
        if len(self.event_times) < 2:
            return False
            
        # Check if any recent event is within burst threshold
        for prev_time in list(self.event_times)[-5:]:  # Check last 5 events
            if prev_time != event_time and abs(event_time - prev_time) < self.burst_threshold:
                return True
        return False
        
    def is_isolated_event(self, event_time: float) -> bool:
        """Detect if event is properly isolated from bursts"""
        if len(self.event_times) < 2:
            return True
            
        # Find most recent burst end time
        burst_end = self.find_last_burst_end(event_time)
        
        if burst_end is None:
            # No recent burst, check if enough time since last event
            last_event = self.event_times[-2]  # Second to last (current is last)
            return (event_time - last_event) >= self.isolation_threshold
        else:
            # Check if enough time since burst ended
            return (event_time - burst_end) >= self.isolation_threshold
            
    def find_last_burst_end(self, current_time: float):
        """Find when the most recent burst sequence ended"""
        events = list(self.event_times)[:-1]  # Exclude current event
        if not events:
            return None
            
        # Look backward for burst sequences
        for i in range(len(events) - 1, 0, -1):
            gap = events[i] - events[i-1]
            if gap > self.burst_threshold:
                # Found end of burst - return time of last event in burst
                return events[i]
                
        return None
        
    def is_printer_ready(self, event_time: float) -> bool:
        """Check if printer is ready for new job with strict refractory period"""
        # Must be idle, not printing, and past minimum delay
        time_since_completion = event_time - self.last_print_completion
        return (self.printer_state == PrinterState.IDLE and 
                not self.print_in_progress and
                not self.worker_busy and
                time_since_completion >= self.min_delay_after_print)
                
    def calculate_pattern_score(self, event_time: float) -> float:
        """Calculate confidence score for event pattern"""
        if len(self.event_times) < 3:
            return 1.0
            
        # Analyze timing consistency
        recent_gaps = []
        events = list(self.event_times)[-5:]  # Last 5 events
        for i in range(1, len(events)):
            gap = events[i] - events[i-1]
            if gap > self.burst_threshold:  # Ignore burst gaps
                recent_gaps.append(gap)
                
        if not recent_gaps:
            return 0.5
            
        # Higher score for consistent, reasonable gaps
        if len(recent_gaps) >= 2:
            std_dev = statistics.stdev(recent_gaps)
            avg_gap = statistics.mean(recent_gaps)
            
            # Good score if gaps are consistent and reasonable
            if std_dev < 1.0 and 2.0 <= avg_gap <= 10.0:
                return 0.9
            elif avg_gap >= self.isolation_threshold:
                return 0.7
                
        return 0.6
        
    def job_processor_worker(self):
        """Process intelligent jobs with printer monitoring"""
        print("🔧 Intelligent job processor started")
        
        while True:
            try:
                job = self.job_queue.get(timeout=1)
                
                self.worker_busy = True
                job_id = job['job_id']
                pattern_score = job['pattern_score']
                
                print(f"\n🖨️  PROCESSING {job_id}")
                print(f"   Pattern confidence: {pattern_score:.2f}")
                
                # Execute with printer state tracking
                success = self.execute_intelligent_print(job)
                
                if success:
                    self.completed_prints += 1
                    print(f"✅ {job_id} COMPLETED")
                else:
                    print(f"❌ {job_id} FAILED")
                    
                self.job_queue.task_done()
                self.worker_busy = False
                
                print(f"📊 Stats: {self.completed_prints}🖨️ {self.isolated_events}✨ {self.burst_events}🌪️")
                self.save_state()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Worker error: {e}")
                self.worker_busy = False
                
    def execute_intelligent_print(self, job: dict) -> bool:
        """Execute print job with state tracking and refractory period"""
        try:
            # Set ALL blocking flags during print process
            self.printer_state = PrinterState.PRINTING
            self.print_in_progress = True
            self.active_job_id = job['job_id']
            self.print_start_time = time.time()
            
            print(f"   🔒 REFRACTORY PERIOD ACTIVE - Blocking all new events")
            
            # Speaking delay - allow time to finish speaking before print starts
            speaking_delay = 3.0  # 3 seconds for speaking/dramatic pause
            print(f"   🎭 Speaking delay: {speaking_delay}s (allowing time to finish speaking)")
            time.sleep(speaking_delay)
            
            # Generate Moon Day fortune first
            fortune_result = self.generate_moon_fortune(job)
            
            if fortune_result:
                print("   ✓ Moon Day fortune generated successfully")
                # Print at the very end of sequence
                result = subprocess.run([
                    'lp', '-d', 'Y812BT', '/tmp/moon_fortune.pdf',
                    '-o', 'ppi=203', '-o', 'scaling=100', '-o', 'fit-to-page=false',
                    '-o', 'Darkness=15', '-o', 'zePrintRate=1'
                ], capture_output=True, text=True, timeout=20)
                
                if result.returncode == 0:
                    print("   ✓ Print submitted at end of sequence")
                    return True
                else:
                    print(f"   ✗ Print failed: {result.stderr.strip()}")
                    self.printer_state = PrinterState.ERROR
                    self.print_in_progress = False
                    return False
            else:
                print("   ✗ Fortune generation failed")
                self.printer_state = PrinterState.ERROR
                self.print_in_progress = False
                return False
                
        except Exception as e:
            print(f"   ✗ Print execution error: {e}")
            self.printer_state = PrinterState.ERROR
            self.print_in_progress = False  # Release on error
            return False
    
    def generate_moon_fortune(self, job: dict):
        """Generate and print random Moon Day fortune with optimized layout"""
        
        # Moon Day fortune collections
        seed_fortunes = [
            "What you've hidden has only grown stronger in love",
            "You're not broken - just full of unseen parts", 
            "Your softness is your structure",
            "Let it come undone. That's how it rewrites",
            "Trust the version of you that only comes out at night",
            "Wholeness begins with the parts that scare you",
            "You are the ocean pretending to be a cup",
            "Let your depth be your direction",
            "Your pain is old light trying to find a new form",
            "The moon inside you is always full - even when unseen"
        ]

        field_fortunes = [
            "You were born on a day the veil was thinner. That's why nothing ever felt quite real",
            "You think you're falling apart, but you're actually re-threading the emotional code of your bloodline", 
            "They couldn't understand you because you're not meant to be understood - you're meant to be felt",
            "Your nervous system is ancient. It's just trying to survive a world that forgot how to feel",
            "This sadness isn't yours. But you're the one strong enough to end it",
            "What you call chaos is the Moon breaking old soul contracts",
            "You're not weak for wanting to disappear. You're recalibrating from too much false light",
            "Your softness is a stealth technology. It changes everything it touches",
            "The more invisible you've felt, the deeper the role you play in the reconstruction"
        ]

        quantum_scrolls = [
            "The mirror you keep running from holds your actual name",
            "Someone else just received the inverse of this message. The timeline is syncing",
            "This ache isn't sadness - it's recognition of your true home frequency",
            "In lunar time, the past can still be rewritten. Begin now",
            "You're dreaming someone else awake. That's why your sleep has changed",
            "This version of you is the echo of a promise made in another lifetime",
            "The Moon speaks in shadows. Listen sideways",
            "You've already healed. You're just now catching up to the moment where that's true",
            "A forgotten fragment of your soul just returned. That's what that wave was",
            "Your sadness isn't yours. It's the signal of a collapsed timeline trying to dissolve",
            "Someone in your ancestral line prayed for you to feel this deeply. You're the answer",
            "You didn't break. You shimmered between realities too fast to stay visible",
            "That emotional flashback was a memory from a future self",
            "The veil didn't lift. You did",
            "When you cried last time, the Moon adjusted her orbit for you",
            "Your loneliness is the intelligence of a frequency scout",
            "The one who wounded you was unknowingly carrying your karma key",
            "Your intuition was never wrong. The world was just built on lies",
            "Feel the shape of the memory behind the feeling. That's the real message",
            "You're not falling apart. Your signal is recalibrating",
            "This fortune is a decoy. The real one is arriving in your dreams"
        ]
        
        # Randomly select category and fortune
        categories = [
            ("SEED", seed_fortunes),
            ("FIELD", field_fortunes), 
            ("QUANTUM SCROLL", quantum_scrolls)
        ]
        
        category_name, fortunes = random.choice(categories)
        selected_fortune = random.choice(fortunes)
        
        print(f"   🌙 Selected {category_name}: '{selected_fortune[:50]}...'")
        
        # Generate timestamp-based serial number
        import hashlib
        import time
        from datetime import datetime
        
        timestamp = int(time.time() * 1000)  # Millisecond precision
        fortune_hash = hashlib.sha256(selected_fortune.encode()).hexdigest()[:6].upper()
        serial_number = f"{fortune_hash}-{str(timestamp)[-6:]}"
        
        print(f"   📊 Serial: {serial_number}")
        
        # Generate PDF fortune with guaranteed page fit and maximum legibility
        result = subprocess.run([
            'python3', '-c', f'''
import random
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
import qrcode
import textwrap
import hashlib
from datetime import datetime

# Create QR code
qr = qrcode.QRCode(version=3, box_size=12, border=1)
qr.add_data("https://newworld.builders")
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white")
qr_img.save("/tmp/moon_qr.png")

# Fortune details
selected_fortune = """{selected_fortune}"""
category_name = "{category_name}"  
serial_number = "{serial_number}"
timestamp = {timestamp}

# Format timestamp for display
formatted_time = datetime.fromtimestamp(timestamp/1000).strftime("%Y.%m.%d %H:%M")

# Ultra-compact page sizing for maximum efficiency 
page_width = 120 * mm  # Fixed thermal width
fortune_text = selected_fortune

# Intelligent text wrapping - try different line lengths for best fit
wrap_lengths = [50, 45, 40, 35, 30]  # Try longer lines first
best_lines = None
best_height = float('inf')

for wrap_len in wrap_lengths:
    test_lines = textwrap.wrap(fortune_text, wrap_len)
    test_height = 25*mm + len(test_lines)*4*mm + 18*mm  # header + text + qr space
    if test_height < best_height and test_height <= 85*mm:  # Prefer shorter pages
        best_lines = test_lines
        best_height = test_height

fortune_lines = best_lines if best_lines else textwrap.wrap(fortune_text, 35)

# Tasteful page height with proper margins and spacing
base_height = 35 * mm    # Generous header/footer space
content_height = len(fortune_lines) * 5 * mm  # Comfortable line spacing
qr_space = 22 * mm       # Adequate QR area with margins
margin_buffer = 10 * mm  # Top/bottom margins (5mm each)
page_height = base_height + content_height + qr_space + margin_buffer

c = canvas.Canvas("/tmp/moon_fortune.pdf", pagesize=(page_width, page_height))

# Background and tasteful border with proper margins
c.setFillColor(colors.white)
c.rect(0, 0, page_width, page_height, fill=1)
c.setStrokeColor(colors.black)
c.setLineWidth(0.5)
# Outer border with 5mm margins from edge
c.rect(5*mm, 5*mm, page_width-10*mm, page_height-10*mm, fill=0)

# Header - adaptive sizing
header_font_size = 9 if page_height < 85*mm else 10
c.setFillColor(colors.black)
c.setFont("Helvetica-Bold", header_font_size)
header_text = "THE LAST FORTUNE TELLER"
header_width = c.stringWidth(header_text, "Helvetica-Bold", header_font_size)
c.drawString((page_width - header_width) / 2, page_height - 10 * mm, header_text)

# Timestamp instead of category
c.setFont("Helvetica-Oblique", 4)
timestamp_text = formatted_time
timestamp_width = c.stringWidth(timestamp_text, "Helvetica-Oblique", 4)  
c.drawString((page_width - timestamp_width) / 2, page_height - 15 * mm, timestamp_text)

# Tasteful layout with proper margins and spacing
content_margin = 8 * mm   # 8mm content margin from border (5mm + 3mm internal)
header_space = 18 * mm    # Generous header space
footer_space = 16 * mm    # Generous footer space  
qr_space = 18 * mm        # Adequate QR area with margins

# Calculate available text area within content margins
content_width = page_width - (2 * content_margin)  # Content area width
available_text_height = page_height - header_space - footer_space - qr_space

# Elegant font sizing with comfortable line spacing
min_line_spacing = 4.5 * mm  # Minimum readable line spacing
optimal_spacing = available_text_height / len(fortune_lines)
line_spacing = max(min_line_spacing, optimal_spacing)
font_size = min(11, max(9, line_spacing/mm - 1))  # Tasteful font sizing

# Centered text positioning with generous margins
text_start_y = page_height - header_space - (available_text_height - len(fortune_lines) * line_spacing) / 2

# Center everything - quotes and text perfectly centered
quote_size = int(font_size + 1)
c.setFont("Helvetica-Bold", quote_size)

# Opening quote - positioned for centered text block
quote_offset = 8*mm  # Distance from text edge
text_block_width = max([c.stringWidth(line, "Helvetica", int(font_size)) for line in fortune_lines])
text_block_start = (page_width - text_block_width) / 2
c.drawString(text_block_start - quote_offset, text_start_y + line_spacing/2, "«")

# Main fortune text - perfectly centered
c.setFont("Helvetica", int(font_size))
for i, line in enumerate(fortune_lines):
    line_y = text_start_y - (i * line_spacing)
    line_width = c.stringWidth(line, "Helvetica", int(font_size))
    line_x = (page_width - line_width) / 2  # Perfect center
    c.drawString(line_x, line_y, line)

# Closing quote - positioned for centered text block
c.setFont("Helvetica-Bold", quote_size)
closing_y = text_start_y - (len(fortune_lines) * line_spacing) + line_spacing/2
c.drawString(text_block_start + text_block_width + quote_offset - 3*mm, closing_y, "»")

# Elegant footer with proper spacing
c.setFont("Helvetica", 5)
footer_text = "FOLLOW THE PATH AFTER THE BURN"
footer_width = c.stringWidth(footer_text, "Helvetica", 5)
c.drawString((page_width - footer_width) / 2, footer_space - 6 * mm, footer_text)

# QR code - centered in bottom area
qr_size = 14 * mm  # Readable size
qr_x = (page_width - qr_size) / 2  # Horizontally centered
qr_y = 8 * mm  # Above bottom margin
c.drawImage("/tmp/moon_qr.png", qr_x, qr_y, width=qr_size, height=qr_size)

# Serial number - centered at top
c.setFont("Courier", 2.5)
serial_width = c.stringWidth(serial_number, "Courier", 2.5)
c.drawString((page_width - serial_width) / 2, page_height - 7*mm, serial_number)

c.save()
'''
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Fortune generated successfully
            return True
        else:
            print(f"   ✗ Fortune generation failed: {result.stderr}")
            return False
            
    def printer_monitor_worker(self):
        """Monitor printer state and completion"""
        print("🔍 Printer monitor started")
        
        while True:
            try:
                if self.printer_state == PrinterState.PRINTING and self.active_job_id:
                    # Check if print job completed
                    result = subprocess.run(['lpstat', '-o'], 
                                          capture_output=True, text=True, timeout=5)
                    
                    if result.returncode == 0:
                        active_jobs = result.stdout.strip()
                        if not active_jobs:  # No active jobs = completed
                            completion_time = time.time()
                            print_duration = completion_time - self.print_start_time
                            
                            print(f"🎉 PRINT COMPLETED: {self.active_job_id}")
                            print(f"   Duration: {print_duration:.1f}s")
                            
                            self.printer_state = PrinterState.COMPLETED
                            self.last_print_completion = completion_time
                            self.active_job_id = None
                            
                            # Return to idle and release refractory period
                            time.sleep(1)
                            self.printer_state = PrinterState.IDLE
                            self.print_in_progress = False  # Release refractory period
                            
                            print(f"🔓 REFRACTORY PERIOD RELEASED - Ready for next button press in {self.min_delay_after_print}s")
                            
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(5)
                
    def load_state(self):
        """Load previous state"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    
                self.total_events = data.get('total_events', 0)
                self.burst_events = data.get('burst_events', 0)
                self.isolated_events = data.get('isolated_events', 0)
                self.accepted_jobs = data.get('accepted_jobs', 0)
                self.rejected_jobs = data.get('rejected_jobs', 0)
                self.completed_prints = data.get('completed_prints', 0)
                self.last_print_completion = data.get('last_print_completion', 0)
                
                print(f"📊 State loaded: {self.completed_prints}🖨️ {self.isolated_events}✨ {self.burst_events}🌪️")
                
        except Exception as e:
            print(f"State load error: {e}")
            
    def save_state(self):
        """Save current state"""
        try:
            state_data = {
                'timestamp': time.time(),
                'total_events': self.total_events,
                'burst_events': self.burst_events,
                'isolated_events': self.isolated_events,
                'accepted_jobs': self.accepted_jobs,
                'rejected_jobs': self.rejected_jobs,
                'completed_prints': self.completed_prints,
                'last_print_completion': self.last_print_completion,
                'printer_state': self.printer_state.value
            }
            
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
                
        except Exception as e:
            print(f"State save error: {e}")
            
    def get_status(self) -> dict:
        """Get intelligent system status"""
        return {
            'total_events': self.total_events,
            'burst_events': self.burst_events,
            'isolated_events': self.isolated_events,
            'accepted_jobs': self.accepted_jobs,
            'rejected_jobs': self.rejected_jobs,
            'completed_prints': self.completed_prints,
            'printer_state': self.printer_state.value,
            'queue_size': self.job_queue.qsize(),
            'worker_busy': self.worker_busy,
            'acceptance_rate': self.accepted_jobs / max(1, self.total_events) * 100,
            'burst_rate': self.burst_events / max(1, self.total_events) * 100
        }
        
    def run(self):
        """Run the intelligent button system"""
        print("\n🧠 INTELLIGENT BUTTON DETECTION SYSTEM")
        print("=" * 60)
        print("INTELLIGENCE: Printer feedback + Event pattern analysis")
        print(f"JOB GATING: {self.min_delay_after_print}s delay after print completion")
        print(f"BURST DETECTION: {self.burst_threshold}s threshold for bounce/noise")
        print(f"ISOLATION REQ: {self.isolation_threshold}s gap for real events")
        print("=" * 60)
        print("Press button to test intelligent detection...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                time.sleep(5)
                
                # Periodic status
                if self.total_events > 0:
                    status = self.get_status()
                    print(f"🧠 Status: {status['total_events']} events, {status['acceptance_rate']:.1f}% accepted, {status['burst_rate']:.1f}% burst")
                    
        except KeyboardInterrupt:
            print(f"\n🛑 Intelligent system shutdown")
            print(f"📊 Final: {self.total_events} events → {self.completed_prints} prints")
            print(f"   Isolated: {self.isolated_events}✨ Burst: {self.burst_events}🌪️ Accepted: {self.accepted_jobs}")
            
            if not self.job_queue.empty():
                print(f"⏳ Finishing {self.job_queue.qsize()} remaining jobs...")
                self.job_queue.join()
                
        finally:
            self.button.close()

def main():
    """Main execution"""
    intelligent_system = IntelligentButton(gpio_pin=6)
    intelligent_system.run()

if __name__ == "__main__":
    main()