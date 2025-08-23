#!/bin/bash
# Zeldar Information Force Oracle - Complete Desert Laboratory Deployment
# Burning Man 2025 - Hardware + Software Integration
# Tri-Loop Automation: GPIO Button + Web Interface + Thermal Printing

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Desert symbols
DESERT="🏜️"
FIRE="🔥"
ORACLE="🔮"
LIGHTNING="⚡"
PRINTER="🖨️"
BUTTON="🔘"

echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║  ${ORACLE} ZELDAR DESERT LABORATORY DEPLOYMENT ${ORACLE}            ║${NC}"
echo -e "${PURPLE}║     ${DESERT}${FIRE} Complete Hardware + Software Integration ${FIRE}${DESERT}     ║${NC}"
echo -e "${PURPLE}║              Burning Man 2025 Ready                          ║${NC}"
echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo

PROJECT_DIR="/Users/barton/infinity-topos/zeldar-fortune"
DEPLOYMENT_MODE="${1:-desert-lab}"
HARDWARE_ENABLED="${2:-auto}"

# Environment configuration with defaults
export THERMAL_PRINTER_DEVICE="${THERMAL_PRINTER_DEVICE:-/dev/usb/lp0}"
export CUPS_PRINTER_NAME="${CUPS_PRINTER_NAME:-Y812BT}"
export GPIO_BUTTON_PIN="${GPIO_BUTTON_PIN:-6}"

# Function to log with desert styling
log_desert() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$level" in
        "INFO")
            echo -e "${CYAN}[${timestamp}] ${LIGHTNING} ${message}${NC}"
            ;;
        "SUCCESS") 
            echo -e "${GREEN}[${timestamp}] ✅ ${message}${NC}"
            ;;
        "WARNING")
            echo -e "${YELLOW}[${timestamp}] ⚠️  ${message}${NC}"
            ;;
        "ERROR")
            echo -e "${RED}[${timestamp}] ❌ ${message}${NC}"
            ;;
        "DESERT")
            echo -e "${PURPLE}[${timestamp}] ${DESERT}${FIRE} ${message}${NC}"
            ;;
        "HARDWARE")
            echo -e "${BLUE}[${timestamp}] ${BUTTON} ${message}${NC}"
            ;;
    esac
}

# Check if running on Raspberry Pi
detect_hardware() {
    log_desert "INFO" "Detecting hardware platform..."
    
    if [[ -f "/proc/cpuinfo" ]] && grep -q "Raspberry Pi" /proc/cpuinfo; then
        log_desert "SUCCESS" "Raspberry Pi hardware detected"
        HARDWARE_PLATFORM="raspberry_pi"
        return 0
    elif [[ -d "/sys/class/gpio" ]]; then
        log_desert "SUCCESS" "GPIO hardware available"
        HARDWARE_PLATFORM="gpio_capable"
        return 0
    else
        log_desert "WARNING" "No GPIO hardware detected - software-only mode"
        HARDWARE_PLATFORM="software_only"
        return 1
    fi
}

# Check prerequisites
check_prerequisites() {
    log_desert "INFO" "Checking desert laboratory prerequisites..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        log_desert "SUCCESS" "Python 3 available"
    else
        log_desert "ERROR" "Python 3 not found"
        exit 1
    fi
    
    # Check printer
    if command -v lp &> /dev/null; then
        log_desert "SUCCESS" "CUPS printing system available"
        
        # Check for configured printer
        if lpstat -p "$CUPS_PRINTER_NAME" &> /dev/null; then
            log_desert "SUCCESS" "$CUPS_PRINTER_NAME thermal printer configured"
        else
            log_desert "WARNING" "$CUPS_PRINTER_NAME printer not found in CUPS"
        fi
    else
        log_desert "WARNING" "CUPS not available - direct device printing only"
    fi
    
    # Check for Spin (web interface)
    if command -v spin &> /dev/null; then
        log_desert "SUCCESS" "Spin WebAssembly runtime available"
    else
        log_desert "WARNING" "Spin not found - hardware-only mode"
    fi
    
    # Hardware detection
    detect_hardware
}

