#!/bin/bash
# Immediate print test - bypasses GPIO button for direct testing

echo "🖨️  IMMEDIATE PRINT TEST"
echo "======================"

# Check if printer is connected
if ! lsusb | grep -q "5958:0130"; then
    echo "❌ Y812BT printer not detected"
    echo "Connect printer to USB hub and try again"
    exit 1
fi

# Check if device node exists
if [ ! -c /dev/usb/lp0 ]; then
    echo "❌ Printer device /dev/usb/lp0 not found"
    echo "Printer may be disconnected or driver not loaded"
    exit 1
fi

echo "✅ Printer detected and ready"
echo ""

# Print the haiku
echo "Printing haiku..."
sudo bash -c 'echo -e "\x1b@Context distilled,\nIn geometric form --\nInductive bias,\nResonating worlds\n\n\n\x1bi" > /dev/usb/lp0'

if [ $? -eq 0 ]; then
    echo "✅ Print command sent successfully!"
    echo ""
    echo "📄 Haiku should be printing now:"
    echo "   Context distilled,"
    echo "   In geometric form --"
    echo "   Inductive bias,"
    echo "   Resonating worlds"
else
    echo "❌ Print command failed"
    exit 1
fi