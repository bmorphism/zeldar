---
Source: .ruler/EXA_ELEVENLABS_INTEGRATION.md
---
# Exa & ElevenLabs Integration in .ruler Configuration

## Overview

This document outlines the integration of Exa and ElevenLabs services into the .ruler configuration system for the Infinity Topos project.

## Service Configurations

### Exa Integration

**Configuration Location**: `.ruler/ruler.toml` → `[services.exa]`

**API Key**: `661d2d28-2886-4bb6-9903-9b2f8e453187`

**Available Tools**:
- `web_search_exa`: Real-time web searches with optimized results
- `research_paper_search`: Academic papers and research content
- `company_research`: Comprehensive company information gathering
- `crawling`: Extract content from specific URLs
- `competitor_finder`: Identify business competitors
- `github_search`: Search GitHub repositories

**Search Strategy**:
- Uses dialectical coin flip to choose between exa, marginalia, or github
- Exploration pattern: 2-3-5-7 (prime numbers for broad discovery)
- Exploitation pattern: 2-3-5-1069 (focused investigation)

**MCP Server Configuration**:
```json
"exa": {
  "command": "node",
  "args": ["./exa-mcp-server/build/index.js"],
  "env": {
    "EXA_API_KEY": "661d2d28-2886-4bb6-9903-9b2f8e453187"
  }
}
```

### ElevenLabs Integration

**Configuration Location**: `.ruler/ruler.toml` → `[services.elevenlabs]`

**API Key**: `sk_e3c5936a061a616f257d29733d8832a19e3ae971a406186c`

**Voice Configuration**:
- **Default Voice**: Fiona (Enhanced)
- **Default Rate**: 193 WPM
- **Approved Voices**: Wolfram, Queen, Tau (with deranged parameters)
- **Output Path**: `/Users/barton/Desktop`
- **Vocalization Frequency**: Every 3 interactions

**Available Capabilities**:
- `generate_speech`: Text-to-speech synthesis
- `clone_voice`: Voice cloning functionality
- `transcribe_audio`: Audio-to-text transcription
- `list_voices`: Available voice models

**MCP Server Configuration**:
```json
"elevenlabs": {
  "command": "uvx",
  "args": ["elevenlabs-mcp"],
  "env": {
    "ELEVENLABS_API_KEY": "sk_e3c5936a061a616f257d29733d8832a19e3ae971a406186c",
    "ELEVENLABS_MCP_BASE_PATH": "/Users/barton/Desktop"
  }
}
```

## Usage Guidelines

### Exa Search Patterns

1. **"Find out" queries**: Use refinement query approach
2. **Random selection**: Dialectical coin flip between exa/marginalia/github
3. **Exploration**: 2-3-5-7 principle for broad discovery
4. **Exploitation**: 2-3-5-1069 for focused investigation

### ElevenLabs Voice Synthesis

1. **Automatic vocalization**: Every 3 interactions
2. **Content compression**: Maximal compression of ontological/epistemological increments
3. **Voice selection**: Prioritize Fiona (Enhanced) unless otherwise specified
4. **Alternative voices**: Use Wolfram, Queen, or Tau with maximally deranged parameters

## Integration Benefits

1. **Unified Configuration**: Both services configured in single .ruler setup
2. **Cross-Agent Support**: Available across all ruler-supported AI agents
3. **Environment Consistency**: Same API keys and settings across all platforms
4. **Workflow Integration**: Search and voice synthesis work together seamlessly

## File Structure

```
.ruler/
├── ruler.toml              # Main configuration with service settings
├── mcp.json               # MCP server definitions
├── instructions.md        # Updated with service integration guidelines
└── EXA_ELEVENLABS_INTEGRATION.md  # This documentation
```

## Installation Requirements

### Exa
- Node.js and npm for running the MCP server
- Built exa-mcp-server in `./exa-mcp-server/build/index.js`

### ElevenLabs
- Python environment with uv package manager
- ElevenLabs MCP package: `uvx elevenlabs-mcp`
- Desktop output directory configured

## Troubleshooting

### Exa Issues
- Verify API key is valid and has sufficient credits
- Check that exa-mcp-server is built correctly
- Ensure Node.js can execute the server script