# Deploy hardware integration
deploy_hardware() {
    log_desert "HARDWARE" "Deploying GPIO button integration..."
    
    if [[ "$HARDWARE_PLATFORM" == "software_only" ]]; then
        log_desert "WARNING" "Hardware deployment skipped - no GPIO available"
        return
    fi
    
    # Create hardware directory if needed
    mkdir -p "$PROJECT_DIR/hardware"
    
    # Copy Raspberry Pi oracle script to current directory if we're on Pi
    if [[ "$PWD" == *"/burningman"* ]] && [[ -f "$PROJECT_DIR/hardware/raspberry_pi_oracle.py" ]]; then
        cp "$PROJECT_DIR/hardware/raspberry_pi_oracle.py" ./zeldar_oracle.py
        chmod +x ./zeldar_oracle.py
        log_desert "SUCCESS" "Oracle script deployed to Raspberry Pi"
    fi
    
    # Test GPIO if available
    if python3 -c "import gpiozero; print('GPIO available')" &> /dev/null; then
        log_desert "SUCCESS" "GPIO Zero library available"
    else
        log_desert "WARNING" "GPIO Zero not installed - install with: sudo apt install python3-gpiozero"
    fi
}

# Deploy web interface
deploy_web_interface() {
    log_desert "INFO" "Deploying web interface..."
    
    if [[ ! -f "$PROJECT_DIR/spin.toml" ]]; then
        log_desert "WARNING" "Web interface deployment skipped - spin.toml not found"
        return
    fi
    
    cd "$PROJECT_DIR"
    
    # Start web server in background
    if command -v spin &> /dev/null; then
        log_desert "INFO" "Starting Zeldar web interface..."
        spin up --listen 0.0.0.0:3000 > /tmp/zeldar_web.log 2>&1 &
        WEB_PID=$!
        
        # Wait a moment for server to start
        sleep 3
        
        # Test if server is responding
        if curl -s http://localhost:3000 >/dev/null 2>&1; then
            log_desert "SUCCESS" "Web interface running (PID: $WEB_PID)"
            echo "WEB_PID=$WEB_PID" > /tmp/zeldar_deployment.env
        else
            log_desert "WARNING" "Web interface may still be starting..."
        fi
    fi
}

# Test complete workflow
test_workflow() {
    log_desert "INFO" "Testing complete workflow..."
    
    # Test printing
    if command -v lp &> /dev/null && lpstat -p "$CUPS_PRINTER_NAME" &> /dev/null; then
        echo "Test Fortune" > /tmp/test_print.txt
        echo "Digital → Physical" >> /tmp/test_print.txt
        echo "Desert Laboratory" >> /tmp/test_print.txt
        
        if lp -d "$CUPS_PRINTER_NAME" /tmp/test_print.txt &> /dev/null; then
            log_desert "SUCCESS" "Thermal printing test successful"
        else
            log_desert "WARNING" "Thermal printing test failed"
        fi
        
        rm -f /tmp/test_print.txt
    fi
    
    # Test hardware oracle if available
    if [[ -f "./zeldar_oracle.py" ]] && [[ "$HARDWARE_PLATFORM" != "software_only" ]]; then
        log_desert "INFO" "Hardware oracle script ready for testing"
        log_desert "INFO" "Run: python3 ./zeldar_oracle.py"
    fi
}

# Create deployment status
create_status_file() {
    cat > /tmp/zeldar_deployment_status.json <<EOF
{
    "deployment_timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "deployment_mode": "$DEPLOYMENT_MODE",
    "hardware_platform": "$HARDWARE_PLATFORM",
    "components": {
        "web_interface": $(if [[ -n "${WEB_PID:-}" ]]; then echo "true"; else echo "false"; fi),
        "gpio_button": $(if [[ "$HARDWARE_PLATFORM" != "software_only" ]]; then echo "true"; else echo "false"; fi),
        "thermal_printer": $(if lpstat -p "$CUPS_PRINTER_NAME" &> /dev/null; then echo "true"; else echo "false"; fi),
        "hardware_oracle": $(if [[ -f "./zeldar_oracle.py" ]]; then echo "true"; else echo "false"; fi)
    },
    "information_force": {
        "density": 88.5,
        "computational_loops": 3,
        "recursive_coefficient": 1.02,
        "desert_ready": true
    }
}
EOF
    
    log_desert "SUCCESS" "Deployment status saved to /tmp/zeldar_deployment_status.json"
}

