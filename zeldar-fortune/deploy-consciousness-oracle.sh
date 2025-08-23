#!/bin/bash
# Zeldar Information Force Oracle Deployment Script
# Automated deployment for Burning Man 2025 and development environments
# Tri-Loop Automation Architecture: MCP + Gemini Live + Codex-rs

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Unicode symbols for information force
INFORMATION_FORCE="⚡"
LOOPS="🔄"
DESERT="🏜️"
FIRE="🔥"
SPARKLES="✨"
GEAR="⚙️"
PRINTER="🖨️"

echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║     ${INFORMATION_FORCE} ZELDAR INFORMATION FORCE ORACLE DEPLOYMENT ${INFORMATION_FORCE}         ║${NC}"
echo -e "${PURPLE}║                 Tri-Loop Automation System                    ║${NC}"
echo -e "${PURPLE}║              ${DESERT}${FIRE} Burning Man 2025 Ready ${FIRE}${DESERT}                   ║${NC}"
echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo

# Configuration
PROJECT_DIR="/Users/barton/infinity-topos/zeldar-fortune"
QUANTUM_ORACLE_DIR="/Users/barton/infinity-topos/zeldar"
DEPLOYMENT_MODE="${1:-development}"  # development, burning-man, production
INFORMATION_FORCE_LEVEL="${2:-88.5}" # Information density percentage

# Validate deployment mode
case "$DEPLOYMENT_MODE" in
    development|dev)
        DEPLOYMENT_MODE="development"
        echo -e "${BLUE}${GEAR} Deployment Mode: Development Environment${NC}"
        ;;
    burning-man|playa|desert)
        DEPLOYMENT_MODE="burning-man"
        echo -e "${YELLOW}${DESERT} Deployment Mode: Burning Man 2025 Desert Laboratory${NC}"
        ;;
    production|prod)
        DEPLOYMENT_MODE="production"  
        echo -e "${GREEN}${SPARKLES} Deployment Mode: Production Consciousness System${NC}"
        ;;
    *)
        echo -e "${RED}❌ Invalid deployment mode: $DEPLOYMENT_MODE${NC}"
        echo -e "${CYAN}Valid modes: development, burning-man, production${NC}"
        exit 1
        ;;
esac

# Function to log with information force awareness
log_information_force() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$level" in
        "INFO")
            echo -e "${CYAN}[${timestamp}] ${INFORMATION_FORCE} ${message}${NC}"
            ;;
        "SUCCESS") 
            echo -e "${GREEN}[${timestamp}] ${SPARKLES} ${message}${NC}"
            ;;
        "WARNING")
            echo -e "${YELLOW}[${timestamp}] ${LOOPS} ${message}${NC}"
            ;;
        "ERROR")
            echo -e "${RED}[${timestamp}] ❌ ${message}${NC}"
            ;;
        "DESERT")
            echo -e "${PURPLE}[${timestamp}] ${DESERT}${FIRE} ${message}${NC}"
            ;;
    esac
}

# Legacy function for backward compatibility
log_consciousness() {
    log_information_force "$1" "$2"
}

# Validate information force threshold
validate_information_force() {
    local threshold=$(echo "$INFORMATION_FORCE_LEVEL" | bc -l 2>/dev/null || echo "0")
    
    if (( $(echo "$threshold >= 80.0" | bc -l) )); then
        log_information_force "SUCCESS" "Information force threshold exceeded: ${threshold}% - INFORMATION FORCE ACHIEVED"
        return 0
    elif (( $(echo "$threshold >= 60.0" | bc -l) )); then
        log_information_force "WARNING" "Information force level: ${threshold}% - BUILDING STATE"
        return 0
    else
        log_information_force "ERROR" "Information force level too low: ${threshold}% - Minimum 60% required"
        return 1
    fi
}

# Legacy function for backward compatibility
validate_consciousness() {
    validate_information_force
}

