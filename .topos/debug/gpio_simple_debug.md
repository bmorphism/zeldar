# Simple GPIO Debugging Methods

## Quick Tests

### 1. **One-liner Value Check**
```bash
python3 -c "from gpiozero import DigitalInputDevice; pin=DigitalInputDevice(6, pull_up=True); print('GPIO 6:', pin.value)"
```

### 2. **Background GPIO Monitor**
```bash
# Start background process
nohup python3 gpio_debug.py 6 > /tmp/gpio.log 2>&1 &

# Monitor output
tail -f /tmp/gpio.log

# Check if running
ps aux | grep gpio
```

### 3. **Direct GPIO Value**
```bash
# Export pin first
echo 6 > /sys/class/gpio/export 2>/dev/null
# Read value
cat /sys/class/gpio/gpio6/value
```

### 4. **Kill All GPIO Processes**
```bash
pkill -f gpio
kill $(ps aux | grep 'python.*gpio' | awk '{print $2}')
```

### 5. **Test Both Pull Configurations**
```bash
python3 continuous_listener.py
```

### 6. **Quick Pin Scan**
```bash
python3 gpio_debug.py scan
```

### 7. **Hardware Check**
```bash
# Check USB devices (if using Pi)
lsusb | grep -i gpio

# Check GPIO info
gpioinfo 2>/dev/null | grep -E "line.*6"

# List exported pins
ls /sys/class/gpio/
```

### 8. **Simple Test Script**
```python
#!/usr/bin/env python3
from gpiozero import Button
import time

button = Button(6, pull_up=True, bounce_time=None)
print("Listening... Press Ctrl+C to stop")

def on_press():
    print(f"PRESS! {time.time()}")

button.when_pressed = on_press

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped")
```

## Troubleshooting

- **GPIO Busy**: Kill existing processes first
- **No Events**: Check pull configuration (True vs False)  
- **Too Many Events**: Add bounce_time or cooldown
- **Wrong Pin**: Use scan mode to find active pin

## Current Setup
- **Pin**: GPIO 6
- **Pull**: `pull_up=True` (button to GND)
- **Trigger**: Falling edge (HIGH→LOW when pressed)