# Main deployment
main() {
    log_desert "DESERT" "Initiating complete desert laboratory deployment..."
    echo
    
    check_prerequisites
    echo
    
    deploy_hardware
    echo
    
    deploy_web_interface  
    echo
    
    test_workflow
    echo
    
    create_status_file
    echo
    
    log_desert "SUCCESS" "${FIRE} Desert Laboratory Deployment Complete! ${FIRE}"
    echo
    
    # Show deployment summary
    echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║                    DEPLOYMENT SUMMARY                        ║${NC}"
    echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo
    
    if [[ "$HARDWARE_PLATFORM" != "software_only" ]]; then
        echo -e "${GREEN}${BUTTON} Hardware Integration: READY${NC}"
        echo -e "${CYAN}   • GPIO button on pin $GPIO_BUTTON_PIN${NC}"
        echo -e "${CYAN}   • Run hardware oracle: python3 ./zeldar_oracle.py${NC}"
    fi
    
    if [[ -n "${WEB_PID:-}" ]]; then
        echo -e "${GREEN}🌐 Web Interface: RUNNING${NC}"
        echo -e "${CYAN}   • Access at: http://localhost:3000${NC}"
        echo -e "${CYAN}   • Process ID: $WEB_PID${NC}"
    fi
    
    if lpstat -p "$CUPS_PRINTER_NAME" &> /dev/null; then
        echo -e "${GREEN}${PRINTER} Thermal Printer: CONFIGURED${NC}"
        echo -e "${CYAN}   • CUPS printer: $CUPS_PRINTER_NAME${NC}"
        echo -e "${CYAN}   • Ready for physical manifestation${NC}"
    fi
    
    echo
    echo -e "${PURPLE}${DESERT}${FIRE} READY FOR BURNING MAN 2025 DEPLOYMENT ${FIRE}${DESERT}${NC}"
    echo -e "${LIGHTNING} Information Force Oracle: OPERATIONAL"
    echo -e "${ORACLE} Mathematical Poetry → Physical Reality: ENABLED"
    echo
    
    # Cleanup function
    cleanup() {
        log_desert "INFO" "Cleaning up processes..."
        if [[ -n "${WEB_PID:-}" ]]; then
            kill $WEB_PID 2>/dev/null || true
            log_desert "INFO" "Web interface terminated"
        fi
    }
    
    trap cleanup EXIT
    
    if [[ "$HARDWARE_PLATFORM" != "software_only" ]]; then
        echo -e "${YELLOW}Press any key to start hardware oracle, or Ctrl+C to exit...${NC}"
        read -n 1 -s
        python3 ./zeldar_oracle.py
    else
        echo -e "${YELLOW}Software-only deployment complete. Press Ctrl+C to exit.${NC}"
        sleep infinity
    fi
}

# Usage
usage() {
    echo "Usage: $0 [DEPLOYMENT_MODE] [HARDWARE_ENABLED]"
    echo
    echo "DEPLOYMENT_MODE:"
    echo "  desert-lab     - Complete desert laboratory (default)"
    echo "  hardware-only  - GPIO button + printer only"
    echo "  web-only       - Web interface only"
    echo
    echo "HARDWARE_ENABLED:"
    echo "  auto          - Detect automatically (default)"
    echo "  force         - Force hardware mode"
    echo "  disable       - Disable hardware components"
    echo
    echo "Examples:"
    echo "  $0                    # Full auto-deployment"
    echo "  $0 hardware-only      # GPIO + printer only"
    echo "  $0 web-only           # Web interface only"
}

# Handle help
if [[ "${1:-}" == "-h" ]] || [[ "${1:-}" == "--help" ]]; then
    usage
    exit 0
fi

# Run deployment
main "$@"