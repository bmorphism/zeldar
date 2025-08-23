# Zeldar - The Interactive Fortune-Teller

A bartholomew.wasm-powered mystical experience combining interactive fortune-telling with a comprehensive archive of historical automaton engineering.

## 🔮 About Zeldar

Zeldar channels the wisdom of mechanical oracles through modern WebAssembly technology, offering:

- **Interactive Fortune-Telling**: Click-activated mystical revelations
- **Historical Automaton Archive**: 150+ years of fortune-telling machine evolution
- **Authentic Mechanisms**: Fortunes generated using historical engineering principles
- **Responsive Design**: Mystical experience across all devices

## 🛠️ Technical Architecture

Built with **bartholomew.wasm** - a WebAssembly micro-CMS by Fermyon:

- **Framework**: Spin WebAssembly runtime
- **Content**: Markdown with TOML frontmatter
- **Templates**: Handlebars (.hbs) with mystical theming
- **Scripts**: Rhai for dynamic fortune generation
- **Styling**: Embedded CSS with atmospheric effects

## 📁 Project Structure

```
zeldar-fortune/
├── spin.toml              # Spin framework configuration
├── config/
│   └── site.toml          # Site-wide settings
├── content/
│   ├── index.md          # Main Zeldar page
│   └── history/          # Historical automaton archive
│       ├── index.md      # Timeline overview
│       ├── early-period.md     # 1867-1900 Mechanical Era
│       ├── electromechanical.md # 1900-1950 Electrical Era
│       └── animatronics.md     # 1950s+ Animatronic Era
├── templates/
│   ├── main.hbs          # Main page template
│   └── history.hbs       # History section template
├── partials/
│   └── history_timeline.hbs    # Interactive timeline component
├── scripts/
│   └── fortune_generator.rhai  # Fortune generation logic
├── shortcodes/
│   └── fortune_card.rhai       # Fortune card component
└── static/
    ├── css/              # Additional stylesheets
    └── images/           # Historical imagery
```

## 🚀 Deployment

### Prerequisites
- [Spin CLI](https://spin.fermyon.dev/quickstart/) installed
- [Fermyon Cloud](https://cloud.fermyon.com/) account (optional)

### Local Development
```bash
# Clone and navigate to project
cd zeldar-fortune

# Run locally
spin up

# Visit http://localhost:3000
```

### Cloud Deployment
```bash
# Deploy to Fermyon Cloud
spin deploy

# Or deploy to custom Spin-compatible host
spin up --listen 0.0.0.0:8080
```

## 🎨 Features

### Interactive Fortune-Telling
- **Mystical Atmosphere**: Animated gears, ethereal mist effects
- **Historical Accuracy**: Fortunes inspired by actual automaton mechanisms
- **Dynamic Generation**: 20+ unique fortunes with mechanism descriptions
- **Authentic Experience**: Coin-slot simulation and mechanical operation effects

### Historical Archive
- **Three Eras**: Mechanical (1867-1900), Electromechanical (1900-1950), Animatronic (1950s+)
- **Technical Details**: Authentic engineering specifications and innovations
- **Visual Timeline**: Interactive era navigation with animated markers
- **Manufacturer Profiles**: Genco, Mills, Mutoscope, Exhibit Supply, and more

## 📚 Historical Research

Content based on comprehensive research covering:

- **1867**: J. Parkes' first mechanical fortune-telling patent
- **1891**: Roover Brothers' political automatons (Donkey Wonder, Elephant Wonder)
- **1906**: Mills Novelty Company's electrical innovations
- **1920s**: Mutoscope's sophisticated "Grandmother's Predictions"
- **1957**: Genco Gypsy Grandma - most advanced fortune-teller ever created

## 🔧 Technical Implementation

### Fortune Generation System
```rhai
// Historical mechanism simulation
let fortunes = [
    "The gears of fate turn in your favor...",
    "Like Genco's cam shafts, your patience will be rewarded..."
];

let mechanisms = [
    "coin-activated disk selection",
    "spring-driven clockwork timing",
    "solenoid electromagnetic activation"
];
```

### Responsive Design
- Mobile-first CSS with mystical theming
- Animated background elements (floating gears, ethereal mist)
- Interactive timeline with era-specific styling
- Touch-friendly fortune card interactions

## 🎭 Theming Philosophy

Zeldar combines **mechanical precision** with **mystical atmosphere**:

- **Color Palette**: Deep blues, mystical golds, brass tones
- **Typography**: Georgia serif for authenticity
- **Animation**: Subtle mechanical movements and mist effects
- **Interaction**: Coin-operated fortune dispensing simulation

## 📖 Content Management

All content uses TOML frontmatter for metadata:

```toml
title = "Welcome to Zeldar's Mystical Chamber"
description = "Interactive fortune-telling with historical authenticity"
template = "main"

[extra]
fortune_enabled = true
mystical_level = "high"
```

## 🔮 Fortune Mechanisms

Historically-inspired randomization systems:
- **Cam Shaft Programming**: Sequential fortune selection
- **Pneumatic Systems**: Breathing simulation effects  
- **Solenoid Activation**: Electromagnetic precision
- **Mechanical Memory**: Temporal fortune patterns

## 🌟 Future Enhancements

- **Voice Integration**: ElevenLabs mystical narration
- **Extended History**: Additional manufacturer profiles
- **Interactive Mechanics**: Clickable mechanism diagrams
- **Fortune Categories**: Love, career, wisdom, adventure

---

*Zeldar honors the mechanical artistry of historical fortune-telling automatons while delivering a modern mystical experience through WebAssembly technology.*

**Built with bartholomew.wasm • Powered by historical engineering wisdom • Channeled through mystical mechanisms**