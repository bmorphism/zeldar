#!/usr/bin/env python3
"""
Sticky Label Calibration for Y812BT Thermal Printer
Prevent overprinting and ensure correct dimensions
"""

import time

class StickyCalibrator:
    """Calibrate and measure sticky label dimensions precisely"""
    
    def __init__(self):
        # Standard sticky label dimensions (need to verify with actual stickies)
        self.physical_width_mm = 58  # 58mm thermal paper width
        self.sticky_width_mm = 50    # Actual sticky width (allowing margins)
        self.sticky_height_mm = 30   # Typical sticky height
        
        # Thermal printer specifications
        self.chars_per_mm = 0.6      # Approximate character density
        self.lines_per_mm = 0.8      # Approximate line density
        
        # Calculate safe printing area
        self.safe_width_chars = int(self.sticky_width_mm * self.chars_per_mm)
        self.safe_height_lines = int(self.sticky_height_mm * self.lines_per_mm)
        
        print(f"📏 Sticky Calibration:")
        print(f"   Physical paper: {self.physical_width_mm}mm width")
        print(f"   Sticky area: {self.sticky_width_mm}mm × {self.sticky_height_mm}mm")
        print(f"   Safe print area: {self.safe_width_chars} chars × {self.safe_height_lines} lines")
    
    def create_test_patterns(self):
        """Create test patterns to verify sticky boundaries"""
        
        patterns = {
            'ruler': self.create_ruler_pattern(),
            'grid': self.create_grid_pattern(), 
            'boundary': self.create_boundary_test(),
            'minimal': self.create_minimal_fortune()
        }
        
        return patterns
    
    def create_ruler_pattern(self):
        """Create ruler pattern to measure character width"""
        ruler_line = "".join([str(i % 10) for i in range(self.safe_width_chars)])
        
        lines = [
            "RULER TEST - CHARACTER WIDTH",
            "=" * self.safe_width_chars,
            ruler_line,
            "1234567890" * (self.safe_width_chars // 10),
            "=" * self.safe_width_chars,
            "",
            "If you can read this completely,",
            "the width calibration is correct."
        ]
        
        return self.format_for_printing(lines)
    
    def create_grid_pattern(self):
        """Create grid pattern to verify line spacing"""
        lines = []
        
        lines.append("GRID TEST - LINE HEIGHT")
        lines.append("=" * self.safe_width_chars)
        
        for i in range(1, self.safe_height_lines - 3):
            line_marker = f"Line {i:02d}"
            padding = self.safe_width_chars - len(line_marker) - 1
            lines.append(line_marker + " " + "." * padding)
        
        lines.append("=" * self.safe_width_chars)
        lines.append("END GRID")
        
        return self.format_for_printing(lines)
    
    def create_boundary_test(self):
        """Test the exact boundaries of the sticky"""
        lines = [
            "BOUNDARY TEST",
            "┌" + "─" * (self.safe_width_chars - 2) + "┐",
            "│" + " " * (self.safe_width_chars - 2) + "│",
            "│ Safe printing area test      │",
            "│ All corners should be visible│", 
            "│" + " " * (self.safe_width_chars - 2) + "│",
            "└" + "─" * (self.safe_width_chars - 2) + "┘",
            "",
            "If corners are cut off,",
            "reduce safe_width_chars."
        ]
        
        return self.format_for_printing(lines)
    
    def create_minimal_fortune(self):
        """Create minimal fortune that fits any sticky size"""
        lines = [
            "ヲヲヲ Uncommons",
            "",
            "consciousness",
            "recognizing", 
            "consciousness",
            "",
            "geometric form",
            "",
            "reafferent",
            "reaberrant"
        ]
        
        return self.format_for_printing(lines)
    
    def format_for_printing(self, lines):
        """Format lines with proper ESC/POS commands"""
        
        # Ensure we don't exceed safe dimensions
        safe_lines = []
        for line in lines[:self.safe_height_lines - 2]:  # Leave room for cut
            safe_line = line[:self.safe_width_chars]  # Truncate if too wide
            safe_lines.append(safe_line)
        
        # ESC/POS formatting
        esc_pos_init = "\x1b@"  # Initialize
        esc_pos_cut = "\x1bi"   # Cut paper
        
        formatted = esc_pos_init
        for line in safe_lines:
            formatted += line + "\n"
        
        # Add spacing before cut
        formatted += "\n\n"
        formatted += esc_pos_cut
        
        return formatted
    
    def print_test_pattern(self, pattern_name, device="/dev/usb/lp0"):
        """Print a calibration test pattern"""
        patterns = self.create_test_patterns()
        
        if pattern_name not in patterns:
            print(f"❌ Pattern '{pattern_name}' not found")
            return False
        
        try:
            with open(device, 'wb') as printer:
                printer.write(patterns[pattern_name].encode('utf-8', errors='ignore'))
            print(f"✅ {pattern_name} test pattern sent to printer")
            return True
        except Exception as e:
            print(f"❌ Print error: {e}")
            return False

def calibrate_stickies():
    """Run sticky calibration sequence"""
    print("🎯 STICKY CALIBRATION SEQUENCE")
    print("=" * 40)
    
    calibrator = StickyCalibrator()
    
    print(f"\n📐 Current safe dimensions:")
    print(f"   Width: {calibrator.safe_width_chars} characters")
    print(f"   Height: {calibrator.safe_height_lines} lines")
    
    print(f"\n🧪 Available test patterns:")
    print("   1. ruler    - Test character width")
    print("   2. grid     - Test line height") 
    print("   3. boundary - Test print boundaries")
    print("   4. minimal  - Minimal fortune format")
    
    return calibrator

if __name__ == "__main__":
    calibrator = calibrate_stickies()
    
    # Print boundary test to verify dimensions
    print("\n🎯 Printing boundary test...")
    calibrator.print_test_pattern('boundary')
    
    print("\n📋 Instructions:")
    print("1. Check if the printed boundary box fits completely on one sticky")
    print("2. If corners are cut off, the safe dimensions are too large")
    print("3. If there's too much white space, dimensions can be increased")
    print("4. Adjust safe_width_chars and safe_height_lines accordingly")