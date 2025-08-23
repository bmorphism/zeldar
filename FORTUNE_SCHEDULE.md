# Burning Man Fortune Schedule 2025

## Fortune Deployment Timeline

**Event Dates**: August 24-30, 2025 (+ Special Day August 31)

### Daily Fortune Schedule:

| Date | Day | Fortune Type | Status |
|------|-----|-------------|---------|
| **August 24** | Sunday | Opening Day Fortunes | 📅 **STARTING** |
| **August 25** | Monday | Monday Sequence | 📅 Scheduled |
| **August 26** | Tuesday | Tuesday Sequence | 📅 Scheduled |
| **August 27** | Wednesday | Wednesday Sequence | 📅 Scheduled |
| **August 28** | Thursday | Thursday Sequence | 📅 Scheduled |
| **August 29** | Friday | Friday Sequence | 📅 Scheduled |
| **August 30** | Saturday | Saturday Closing | 📅 Final Day |
| **August 31** | Sunday | **SPECIAL FORTUNES** | ⭐ **To be uploaded later** |

## Technical Implementation

### Current System Configuration:
```bash
# Default fortune (currently deployed)
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
```

### Required Modifications for Schedule:

#### 1. Date-Based Fortune Selection System
```python
# Add to src/controlled_button.py
import datetime

def get_daily_fortune():
    """Select fortune based on current date during Burning Man 2025"""
    today = datetime.date.today()
    
    fortune_map = {
        # Burning Man 2025 Schedule
        datetime.date(2025, 8, 24): "sunday_opening_fortunes",
        datetime.date(2025, 8, 25): "monday_sequence", 
        datetime.date(2025, 8, 26): "tuesday_sequence",
        datetime.date(2025, 8, 27): "wednesday_sequence",
        datetime.date(2025, 8, 28): "thursday_sequence",
        datetime.date(2025, 8, 29): "friday_sequence",
        datetime.date(2025, 8, 30): "saturday_closing",
        datetime.date(2025, 8, 31): "special_fortunes"  # Upload later
    }
    
    return fortune_map.get(today, "default_fortune")
```

#### 2. Fortune Content Database
```bash
# Directory structure for daily fortunes
fortunes/
├── sunday_opening_fortunes.txt
├── monday_sequence.txt
├── tuesday_sequence.txt
├── wednesday_sequence.txt
├── thursday_sequence.txt
├── friday_sequence.txt
├── saturday_closing.txt
└── special_fortunes.txt  # To be uploaded August 31
```

#### 3. Dynamic Print Script Modification
```bash
# Update scripts/print-now.sh to use daily fortune selection
FORTUNE_DATE=$(date +"%Y-%m-%d")
FORTUNE_FILE="/home/zeldar/burningman/fortunes/${FORTUNE_DATE}.txt"

if [ -f "$FORTUNE_FILE" ]; then
    FORTUNE_CONTENT=$(cat "$FORTUNE_FILE")
else
    # Fallback to default
    FORTUNE_CONTENT="[default content]"
fi
```

## Deployment Requirements

### Pre-Event Setup (Before August 24):
1. **Create fortune content files** for each day
2. **Test date-based selection system**
3. **Verify timezone configuration** (Pacific Time)
4. **Upload initial fortune set** (August 24-30)

### During Event:
- **Automated daily rotation** based on system date
- **Monitor fortune selection accuracy**
- **Remote fortune updates** via Starlink if needed

### Special Day Preparation (August 31):
- **Upload special_fortunes.txt** via remote access
- **Test special fortune deployment**
- **Verify system switches correctly at midnight**

## Current Action Items

### Immediate (Today):
1. **Create fortune directory structure**
2. **Implement date-based selection logic** 
3. **Test with mock dates** to verify rotation

### Before August 24:
1. **Deploy fortune content files**
2. **Verify system timezone alignment**
3. **Test remote update capability via Starlink**

### August 31 Preparation:
1. **Prepare special fortune upload**
2. **Schedule remote deployment**
3. **Monitor system transition**

## Fortune Content Guidelines

### Format Requirements:
- **28×15 character limits** (paper optimized)
- **ESC/POS compatible** text encoding
- **Semantic coherence** with art installation theme
- **Daily thematic variation** while maintaining core philosophy

### Content Themes by Day:
- **Sunday (Opening)**: Welcome, intention-setting
- **Monday-Friday**: Daily progression through concepts
- **Saturday (Closing)**: Integration, completion
- **Sunday (Special)**: ⭐ **TBD - Special content upload**

---

**Status**: Ready to implement daily fortune rotation system for Burning Man 2025 deployment.

**Next Steps**: Create fortune content files and implement date-based selection logic.