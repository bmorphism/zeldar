#!/usr/bin/env python3
"""
Corrected Precision Fortune for Actual Sticky Dimensions
Based on calibration test results
"""

def create_safe_sticky_fortune():
    """Create fortune that definitely fits on sticky without overprinting"""
    
    # Conservative safe dimensions (will adjust based on boundary test)
    SAFE_WIDTH = 28  # Characters (even more conservative)
    SAFE_HEIGHT = 18 # Lines (leave room for cut and margins)
    
    lines = [
        "ヲヲヲ welcome to Uncommons",      # Shortened to fit
        "(symplectomorphic cobordism)",     # Shortened  
        "",
        "no official universe-agent",      # Simplified
        "every _ is unofficial agent",     # Shortened
        "",
        "-----",
        "Context distilled,",
        "geometric form --", 
        "bias resonating",
        "worlds",
        "",
        "yours truly,",
        "reafferent reaberrant"
    ]
    
    # Ensure each line fits in safe width
    safe_lines = []
    for line in lines:
        if len(line) <= SAFE_WIDTH:
            safe_lines.append(line)
        else:
            # Split long lines
            words = line.split()
            current_line = ""
            for word in words:
                if len(current_line + word + " ") <= SAFE_WIDTH:
                    current_line += word + " "
                else:
                    if current_line:
                        safe_lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                safe_lines.append(current_line.strip())
    
    # Limit to safe height
    safe_lines = safe_lines[:SAFE_HEIGHT-2]  # Leave room for cut commands
    
    # Generate ESC/POS command
    esc_pos_init = "\x1b@"
    esc_pos_cut = "\x1bi"
    
    command = esc_pos_init
    for line in safe_lines:
        command += line + "\n"
    
    command += "\n"  # Single spacing before cut
    command += esc_pos_cut
    
    return command

def update_print_script():
    """Generate corrected print command for print-now.sh"""
    
    safe_fortune = create_safe_sticky_fortune()
    
    print("🔧 CORRECTED STICKY FORTUNE:")
    print("=" * 30)
    
    # Preview the output
    lines = safe_fortune.split('\n')
    for i, line in enumerate(lines[1:-2]):  # Skip ESC commands
        if line:  # Skip empty lines in display
            print(f"{i+1:2d}|{line}|")
    
    print("=" * 30)
    print(f"Total printable lines: {len([l for l in lines[1:-2] if l])}")
    print(f"Max line width: {max(len(l) for l in lines[1:-2] if l)} chars")
    
    return safe_fortune

if __name__ == "__main__":
    corrected_command = update_print_script()
    
    # Save the corrected command
    with open('/home/zeldar/burningman/safe_fortune_command.txt', 'w') as f:
        f.write(corrected_command)
    
    print("\n💾 Saved corrected command to safe_fortune_command.txt")
    print("🎯 This format should fit perfectly on sticky labels!")
    print("\n📋 Next steps:")
    print("1. Check the boundary test print to verify sticky size")
    print("2. If boundary test fits well, use this corrected format")
    print("3. Update print-now.sh with the safe command")