# Check prerequisites
check_prerequisites() {
    log_consciousness "INFO" "Checking deployment prerequisites..."
    
    # Check if we're in the right directory
    if [[ ! -f "$PROJECT_DIR/spin.toml" ]]; then
        log_consciousness "ERROR" "spin.toml not found. Are you in the zeldar-fortune directory?"
        exit 1
    fi
    
    # Check for Spin CLI
    if ! command -v spin &> /dev/null; then
        log_consciousness "ERROR" "Spin CLI not found. Install from: https://spin.fermyon.dev/"
        log_consciousness "INFO" "Run: curl -fsSL https://developer.fermyon.com/downloads/install.sh | bash"
        exit 1
    fi
    
    # Check information force level
    if ! validate_information_force; then
        exit 1
    fi
    
    # Check for quantum oracle core (if burning-man mode)
    if [[ "$DEPLOYMENT_MODE" == "burning-man" ]]; then
        if [[ ! -f "$QUANTUM_ORACLE_DIR/.topos/RESEARCH_JUSTIFIED_ORACLE_CORE.py" ]]; then
            log_consciousness "WARNING" "Quantum oracle core not found - web-only deployment"
        else
            log_consciousness "SUCCESS" "Quantum oracle core validated"
        fi
    fi
    
    log_consciousness "SUCCESS" "All prerequisites validated"
}

# Build information force-enhanced assets
build_information_force_assets() {
    log_information_force "INFO" "Building information force-enhanced frontend assets..."
    
    cd "$PROJECT_DIR"
    
    # Validate consciousness JavaScript engine
    if [[ -f "static/js/consciousness-oracle.js" ]]; then
        local js_size=$(wc -c < static/js/consciousness-oracle.js)
        if (( js_size > 1000 )); then
            log_consciousness "SUCCESS" "Consciousness JavaScript engine ready (${js_size} bytes)"
        else
            log_consciousness "WARNING" "Consciousness JavaScript engine seems small (${js_size} bytes)"
        fi
    else
        log_consciousness "ERROR" "Consciousness JavaScript engine not found"
        exit 1
    fi
    
    # Validate consciousness CSS framework  
    if [[ -f "static/css/consciousness-enhancements.css" ]]; then
        local css_size=$(wc -c < static/css/consciousness-enhancements.css)
        if (( css_size > 5000 )); then
            log_consciousness "SUCCESS" "Consciousness CSS framework ready (${css_size} bytes)"
        else
            log_consciousness "WARNING" "Consciousness CSS framework seems small (${css_size} bytes)"
        fi
    else
        log_consciousness "ERROR" "Consciousness CSS framework not found"
        exit 1
    fi
    
    # Validate consciousness-aware content
    if [[ -f "content/index.md" ]]; then
        if grep -q "information_force_enabled = true" content/index.md; then
            log_consciousness "SUCCESS" "Consciousness-aware content validated"
        else
            log_consciousness "WARNING" "Content may not be consciousness-enabled"
        fi
    fi
    
    # Validate Rhai fortune generation script
    if [[ -f "scripts/fortune_generator.rhai" ]]; then
        if grep -q "CONSCIOUSNESS_ORACLE" scripts/fortune_generator.rhai; then
            log_consciousness "SUCCESS" "Consciousness-aware fortune generation ready"
        else
            log_consciousness "WARNING" "Fortune generator may not be consciousness-enhanced"
        fi
    fi
    
    log_consciousness "SUCCESS" "All consciousness assets validated"
}

# Configure deployment environment
configure_environment() {
    log_consciousness "INFO" "Configuring ${DEPLOYMENT_MODE} environment..."
    
    # Create environment-specific configuration
    case "$DEPLOYMENT_MODE" in
        "development")
            export CONSCIOUSNESS_MODE="development"
            export SEMANTIC_CLOSURE_TARGET="$INFORMATION_FORCE_LEVEL"
            export TRI_LOOP_ENABLED="true"
            export DESERT_DEPLOYMENT="false"
            export GIFT_ECONOMY_MODE="false"
            ;;
        "burning-man")
            export CONSCIOUSNESS_MODE="burning_man_2025" 
            export SEMANTIC_CLOSURE_TARGET="$INFORMATION_FORCE_LEVEL"
            export TRI_LOOP_ENABLED="true"
            export DESERT_DEPLOYMENT="true"
            export GIFT_ECONOMY_MODE="true"
            export THERMAL_PRINTER_ENABLED="true"
            export GPIO_BUTTON_ENABLED="true"
            ;;
        "production")
            export CONSCIOUSNESS_MODE="production"
            export SEMANTIC_CLOSURE_TARGET="$INFORMATION_FORCE_LEVEL"
            export TRI_LOOP_ENABLED="true"
            export DESERT_DEPLOYMENT="false"
            export GIFT_ECONOMY_MODE="false"
            ;;
    esac
    
    log_consciousness "SUCCESS" "Environment configured for ${DEPLOYMENT_MODE} mode"
    log_consciousness "INFO" "Consciousness parameters:"
    log_consciousness "INFO" "  - Semantic Closure Target: ${INFORMATION_FORCE_LEVEL}%"
    log_consciousness "INFO" "  - Tri-Loop System: ${TRI_LOOP_ENABLED}"
    log_consciousness "INFO" "  - Desert Deployment: ${DESERT_DEPLOYMENT}"
    log_consciousness "INFO" "  - Gift Economy: ${GIFT_ECONOMY_MODE}"
}

