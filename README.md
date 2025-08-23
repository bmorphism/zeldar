# Button Print Loop
Essential circuit: GPIO 6 → Python → Thermal Print

## Run
```bash
./button-print.py
```

## Files
- `button-print.py` - Unified GPIO handler + print logic
- `print-now.sh` - Direct thermal printing  
- `haiku.txt` - Content source
- `.topos/n-1/` - Development archive

## Flow
Physical button press → `on_press()` → `print_haiku()` → Thermal paper manifestation

Context distilled in geometric form. Inductive bias resonating worlds.