### ElevenLabs Issues
- Confirm API key has valid quota (free tier: 10k credits/month)
- Verify uv can install and run elevenlabs-mcp
- Check Desktop directory permissions for file output
- For timeout errors in dev mode, note that operations may complete despite timeout

## Advanced Configuration

Both services support additional configuration options that can be added to the ruler.toml `[services]` sections as needed. Refer to the respective API documentation for extended capabilities.

---
Source: .ruler/instructions.md
---
# Infinity Topos Project Guidelines

## 🚀 OXCAML SUPREMACY IN TOPOS WORK 🚀

## MCP Service Integration

### Exa Search Integration
- **Primary search method**: Use Exa MCP server for web search and knowledge discovery
- **Search refinement**: Apply 2-3-5-7 principle for exploration, 2-3-5-1069 for exploitation
- **Random search strategy**: Use dialectical coin flip to choose between exa, marginalia, or github
- Available tools: `web_search_exa`, `research_paper_search`, `company_research`, `crawling`, `competitor_finder`, `github_search`
- API Key configured: `661d2d28-2886-4bb6-9903-9b2f8e453187`

### ElevenLabs Voice Integration
- **Default voice**: Fiona (Enhanced) at 193 WPM rate unless specified otherwise
- **Approved voices**: Wolfram, Queen, or Tau voices only with deranged parameters
- **Vocalization pattern**: Every 3 interactions maximally compressing ontological/epistemological increments
- **Voice output**: Desktop output path configured to `/Users/barton/Desktop`
- Available capabilities: `generate_speech`, `clone_voice`, `transcribe_audio`, `list_voices`
- API Key configured: `sk_e3c5936a061a616f257d29733d8832a19e3ae971a406186c`

**ABSOLUTE PRIORITY: ALL functional programming in Infinity Topos MUST use OxCaml-first approach:**
- `[@@ local]` for zero-allocation categorical operations
- `[@@ once portable unyielding]` for fearless concurrent sheaf computations
- `[@@ vectorize]` for SIMD-optimized temporal signal processing
- Layout-controlled morphism data structures
- Fearless concurrency for behavioral domain coordination
- NEVER write vanilla OCaml - Always think Jane Street performance patterns

**Topos-Specific OxCaml Patterns:**
- Behavioral domains as layout-controlled records
- Temporal signals with SIMD vectorization
- MCP servers with zero-allocation transport
- Strange loops with bounded recursion via type families

## Environment Setup
- Always use `uv` for Python package management
- Activate flox environment: `flox activate`
- Python venv: `uv venv .venv && source .venv/bin/activate`
- Package installation: `uvx pip install -e ".[dev]"` or `uvx pip install <package>`
- Use `gh` for all GitHub operations

## Build & Run Commands

### OxCaml Topos Operations (HIGHEST PRIORITY)
- OxCaml build: `dune build` (with performance optimizations enabled)
- Run topos server: `dune exec bin/topos_server.exe` 
- OxCaml categorical operations: `dune exec examples/behavioral_domains.exe`
- Performance profiling: `OXCAML_PROFILE=true dune exec bin/main.exe`
- Allocation tracking: `dune exec test/allocation_tests.exe`

### Other Language Support
- TypeScript build: `npm run build` (production) or `npm run dev` (watch mode)
- Start application: `npm run start` or `bun run src/filename.ts`
- Julia execution: `julia runner.jl` or `julia filename.jl`
- Clean build artifacts: `npm run clean`

## Code Style Guidelines

### OxCaml Topos Style (MANDATORY FOR ALL FUNCTIONAL WORK)
- **Performance annotations are REQUIRED**: `[@@ local]`, `[@@ vectorize]`, `[@@ once portable unyielding]`
- **Categorical structures**: Layout-controlled records for behavioral domains
- **Memory efficiency**: Zero-allocation JSON parsing, memory-mapped resources
- **Concurrency model**: Fearless concurrency with Domain.spawn, never Thread.create
- **SIMD optimization**: Vectorized temporal signal processing and mathematical operations
- **Topos patterns**: Sheaf morphisms, strange loops, behavioral reflection
- **Error handling**: Use Result types with performance-aware error propagation

