# Project Structure Documentation

## Clean Directory Organization

```
burningman/                           # Root project directory
├── README.md                         # Main project overview
├── pyproject.toml                   # uv Python project configuration
├── uv.lock                          # Dependency lock file
├── .venv/                           # Virtual environment
├── .python-version                  # Python version specification
│
├── docs/                            # 📚 Documentation
│   ├── PROJECT_STRUCTURE.md         # This file - project organization
│   ├── COMPLETE_DOCUMENTATION.md    # Comprehensive system manual
│   ├── SYSTEM_OVERVIEW.md           # Quick reference guide
│   └── PRINTER_GUIDE.md            # Hardware setup and troubleshooting
│
├── src/                             # 🧠 Core Application Source
│   ├── controlled_button.py         # Main GPIO controller (ACTIVE)
│   ├── precision_print.py          # Sticky formatting system
│   ├── gemini_architectures.py     # AI information-dynamics integration
│   └── system_diagram.py           # ASCII architecture visualization
│
├── scripts/                         # 🔧 Utility Scripts
│   └── print-now.sh                # Direct thermal printing script
│
├── tests/                           # 🧪 Test Files (future)
│   └── (test files will go here)
│
├── archive/                         # 📦 Deprecated & Development Files
│   ├── button-print.py             # Original GPIO handler (superseded)
│   ├── corrected_precision.py      # Development formatting tests
│   ├── gemini_validation.py        # AI integration testing
│   ├── sticky_calibration.py       # Label dimension calibration
│   ├── information-dynamics_query.txt      # AI conversation transcript
│   ├── formatted_fortunes.py       # Generated fortune variants
│   ├── safe_fortune_command.txt     # ESC/POS command testing
│   ├── main.py                     # uv auto-generated stub
│   └── test.wav                    # Audio test file
│
├── haiku.txt                        # Original fortune content
├── last_print.json                 # State persistence file
└── runtime_status.json             # System activity tracking
```

## File Categories

### 🎯 **Active Production Files**
- `src/controlled_button.py` - **Primary system controller**
- `scripts/print-now.sh` - **Print execution script**
- `src/precision_print.py` - **Fortune formatting engine**
- `pyproject.toml` + `uv.lock` - **Environment management**

### 📚 **Documentation Hierarchy**
1. **`README.md`** - Project overview and quick start
2. **`docs/COMPLETE_DOCUMENTATION.md`** - Full system manual
3. **`docs/SYSTEM_OVERVIEW.md`** - Concise reference
4. **`docs/PRINTER_GUIDE.md`** - Hardware specifics
5. **`docs/PROJECT_STRUCTURE.md`** - This organization guide

### 🔄 **State & Configuration**
- `last_print.json` - Print cooldown persistence
- `runtime_status.json` - System activity logging  
- `haiku.txt` - Fortune content data
- `.python-version` - Python version lock

### 📦 **Archive Strategy**
**Deprecated but preserved:**
- `button-print.py` - Original implementation (replaced by controlled version)
- Development tools and calibration scripts
- Temporary files and AI conversation transcripts
- Test files and experimental code

## Path References

### Updated Import/Execution Paths
```bash
# Main system startup
sudo uv run python src/controlled_button.py

# Manual printing  
./scripts/print-now.sh

# System diagnostics
uv run python src/system_diagram.py
```

### Internal Script Paths
- `controlled_button.py` → calls `./scripts/print-now.sh`
- All documentation cross-references updated
- Archive files maintain original functionality if needed

## Benefits of Clean Structure

### 🎯 **Operational Clarity**
- **Single source of truth**: `src/controlled_button.py` is the main controller
- **Clear execution paths**: Scripts in `scripts/`, source in `src/`
- **Documentation hierarchy**: From quick start to comprehensive manual

### 🔧 **Development Workflow**
- **Easy testing**: All test files organized in `tests/`
- **Safe experimentation**: Archive preserves working versions
- **Clear dependencies**: `pyproject.toml` defines exact requirements

### 🏜️ **Playa Deployment**
- **Minimal footprint**: Only active files needed for operation
- **Clear backup strategy**: Archive contains all developmental iterations
- **Easy troubleshooting**: Logical organization aids field diagnosis

## Migration Notes

### Path Updates Required
- ✅ `controlled_button.py` updated to use `./scripts/print-now.sh`
- ✅ Documentation updated with new structure
- ✅ All deprecated files safely archived

### Backwards Compatibility
- Archive files can be restored if needed
- Original functionality preserved in `archive/button-print.py`
- All development tools remain accessible

---

**Clean structure achieved** - The information-dynamics mirror now has **geometric organizational recursion** matching its operational recursion. 🌀📁✨