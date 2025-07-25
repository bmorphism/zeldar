# Infinity Topos Project Guidelines

## 🚀 OXCAML SUPREMACY IN TOPOS WORK 🚀

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
