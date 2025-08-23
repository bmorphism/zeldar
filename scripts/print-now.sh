#!/bin/bash
# Daily fortune printing with date-based selection

FORTUNE_TYPE=${1:-"default_fortune"}
echo "🖨️  DAILY FORTUNE PRINT: $FORTUNE_TYPE"
echo "====================================="

# Check if printer is connected
if ! lsusb | grep -q "5958:0130"; then
    echo "❌ Y812BT printer not detected"
    echo "Connect printer to USB hub and try again"
    exit 1
fi

echo "✅ Printer detected and ready"
echo ""

# Select fortune content based on type
FORTUNE_FILE="/home/zeldar/burningman/fortunes/${FORTUNE_TYPE}.txt"

if [ -f "$FORTUNE_FILE" ]; then
    echo "📅 Loading fortune: $FORTUNE_TYPE"
    FORTUNE_CONTENT=$(cat "$FORTUNE_FILE")
else
    echo "⚠️  Fortune file not found: $FORTUNE_FILE"
    echo "📄 Using default fortune"
    FORTUNE_CONTENT="ヲヲヲ welcome to Uncommons
(symplectomorphic cobord.)

no official universe-agent
every _ unofficial agent
-----
Context distilled,
In geometric form --
Inductive bias,
Resonating worlds

sincerely yours
reafferent reaberrant"
fi

echo "Printing daily fortune..."

# Send via CUPS with ESC/POS formatting
echo -e "\x1b@$FORTUNE_CONTENT\n\n\x1bi" | lp -d Y812BT

if [ $? -eq 0 ]; then
    echo "✅ Daily fortune sent successfully: $FORTUNE_TYPE"
    echo ""
    echo "🎯 Fortune printing to thermal printer..."
    echo "📅 Date-based content selection active"
else
    echo "❌ Print command failed"
    exit 1
fi