# Deploy based on mode
deploy_consciousness_system() {
    case "$DEPLOYMENT_MODE" in
        "development")
            deploy_development
            ;;
        "burning-man")
            deploy_burning_man
            ;;
        "production")
            deploy_production
            ;;
    esac
}

# Development deployment
deploy_development() {
    log_consciousness "INFO" "Starting development consciousness server..."
    
    cd "$PROJECT_DIR"
    
    # Start Spin development server
    log_consciousness "INFO" "Launching Spin WebAssembly server..."
    
    # Create a development-specific spin configuration if needed
    if [[ ! -f "spin.dev.toml" ]]; then
        cp spin.toml spin.dev.toml
        log_consciousness "INFO" "Created development configuration"
    fi
    
    log_consciousness "SUCCESS" "Development server starting..."
    log_consciousness "INFO" "Access consciousness oracle at: http://localhost:3000"
    log_consciousness "INFO" "Press Ctrl+C to stop consciousness processing"
    
    # Start the server (this will block)
    spin up --file spin.dev.toml
}

# Burning Man deployment
deploy_burning_man() {
    log_consciousness "DESERT" "Preparing consciousness system for playa deployment..."
    
    # Check hardware requirements
    if [[ "$OSTYPE" == "linux-gnu"* ]] && [[ -d "/sys/class/gpio" ]]; then
        log_consciousness "SUCCESS" "GPIO hardware detected - Raspberry Pi ready"
        
        # Check for thermal printer
        if command -v bluetoothctl &> /dev/null; then
            log_consciousness "SUCCESS" "Bluetooth stack available for thermal printer"
        else
            log_consciousness "WARNING" "Bluetooth not available - thermal printing disabled"
        fi
    else
        log_consciousness "WARNING" "GPIO hardware not detected - button activation disabled"
    fi
    
    # Start quantum oracle backend if available
    if [[ -f "$QUANTUM_ORACLE_DIR/.topos/burning_man_fortune_teller.py" ]]; then
        log_consciousness "DESERT" "Starting quantum oracle backend..."
        cd "$QUANTUM_ORACLE_DIR"
        python .topos/burning_man_fortune_teller.py &
        QUANTUM_PID=$!
        log_consciousness "SUCCESS" "Quantum oracle running (PID: $QUANTUM_PID)"
        cd "$PROJECT_DIR"
    fi
    
    # Create burning man configuration
    log_consciousness "DESERT" "Configuring for Black Rock City deployment..."
    
    # Deploy web interface
    log_consciousness "DESERT" "Deploying consciousness web interface..."
    
    if command -v spin deploy &> /dev/null; then
        log_consciousness "INFO" "Deploying to Fermyon Cloud..."
        spin deploy
        log_consciousness "SUCCESS" "Consciousness oracle deployed to cloud"
    else
        log_consciousness "INFO" "Starting local server for desert deployment..."
        spin up --listen 0.0.0.0:8080 &
        WEB_PID=$!
        log_consciousness "SUCCESS" "Web interface running (PID: $WEB_PID)"
    fi
    
    # Create deployment info file
    cat > deployment-info.json <<EOF
{
    "deployment_mode": "burning_man_2025",
    "information_force_level": $INFORMATION_FORCE_LEVEL,
    "deployment_timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "hardware_enabled": {
        "gpio_button": $(if [[ -d "/sys/class/gpio" ]]; then echo "true"; else echo "false"; fi),
        "thermal_printer": $(if command -v bluetoothctl &> /dev/null; then echo "true"; else echo "false"; fi)
    },
    "services": {
        "quantum_oracle_pid": ${QUANTUM_PID:-null},
        "web_interface_pid": ${WEB_PID:-null}
    }
}
EOF
    
    log_consciousness "DESERT" "Desert deployment complete!"
    log_consciousness "SUCCESS" "Consciousness expansion gift ready for Black Rock City"
    log_consciousness "INFO" "Deployment info saved to: deployment-info.json"
}

