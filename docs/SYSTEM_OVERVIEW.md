# Burningman Thermal Print System

**Hardware**: Raspberry Pi 5 + GPIO button (pin 6) + Y812BT thermal printer via USB

**Software**: Python 3.11 with uv environment, gpiozero GPIO library, CUPS printing

**Flow**:
1. Physical button press → GPIO interrupt
2. Python handler executes `print_haiku()` 
3. Direct print via `./print-now.sh` (USB detection + raw print commands)
4. Fallback to CUPS `lp -d Y812BT haiku.txt` if direct fails
5. Status message printed to console

**Content**: Prints "Context distilled in geometric form" haiku to 58mm thermal paper

**Status**: Button detection ✅ | GPIO handler ✅ | Printer connection ❌ (Y812BT not detected)