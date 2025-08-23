# Burning Man Art Robot - Thermal Printer System
# Run `just --list` to see all available commands

# Default recipe shows help
default:
    @just --list

# 🚀 Production Commands

# Start the GPIO button daemon (requires sudo)
start:
    @echo "🚀 Starting Burning Man Art Robot..."
    @echo "📍 GPIO 6 → Thermal Print (5s cooldown)"
    @echo "📅 Fortune schedule: Burning Man 2025 (Aug 24-31)"
    sudo uv run python src/controlled_button.py

# Print current daily fortune
print:
    @echo "🖨️ Printing today's fortune..."
    ./scripts/print-now.sh

# Print specific fortune type
print-fortune fortune_type:
    @echo "🖨️ Printing {{fortune_type}} fortune..."
    ./scripts/print-now.sh {{fortune_type}}

# 🧪 Testing Commands

# Run all tests
test:
    @echo "🧪 Running fortune schedule tests..."
    uv run python tests/test_direct_fortune.py
    @echo ""
    uv run python tests/test_fortune_schedule.py

# Test GPIO button functionality (5 second timeout)
test-gpio:
    @echo "🔘 Testing GPIO button (press button within 5 seconds)..."
    timeout 5 python3 -c "from gpiozero import Button; from signal import pause; print('Press button on GPIO 6...'); Button(6).when_pressed = lambda: print('✅ Button works!'); pause()" || echo "⏰ Test timeout - button may not be connected"

# Test printer connectivity
test-printer:
    @echo "🖨️ Testing Y812BT thermal printer..."
    @lsusb | grep -q "5958:0130" && echo "✅ Y812BT printer detected" || echo "❌ Printer not found"
    @ls -la /dev/usb/lp0 2>/dev/null && echo "✅ Device node exists" || echo "❌ Device node missing"
    @lpstat -p Y812BT 2>/dev/null | grep -q "accepting" && echo "✅ CUPS printer ready" || echo "❌ CUPS printer not configured"

# 📅 Fortune Management

# Show current fortune for today
show-fortune:
    @uv run python scripts/show_fortune.py

# List all available fortunes
list-fortunes:
    @uv run python scripts/list_fortunes.py

# Test fortune schedule for specific date (YYYY-MM-DD)
test-date date:
    @uv run python scripts/test_date.py {{date}}

# 🔧 System Commands

# Show system status
status:
    @echo "🎯 Burning Man Art Robot Status"
    @echo "================================"
    @echo ""
    @echo "📦 Environment:"
    @python3 --version
    @uv --version 2>/dev/null || echo "uv: not installed"
    @echo ""
    @echo "🖨️ Printer:"
    @just test-printer
    @echo ""
    @echo "📅 Current Fortune:"
    @just show-fortune
    @echo ""
    @echo "⚡ Last Print:"
    @if [ -f "last_print.json" ]; then \
        python3 -c "import json, time; data=json.load(open('last_print.json')); print(f'   {time.strftime(\"%Y-%m-%d %H:%M:%S\", time.localtime(data[\"last_print_time\"]))}')"; \
    else \
        echo "   No prints recorded"; \
    fi
    @echo ""
    @echo "🔧 Process:"
    @pgrep -f "controlled_button.py" >/dev/null && echo "   ✅ GPIO daemon running" || echo "   ⏸️  GPIO daemon stopped"

# Install/update dependencies
setup:
    @echo "📦 Setting up Burning Man Art Robot..."
    uv sync
    @echo "✅ Dependencies installed"
    @echo "💡 Add user to 'lp' group for printer access:"
    @echo "   sudo usermod -a -G lp $(whoami)"

# Clean up temporary files
clean:
    @echo "🧹 Cleaning temporary files..."
    @rm -f *.pyc
    @find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    @echo "✅ Cleaned"

# 🔄 Development Commands

# Format code
fmt:
    @echo "🎨 Formatting code..."
    @command -v black >/dev/null && black src/ tests/ || echo "⚠️  black not installed"
    @echo "✅ Formatted"

