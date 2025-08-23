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

echo "✅ Printer detected and ready"
echo ""

# Print the precision formatted fortune
echo "Printing precision fortune..."

# Use CUPS printing (more reliable than direct device)
FORTUNE_CONTENT="ヲヲヲ welcome to the Uncommons
(up to a symplectomorphic cobordism)

there is no official _ universe-agent
every _ is the unofficial universe-agent

-----
Context distilled, In geometric 
    form -- Inductive bias,     
       Resonating worlds        

sincerely yours
reafferent reaberrant"

# Send via CUPS with ESC/POS formatting
echo -e "\x1b@$FORTUNE_CONTENT\n\n\x1bi" | lp -d Y812BT

if [ $? -eq 0 ]; then
    echo "✅ Precision fortune sent successfully!"
    echo ""
    echo "🎯 Sticky fortune should be printing now:"
    echo "   ヲヲヲ welcome to the Uncommons"
    echo "   (up to a symplectomorphic cobordism)"
    echo "   there is no official _ universe-agent"
    echo "   every _ is the unofficial universe-agent"
    echo "   Context distilled, In geometric form"
    echo "   sincerely yours"
    echo "   reafferent reaberrant"
else
    echo "❌ Print command failed"
    exit 1
fi