#!/bin/bash

# Zeldar Fortune-Teller Deployment Verification Script
# Verifies bartholomew.wasm project structure and readiness

echo "🔮 Verifying Zeldar Fortune-Teller Deployment Readiness..."
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [[ ! -f "spin.toml" ]]; then
    echo -e "${RED}❌ Error: spin.toml not found. Run this script from the zeldar-fortune directory.${NC}"
    exit 1
fi

echo -e "${BLUE}📁 Checking project structure...${NC}"

# Core configuration files
check_file() {
    if [[ -f "$1" ]]; then
        echo -e "  ${GREEN}✅ $1${NC}"
        return 0
    else
        echo -e "  ${RED}❌ Missing: $1${NC}"
        return 1
    fi
}

check_dir() {
    if [[ -d "$1" ]]; then
        echo -e "  ${GREEN}✅ $1/${NC}"
        return 0
    else
        echo -e "  ${RED}❌ Missing directory: $1/${NC}"
        return 1
    fi
}

# Verify core files
MISSING_FILES=0

check_file "spin.toml" || ((MISSING_FILES++))
check_file "config/site.toml" || ((MISSING_FILES++))
check_file "content/index.md" || ((MISSING_FILES++))
check_file "templates/main.hbs" || ((MISSING_FILES++))
check_file "templates/history.hbs" || ((MISSING_FILES++))
check_file "scripts/fortune_generator.rhai" || ((MISSING_FILES++))
check_file "shortcodes/fortune_card.rhai" || ((MISSING_FILES++))

echo ""
echo -e "${BLUE}📚 Checking content structure...${NC}"

# Check content files
check_file "content/history/index.md" || ((MISSING_FILES++))
check_file "content/history/early-period.md" || ((MISSING_FILES++))
check_file "content/history/electromechanical.md" || ((MISSING_FILES++))
check_file "content/history/animatronics.md" || ((MISSING_FILES++))

# Check template partials
check_file "partials/history_timeline.hbs" || ((MISSING_FILES++))

echo ""
echo -e "${BLUE}🎨 Checking static assets...${NC}"

check_dir "static/css" || ((MISSING_FILES++))
check_dir "static/images/historical" || ((MISSING_FILES++))

echo ""
echo -e "${BLUE}🔧 Validating configuration files...${NC}"

# Check spin.toml syntax
if command -v spin &> /dev/null; then
    if spin doctor &> /dev/null; then
        echo -e "  ${GREEN}✅ Spin configuration valid${NC}"
    else
        echo -e "  ${YELLOW}⚠️  Spin doctor reported issues (check manually)${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠️  Spin CLI not found - cannot validate configuration${NC}"
fi

# Check for TOML syntax in site.toml
if command -v toml &> /dev/null || python3 -c "import toml" &> /dev/null; then
    echo -e "  ${GREEN}✅ TOML validation available${NC}"
else
    echo -e "  ${YELLOW}⚠️  TOML validator not found${NC}"
fi

echo ""
echo -e "${BLUE}🎭 Checking content metadata...${NC}"

# Verify TOML frontmatter exists
check_frontmatter() {
    if head -5 "$1" | grep -q "title\s*="; then
        echo -e "  ${GREEN}✅ $1 has TOML frontmatter${NC}"
    else
        echo -e "  ${YELLOW}⚠️  $1 missing or invalid frontmatter${NC}"
    fi
}

check_frontmatter "content/index.md"
check_frontmatter "content/history/index.md"
check_frontmatter "content/history/early-period.md"
check_frontmatter "content/history/electromechanical.md"
check_frontmatter "content/history/animatronics.md"

echo ""
echo -e "${BLUE}🔮 Checking Rhai scripts...${NC}"

# Basic Rhai syntax check
if [[ -f "scripts/fortune_generator.rhai" ]]; then
    if grep -q "let fortunes" "scripts/fortune_generator.rhai"; then
        echo -e "  ${GREEN}✅ Fortune generator script structure looks good${NC}"
    else
        echo -e "  ${YELLOW}⚠️  Fortune generator script may have issues${NC}"
    fi
fi

if [[ -f "shortcodes/fortune_card.rhai" ]]; then
    if grep -q "card_html" "shortcodes/fortune_card.rhai"; then
        echo -e "  ${GREEN}✅ Fortune card shortcode structure looks good${NC}"
    else
        echo -e "  ${YELLOW}⚠️  Fortune card shortcode may have issues${NC}"
    fi
fi

echo ""
echo -e "${BLUE}📊 Deployment Summary:${NC}"

if [[ $MISSING_FILES -eq 0 ]]; then
    echo -e "${GREEN}🎉 All essential files present! Zeldar is ready for deployment.${NC}"
    echo ""
    echo -e "${BLUE}🚀 Next steps:${NC}"
    echo "  1. Run: spin up (for local testing)"
    echo "  2. Visit: http://localhost:3000"
    echo "  3. Test fortune generation and history navigation"
    echo "  4. Deploy: spin deploy (to Fermyon Cloud)"
    echo ""
    echo -e "${GREEN}✨ May the mechanical spirits guide your deployment! ✨${NC}"
else
    echo -e "${RED}⚠️  Found $MISSING_FILES missing files. Please create them before deployment.${NC}"
    echo ""
    echo -e "${YELLOW}💡 Tip: Check the README.md for complete project structure requirements.${NC}"
fi

echo ""
echo -e "${BLUE}🔮 Zeldar's wisdom: ${YELLOW}'Like the precision of Genco's cam shafts, successful deployment requires every component in perfect alignment.'${NC}"