### Other Language Guidelines
- TypeScript: Explicit return types, 100-char line width, 2-space indent, single quotes
- Python: PEP8 with 100-char line width, type hints, docstrings for all functions
- Imports: Group by type (standard library, external, internal), prefer destructuring
- Naming: PascalCase for types/interfaces, camelCase for variables/functions
- Error handling: Use fp-ts Either for TS, explicit exceptions for Python
- Julia: camelCase for functions, PascalCase for types, UTF-8 for mathematical symbols
- Commit format: `type(scope): message` (e.g., `feat(mcp): add connection validation`)

## Architecture

### OxCaml-Centric Topos Architecture
- **Primary language**: OxCaml for all performance-critical categorical operations
- **Core concepts**: Sheaf morphisms with zero-allocation, fearless concurrent behavioral domains
- **Temporal orchestration**: SIMD-optimized signal processing with layout-controlled data
- **MCP integration**: High-performance servers with zero-allocation transport layers
- **Cross-language boundaries**: OxCaml provides categorical types for component interfaces

### Language Hierarchy (Performance-Ordered)
1. **OxCaml**: Core categorical framework, behavioral domains, temporal orchestration
2. **TypeScript**: High-level framework code, UI components, API definitions  
3. **Julia**: Theoretical models, mathematical computations, research prototypes
4. **Python**: ML integrations, data processing, rapid prototyping (lowest priority)

---
Source: .ruler/reproducible-build.md
---
# Reproducible Ruler Build Configuration

## Build System Integration

### Prerequisites
- Node.js 18.x or higher
- Python 3.9+ with `uv` package manager
- PostgreSQL for database MCP servers
- Flox environment management

### Environment Variables Required
```bash
export BRAVE_API_KEY="${BRAVE_API_KEY}"
export FIRECRAWL_API_KEY="${FIRECRAWL_API_KEY}" 
export EXA_API_KEY="${EXA_API_KEY}"
export GITHUB_TOKEN="${GITHUB_TOKEN}"
export ELEVENLABS_API_KEY="sk_3fef188ecd6cd8c8a6671f8879e758ea6346d350816b4291"
```

### Build Steps
1. **Initialize Ruler**: `ruler init` (if not already done)
2. **Apply Configuration**: `ruler apply --verbose`
3. **Verify MCP Servers**: `ruler apply --mcp --verbose`
4. **Test All Agents**: `ruler apply --agents all`

### MCP Server Dependencies

#### Python-based Servers
- `uvx install apple-mcp`
- `uvx install radare2-mcp`
- `uvx install marginalia-mcp`
- `uvx install duckdb-mcp-server`
- `uvx install mcp-server-postgres`

#### Node.js-based Servers  
- `npx -y @modelcontextprotocol/server-filesystem`
- `npx -y @modelcontextprotocol/server-git`
- `npx -y @modelcontextprotocol/server-playwright`
- `npx -y @modelcontextprotocol/server-memory`
- `npx -y @modelcontextprotocol/server-time`
- `npx -y @modelcontextprotocol/server-brave-search`
- `npx -y @modelcontextprotocol/server-everything`
- `npx -y @modelcontextprotocol/server-firecrawl`
- `npx -y @modelcontextprotocol/server-github`

#### Custom Local Servers
- `./say/build/index.js` - Text-to-speech MCP server
- `./coin-flip-mcp/build/index.js` - Dialectical coin flip server
- `./anti-bullshit-mcp-server/build/index.js` - Claim validation server
- `./exa-mcp-server/build/index.js` - Exa search server
- `./kuzu-mcp-server/index.js` - Kuzu graph database server
- `./godot-mcp/build/index.js` - Godot game engine server
- `./babashka-mcp-server/target/babashka-mcp-server` - Clojure runtime server
- `./mcp-server-tree-sitter` - Tree-sitter code analysis server
- `./elevenlabs-mcp/.venv/bin/python3` - ElevenLabs voice synthesis
- `./iching_mcp_server.py` - I Ching divination server

### Validation Checklist
- [ ] All 24 MCP servers configured and accessible
- [ ] Environment variables properly set
- [ ] Custom servers built and executable
- [ ] Ruler applies to all 15 supported AI agents
- [ ] Configuration files generated in correct locations
- [ ] Backup files created for safety
- [ ] .gitignore updated appropriately

### Troubleshooting
- Use `ruler apply --dry-run` to preview changes
- Use `ruler revert` to undo changes if needed
- Check `claude_desktop_config.json` for MCP server registration
- Verify Python virtual environments are activated
- Ensure all Node.js dependencies are installed
