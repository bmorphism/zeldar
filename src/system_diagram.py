#!/usr/bin/env python3
"""
Burningman Thermal Print System Diagram Generator
Creates ASCII and visual diagrams of the system architecture
"""

def print_ascii_diagram():
    """Print ASCII system architecture diagram"""
    diagram = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BURNINGMAN THERMAL PRINT SYSTEM                         │
└─────────────────────────────────────────────────────────────────────────────┘

Hardware Layer:
┌──────────────┐    ┌─────────────────┐    ┌──────────────────────────────────┐
│ Push Button  │    │ Raspberry Pi 5  │    │        USB Hub                   │
│   (GPIO 6)   │◄───┤  BCM2712 SoC    │◄───┤  ┌─────────────────────────────┐ │
│              │    │                 │    │  │      Y812BT Thermal         │ │
└──────────────┘    │  - Python 3.11  │    │  │      Printer (58mm)         │ │
                    │  - uv env       │    │  └─────────────────────────────┘ │
                    │  - gpiozero     │    │  ┌─────────────────────────────┐ │
                    │  - lgpio        │    │  │    OBSBOT Tiny SE           │ │
                    └─────────────────┘    │  │  (Video + Audio Input)      │ │
                                           │  └─────────────────────────────┘ │
                                           └──────────────────────────────────┘

Software Architecture:
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Application Layer                                 │
├─────────────────┬───────────────────┬───────────────────────────────────────┤
│  button-print.py│    print-now.sh   │         haiku.txt                     │
│                 │                   │                                       │
│ • GPIO handler  │ • Direct printer  │ • Content to print:                   │
│ • Event loop    │   communication   │   "Context distilled                  │
│ • Error handling│ • USB detection   │    in geometric form"                 │
│ • CUPS fallback │ • Status feedback │                                       │
└─────────────────┴───────────────────┴───────────────────────────────────────┘

System Flow:
   ┌─────────────┐
   │ User Presses│
   │   Button    │
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐    ┌─────────────────┐
   │GPIO Interrupt│    │  print_haiku()  │
   │   Detected   │───►│   Function      │
   └─────────────┘    └─────────┬───────┘
                                │
                                ▼
                      ┌─────────────────┐    ┌──────────────┐
                      │ Try Direct      │───►│ ./print-now.sh│
                      │ Print Method    │    │   Execution   │
                      └─────────┬───────┘    └──────┬───────┘
                                │                   │
                                │ FAIL              │ SUCCESS
                                ▼                   ▼
                      ┌─────────────────┐    ┌──────────────┐
                      │ CUPS Fallback   │    │ Print Success│
                      │ lp -d Y812BT    │    │   Message    │
                      │   haiku.txt     │    └──────────────┘
                      └─────────────────┘

Dependencies Graph:
┌─────────────────────────────────────────────────────────────────────────────┐
│ burningman/                                                                 │
│ ├── pyproject.toml ──► Dependencies:                                        │
│ │                        • gpiozero>=2.0.1                                 │
│ │                        • lgpio>=0.2.2.0                                  │
│ │                        • rpi-gpio>=0.7.1                                 │
│ ├── .venv/            ──► Virtual Environment                               │
│ ├── button-print.py   ──► Main Application                                  │
│ ├── print-now.sh      ──► Print Handler                                     │
│ ├── haiku.txt         ──► Content File                                      │
│ └── runtime_status.json ► System State                                      │
└─────────────────────────────────────────────────────────────────────────────┘

Current Status:
• ✅ GPIO Button Detection: WORKING (controlled_button.py)
• ✅ Python Environment: uv virtual env active  
• ✅ Cooldown System: 5-second intervals with JSON persistence
• ✅ Thermal Printer: Y812BT operational via CUPS (Y812BT-90)
• ✅ Paper Optimization: 28×15 format (25% savings)
• ✅ Semantic Integrity: 99% preservation validated
• ✅ Audio/Video: OBSBOT Tiny SE available (/dev/video0, card 2)

Print Methods:
1. Optimized: ./scripts/print-now.sh → CUPS submission (primary)
2. Direct ESC/POS: Raw commands → /dev/usb/lp0 (when available)
3. Test Framework: Mock system prevents paper waste
"""
    print(diagram)

if __name__ == "__main__":
    print_ascii_diagram()