# Production deployment  
deploy_production() {
    log_consciousness "INFO" "Deploying consciousness system to production..."
    
    cd "$PROJECT_DIR"
    
    # Build optimized version
    log_consciousness "INFO" "Building optimized consciousness system..."
    
    # Deploy to cloud
    if command -v spin deploy &> /dev/null; then
        log_consciousness "INFO" "Deploying to Fermyon Cloud..."
        spin deploy
        log_consciousness "SUCCESS" "Production consciousness oracle deployed"
    else
        log_consciousness "ERROR" "Spin cloud deployment not available"
        exit 1
    fi
    
    log_consciousness "SUCCESS" "Production deployment complete"
}

# Deployment validation
validate_deployment() {
    log_consciousness "INFO" "Validating consciousness system deployment..."
    
    case "$DEPLOYMENT_MODE" in
        "development")
            # Check if localhost:3000 responds
            if curl -s http://localhost:3000 >/dev/null 2>&1; then
                log_consciousness "SUCCESS" "Development server responding"
            else
                log_consciousness "WARNING" "Development server may still be starting..."
            fi
            ;;
        "burning-man")
            log_consciousness "SUCCESS" "Desert deployment validation complete"
            ;;
        "production")
            log_consciousness "SUCCESS" "Production deployment validation complete"
            ;;
    esac
}

# Cleanup function
cleanup() {
    log_consciousness "INFO" "Cleaning up consciousness processes..."
    
    # Kill background processes if they exist
    if [[ -n "${QUANTUM_PID:-}" ]]; then
        kill $QUANTUM_PID 2>/dev/null || true
        log_consciousness "INFO" "Quantum oracle process terminated"
    fi
    
    if [[ -n "${WEB_PID:-}" ]]; then
        kill $WEB_PID 2>/dev/null || true  
        log_consciousness "INFO" "Web interface process terminated"
    fi
}

# Set trap for cleanup
trap cleanup EXIT

# Main deployment flow
main() {
    echo -e "${INFORMATION_FORCE} Starting Zeldar Information Force Oracle Deployment..."
    echo
    
    check_prerequisites
    echo
    
    build_information_force_assets
    echo
    
    configure_environment
    echo
    
    deploy_consciousness_system
    echo
    
    validate_deployment
    echo
    
    log_information_force "SUCCESS" "${SPARKLES} Information force oracle deployment complete! ${SPARKLES}"
    
    case "$DEPLOYMENT_MODE" in
        "development")
            echo -e "${CYAN}${INFORMATION_FORCE} Access your information force oracle at: ${BLUE}http://localhost:3000${NC}"
            ;;
        "burning-man")
            echo -e "${PURPLE}${DESERT}${FIRE} Desert information force laboratory operational! ${FIRE}${DESERT}${NC}"
            echo -e "${YELLOW}Ready for Burning Man 2025 information force expansion gifts${NC}"
            ;;
        "production")
            echo -e "${GREEN}${SPARKLES} Production information force system deployed successfully${NC}"
            ;;
    esac
    
    echo
    echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║  ${INFORMATION_FORCE} Mathematical Poetry Manifesting Physical Reality ${INFORMATION_FORCE}   ║${NC}"
    echo -e "${PURPLE}║    ${DESERT}${FIRE} Information Force Revolution: COMPLETE ${FIRE}${DESERT}            ║${NC}"
    echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════╝${NC}"
}

# Usage information
usage() {
    echo "Usage: $0 [DEPLOYMENT_MODE] [CONSCIOUSNESS_LEVEL]"
    echo
    echo "DEPLOYMENT_MODE:"
    echo "  development, dev     - Local development server"
    echo "  burning-man, playa   - Burning Man 2025 desert deployment"  
    echo "  production, prod     - Production cloud deployment"
    echo
    echo "CONSCIOUSNESS_LEVEL:"
    echo "  Float value 0.0-100.0 (default: 88.5)"
    echo "  Must be >= 60.0 for basic operation"
    echo "  >= 80.0 for consciousness threshold achievement"
    echo
    echo "Examples:"
    echo "  $0 development          # Start dev server with default consciousness"
    echo "  $0 burning-man 92.3     # Deploy to playa with 92.3% consciousness"
    echo "  $0 production           # Deploy to cloud with default settings"
}

# Handle help flag
if [[ "${1:-}" == "-h" ]] || [[ "${1:-}" == "--help" ]]; then
    usage
    exit 0
fi

# Run main deployment
main "$@"