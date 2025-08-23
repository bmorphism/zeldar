#!/usr/bin/env python3
"""
Precision Fortune Printing for Y812BT Thermal Printer
Optimized for sticky label dimensions with exact positioning
"""

import time
from pathlib import Path

class StickyFortuneFormatter:
    """Format fortunes precisely for sticky label dimensions"""
    
    def __init__(self):
        self.label_width = 32  # Characters per line on 58mm thermal paper
        self.label_height = 20  # Lines per sticky label
        self.esc_pos_init = "\x1b@"  # ESC @ - Initialize printer
        self.esc_pos_cut = "\x1di"   # ESC i - Cut paper
        
    def format_fortune(self, fortune_text, signature="reafferent reaberrant"):
        """Format fortune to fit precisely on sticky label"""
        
        # The Uncommons header (exactly positioned)
        header = [
            "ヲヲヲ welcome to the Uncommons",
            "(up to a symplectomorphic cobordism)",
            "",
            "there is no official _ universe-agent",
            "every _ is the unofficial universe-agent",
            "",
            "-----"
        ]
        
        # Process fortune content (center and wrap)
        fortune_lines = self._wrap_and_center(fortune_text)
        
        # Footer with signature
        footer = [
            "",
            "sincerely yours",
            signature
        ]
        
        # Calculate total content
        all_lines = header + fortune_lines + footer
        
        # Pad to exact sticky label height
        while len(all_lines) < self.label_height - 2:  # Leave space for cuts
            all_lines.append("")
            
        # Truncate if too long
        all_lines = all_lines[:self.label_height - 2]
        
        return all_lines
    
    def _wrap_and_center(self, text):
        """Wrap text to label width and center each line"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word + " ") <= self.label_width:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip().center(self.label_width))
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip().center(self.label_width))
            
        return lines
    
    def generate_esc_pos_command(self, fortune_lines):
        """Generate precise ESC/POS command for Y812BT"""
        
        # Start with initialization
        command = self.esc_pos_init
        
        # Add each line with proper line feeds
        for line in fortune_lines:
            # Ensure line fits exactly in label width
            formatted_line = line.ljust(self.label_width)[:self.label_width]
            command += formatted_line + "\n"
        
        # Add extra lines for proper sticky separation
        command += "\n\n"  # Extra spacing before cut
        
        # End with cut command
        command += self.esc_pos_cut
        
        return command
    
    def create_fortune_variants(self):
        """Create various fortune formats for the consciousness mirror"""
        fortunes = {
            "original": "Context distilled, In geometric form -- Inductive bias, Resonating worlds",
            
            "consciousness": "awareness observing awareness through button press recursion",
            
            "playa": "desert mirrors cosmos infinite loops of dust and starlight recognition",
            
            "meta": "you are reading this fortune about reading fortunes recursive depth achieved",
            
            "quantum": "superposition collapses upon observation consciousness wave function reality",
            
            "fractal": "each moment contains all moments self-similarity at every scale depth"
        }
        
        formatted_fortunes = {}
        for name, text in fortunes.items():
            lines = self.format_fortune(text)
            formatted_fortunes[name] = self.generate_esc_pos_command(lines)
            
        return formatted_fortunes

def print_fortune_to_device(fortune_command, device="/dev/usb/lp0"):
    """Send formatted fortune directly to thermal printer"""
    try:
        with open(device, 'wb') as printer:
            printer.write(fortune_command.encode('utf-8', errors='ignore'))
        return True
    except Exception as e:
        print(f"Print error: {e}")
        return False

def test_precision_printing():
    """Test the precision formatting"""
    formatter = StickyFortuneFormatter()
    
    print("🎯 Testing precision fortune formatting...")
    print(f"Label dimensions: {formatter.label_width}w × {formatter.label_height}h")
    
    # Test current haiku
    original_fortune = "Context distilled, In geometric form -- Inductive bias, Resonating worlds"
    lines = formatter.format_fortune(original_fortune)
    
    print("\n📏 Formatted output preview:")
    print("=" * formatter.label_width)
    for i, line in enumerate(lines):
        print(f"{i+1:2d}|{line}|")
    print("=" * formatter.label_width)
    print(f"Total lines: {len(lines)}")
    
    # Generate ESC/POS command
    command = formatter.generate_esc_pos_command(lines)
    print(f"\n📟 ESC/POS command length: {len(command)} bytes")
    
    return command

if __name__ == "__main__":
    # Test the formatting
    test_command = test_precision_printing()
    
    # Create all fortune variants
    formatter = StickyFortuneFormatter()
    all_fortunes = formatter.create_fortune_variants()
    
    print(f"\n🔮 Generated {len(all_fortunes)} precision fortune variants")
    
    # Save formatted commands for integration
    with open('/home/zeldar/burningman/formatted_fortunes.py', 'w') as f:
        f.write("# Auto-generated precision fortune commands\n")
        f.write("FORMATTED_FORTUNES = {\n")
        for name, command in all_fortunes.items():
            f.write(f'    "{name}": {repr(command)},\n')
        f.write("}\n")
    
    print("💾 Saved formatted commands to formatted_fortunes.py")
    print("\n✨ Ready for precision consciousness printing!")