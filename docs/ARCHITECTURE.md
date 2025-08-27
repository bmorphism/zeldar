# Zeldar Unified Consciousness System - Architecture

This document provides a comprehensive overview of the architecture for the Zeldar system, an interactive art installation for Burning Man. It is designed as a multi-process, multi-language system orchestrated by a central Python script and deployed as a robust `systemd` service on a Raspberry Pi.

## I. High-Level Architecture Diagram

```
                                     ┌─────────────────────────────────┐
                                     │    ZELDAR UNIFIED CONSCIOUSNESS │
                                     │             SYSTEM              │
                                     └─────────────────────────────────┘
                                                  │   ▲
                                                  │   │
                                                  ▼   │
     ┌──────────────────────────────────────────────────────────────────────────────────────┐
     │                                   SYSTEM ORCHESTRATION                               │
     ├──────────────────────────────────────────────────────────────────────────────────────┤
     │ ┌──────────────────┐   starts/manages   ┌───────────────────────────────────────────┐  │
     │ │ systemd service  │ ───────────────► │                  main.py                  │  │
     │ │zeldar-oracle.service│                  │ (Asyncio-based Orchestrator & Health Monitor) │  │
     │ └──────────────────┘                  └───────────────────────────────────────────┘  │
     └─────────────────────────────────────────────────▲────────────────────────────────────┘
                                                       │
                                  (Launches & Monitors Services)
                                                       │
           ┌───────────────────────────────────────────┼───────────────────────────────────────────┐
           │                                           │                                           │
           ▼                                           ▼                                           ▼
┌──────────────────────┐                   ┌───────────────────────────┐                ┌──────────────────────┐
│    HARDWARE SERVICE    │                   │       WEB SERVICES        │                │    AUDIO SERVICE     │
├──────────────────────┤                   ├───────────────────────────┤                ├──────────────────────┤
│ unified_consciousness│                   │   ┌─────────────────────┐ │                │    src/audio_system  │
│      _button.py      │                   │   │ consciousness-oracle│ │                │                      │
│                      │                   │   │ (Rust / Spin / WASM)│ │                │ • Plays voice prompts│
│ • Listens on GPIO 6  │                   │   │ └─ Port 3001        │ │                │   on interaction     │
│ • Generates "Haiku"  │                   │   └─────────────────────┘ │                │                      │
│ • Calculates "Phi"   │                   │   ┌─────────────────────┐ │                └──────────────────────┘
│ • Robust printing    │                   │   │    fortune-web      │ │
│                      │                   │   │ (Rust / Spin / WASM)│ │
└──────────────────────┘                   │   │ └─ Port 3000        │ │
           ▲                               │   └─────────────────────┘ │
           │                               └───────────────────────────┘
           │
┌──────────────────────┐
│    HARDWARE LAYER    │
├──────────────────────┤
│ ┌──────────────────┐ │
│ │   Raspberry Pi   │ │
│ └──────────────────┘ │
│ ┌──────────────────┐ │
│ │  Physical Button │ │
│ └──────────────────┘ │
│ ┌──────────────────┐ │
│ │ Y812BT Printer   │ │
│ └──────────────────┘ │
└──────────────────────┘
```

## II. Component Breakdown

### 1. System Orchestration
- **`zeldar-oracle.service`**: A `systemd` service file that ensures the main application starts on boot and restarts automatically on failure. This provides operational robustness for the installation.
- **`main.py`**: The central nervous system of the project. It's an `asyncio`-based Python script that:
    - Loads the system configuration from `config.json`.
    - Launches and manages the lifecycle of all other services (Hardware, Web, Audio).
    - Runs a continuous health monitor, periodically checking the status of each service and writing it to `runtime_status.json`.
    - Handles graceful shutdown on `SIGTERM` or `SIGINT`.

### 2. Services
- **Hardware Service (`unified_consciousness_button.py`)**:
    - This is the core logic for user interaction.
    - It listens for a button press on GPIO pin 6 using the `gpiozero` library.
    - Upon a press, it triggers the `generate_consciousness_haiku` function, which deterministically creates a haiku and "consciousness metrics" (Phi, entropy) based on the precise timestamp of the press.
    - It then uses a robust, multi-stage printing process to output the haiku to the thermal printer, with fallbacks from direct ESC/POS commands to CUPS printing to console simulation.
- **Web Services (`consciousness-oracle/` & `fortune-web/`)**:
    - Two independent web applications written in **Rust** and compiled to **WebAssembly (WASM)**.
    - They are served using the **Fermyon Spin** server.
    - `main.py` launches these as separate subprocesses.
    - `consciousness-oracle` (Port 3001): Provides a real-time visualization of the system's "consciousness" state.
    - `fortune-web` (Port 3000): An interactive, mystical web interface for users.
- **Audio Service (`src/audio_system.py`)**:
    - Responsible for playing pre-recorded voice prompts and sounds to enhance the user experience.
    - It is triggered by events within the hardware service.

### 3. Hardware Layer
- **Raspberry Pi**: The computing device that runs the entire system.
- **Physical Button**: A simple button connected to GPIO pin 6, which acts as the primary user input.
- **Y812BT Thermal Printer**: A USB-connected printer that produces the physical "fortune" or haiku for the user.

## III. Data and Execution Flow (On Button Press)

1.  A user presses the physical button.
2.  The `gpiozero` library in `unified_consciousness_button.py` detects the falling edge on GPIO pin 6.
3.  The `on_button_press` method is invoked.
4.  A high-precision timestamp is recorded.
5.  The timestamp is used as a seed to deterministically generate a haiku, an "element", an entropy value, and a "consciousness Phi" value.
6.  The generated content is formatted for printing.
7.  The `unified_print_methods` function is called, which attempts to print the content via (in order): direct ESC/POS commands, the CUPS `lp` command, or a fallback script.
8.  The `main.py` health monitor observes the status change and updates `runtime_status.json`.
9.  The audio service may play a sound to signify a successful "manifestation".
10. The web services can be viewed by users on the network to see the system's state change in real-time.

## IV. Technology Stack

- **Orchestration**: Python 3.11 (`asyncio`)
- **Hardware Interaction**: Python (`gpiozero`)
- **Web Services**: Rust, WebAssembly (WASM), Fermyon Spin, HTML/CSS/JS
- **Configuration**: JSON
- **Deployment**: `systemd` on Raspberry Pi OS
- **Code Style/Philosophy**: The `.topos/AGENTS.md` file indicates an aspirational use of advanced concepts like OCaml and Applied Category Theory, though the primary implementation appears to be Python and Rust.