# Run linter
lint:
    @echo "🔍 Linting code..."
    @command -v flake8 >/dev/null && flake8 src/ tests/ || echo "⚠️  flake8 not installed"
    @echo "✅ Linted"

# Watch for file changes and run tests
watch:
    @echo "👀 Watching for changes..."
    @command -v watchexec >/dev/null && watchexec -e py -- just test || echo "⚠️  watchexec not installed"

# 📊 Monitoring Commands

# Show print statistics
stats:
    @echo "📊 Print Statistics"
    @echo "==================="
    @if [ -f "runtime_status.json" ]; then \
        echo "📄 Runtime data found"; \
        python3 -c "import json; data=json.load(open('runtime_status.json')); print('   Activity log available')" 2>/dev/null || echo "   No valid data"; \
    else \
        echo "📄 No runtime data"; \
    fi
    @if [ -f "last_print.json" ]; then \
        echo "⏰ Last print recorded"; \
    else \
        echo "⏰ No prints yet"; \
    fi

# Monitor system logs for printer activity
logs:
    @echo "📋 Monitoring system logs for printer activity..."
    @echo "Press Ctrl+C to stop"
    sudo journalctl -f -u cups | grep -i "y812bt\|thermal\|print" || echo "No recent printer activity"

# 🚀 Deployment Commands

# Package for deployment
package:
    @echo "📦 Packaging for Burning Man deployment..."
    @mkdir -p dist
    @tar -czf dist/burningman-art-robot-$(date +%Y%m%d).tar.gz \
        --exclude='.git' \
        --exclude='dist' \
        --exclude='.venv' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        .
    @echo "✅ Package created in dist/"

# Quick deployment test
deploy-test:
    @echo "🎯 Deployment Test Sequence"
    @echo "============================"
    just setup
    just test
    just test-printer
    @echo "✅ Deployment test complete"

# 📚 Documentation

# Generate system diagram
diagram:
    @echo "📊 Generating system architecture diagram..."
    uv run python src/system_diagram.py

# Show fortune schedule
schedule:
    @echo "📅 Burning Man 2025 Fortune Schedule"
    @echo "===================================="
    @echo ""
    @echo "Aug 24 (Sun) → sunday_opening_fortunes"
    @echo "Aug 25 (Mon) → monday_sequence"
    @echo "Aug 26 (Tue) → tuesday_sequence"  
    @echo "Aug 27 (Wed) → wednesday_sequence"
    @echo "Aug 28 (Thu) → thursday_sequence"
    @echo "Aug 29 (Fri) → friday_sequence"
    @echo "Aug 30 (Sat) → saturday_closing"
    @echo "Aug 31 (Sun) → special_fortunes ⭐"
    @echo ""
    @echo "Other dates → default_fortune"

# Show help for specific topic
help topic="":
    @if [ "{{topic}}" = "printing" ]; then \
        echo "🖨️ Printing Help:"; \
        echo "  just print          - Print today's fortune"; \
        echo "  just print-fortune TYPE - Print specific fortune"; \
        echo "  just test-printer   - Test printer connectivity"; \
    elif [ "{{topic}}" = "gpio" ]; then \
        echo "🔘 GPIO Help:"; \
        echo "  just start          - Start button daemon"; \
        echo "  just test-gpio      - Test button functionality"; \
        echo "  Button: GPIO pin 6, requires 0.5s hold"; \
    elif [ "{{topic}}" = "fortunes" ]; then \
        echo "📅 Fortune Help:"; \
        echo "  just show-fortune   - Current fortune"; \
        echo "  just list-fortunes  - All available fortunes"; \
        echo "  just schedule       - Burning Man schedule"; \
        echo "  just test-date DATE - Test specific date"; \
    else \
        echo "🎯 Burning Man Art Robot"; \
        echo "Available help topics:"; \
        echo "  just help printing  - Printing commands"; \
        echo "  just help gpio      - GPIO button commands"; \
        echo "  just help fortunes  - Fortune management"; \
    fi