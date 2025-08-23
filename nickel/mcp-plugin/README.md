# Nickel MCP Plugin

A comprehensive implementation of the Model Context Protocol (MCP) in Nickel configuration language, featuring both a purist spec-compliant implementation and advanced categorical computing enhancements.

## Overview

This plugin provides:
- **Purist Implementation** (`lib-purist.ncl`): Strict MCP specification compliance
- **Categorical Enhancements** (`categorical-features.ncl`): Advanced topos-theoretic features
- **Neural Sheaf Diffusion** (`neural-sheaf-celegans.ncl`): Heterophilic graph learning for biological networks
- **Capability Discovery** (`capability-discovery.ncl`): Automated server discovery and configuration

## Features

### Core MCP Implementation
- Full JSON-RPC 2.0 support
- All MCP protocol versions (2024-11-05, 2024-10-07)
- Complete type coverage for:
  - Resources (text/binary with subscriptions)
  - Tools (with JSON Schema parameters)
  - Prompts (with dynamic arguments)
  - Sampling (LLM integration)
  - Roots (client-side file system access)
- Transport support: stdio, HTTP/SSE, WebSocket
- Progress tracking and cancellation
- Pagination with cursor support

### Categorical Computing Features
- Path invariance across transport mechanisms
- Topos-theoretic protocol validation
- Natural transformations for protocol adapters
- Monadic effect tracking
- Sheaf-theoretic security models
- Coalgebraic state machines

### Neural Sheaf Diffusion
- Implementation for C. elegans connectomics
- Heterophilic graph learning algorithms
- Cellular sheaf structures
- Diffusion processes (Euler, MidPoint, RK4)

### Capability Discovery System
- High-level capability requirements
- Automated server discovery
- Configuration generation
- Validation suites
- Provisioning pipelines

## Installation

```bash
# Requires Nickel 1.11+
nickel --version  # Should show 1.11.0 or higher

# Clone the repository
git clone <repository-url>
cd nickel/mcp-plugin
```

## Usage

### Basic MCP Server

```nickel
# Import the purist implementation
let mcp = import "lib-purist.ncl" in

# Define a simple MCP server
let my_server = mcp.MCPServer & {
  name = "example-server",
  version = "1.0.0",
  transport = 'Stdio {
    command = "node",
    args = ["server.js"],
  },
  capabilities = {
    resources = { subscribe = true },
    tools = { listChanged = false },
  },
  tools = [{
    name = "hello",
    description = "Say hello",
    inputSchema = {
      type = "object",
      properties = {
        name = { type = "string" },
      },
      required = ["name"],
    },
  }],
} in

my_server
```

### Capability Discovery

```nickel
# Import the discovery system
let discovery = import "capability-discovery.ncl" in

# Define what you need
let requirement = discovery.CapabilityRequirement & {
  category = 'DataAccess,
  functionality = "Query SQL databases with transaction support",
  constraints = {
    latency_ms = 1000,
    require_auth = true,
  },
  priority = 'High,
} in

# Discover and provision
discovery.discover_and_provision requirement
```

### Neural Sheaf for C. elegans

```nickel
# Import neural sheaf implementation
let neural = import "neural-sheaf-celegans.ncl" in

# Load connectome data
let connectome = neural.CElegansConnectome & {
  neurons = [...],  # C. elegans neuron data
  synapses = [...], # Synaptic connections
} in

# Create sheaf structure
let sheaf = neural.create_sheaf_from_connectome connectome in

# Analyze heterophily
neural.compute_heterophily sheaf.graph neuron_labels
```

## Architecture

### File Structure
```
mcp-plugin/
├── lib-purist.ncl              # Core MCP implementation
├── lib-enhanced.ncl            # Enhanced implementation (reference)
├── lib-categorical.ncl         # Original categorical version
├── categorical-features.ncl    # Extracted categorical features
├── neural-sheaf-celegans.ncl  # Neural sheaf diffusion
├── capability-discovery.ncl    # Discovery system
├── capability-demo.ncl         # Discovery examples
├── discovery-integration.ncl   # Real-world integration
└── run-capability-discovery.sh # Demo script
```

### Branch Organization
- `main`: Purist MCP implementation
- `categorical-topos-theoretics`: Advanced categorical features

## Examples

See the following files for detailed examples:
- `example.ncl`: Basic MCP usage
- `capability-demo.ncl`: Capability discovery demonstration
- `discovery-integration.ncl`: Real-world server integration

## Testing

```bash
# Run basic validation
nickel eval lib-purist.ncl

# Test capability discovery
./run-capability-discovery.sh

# Validate specific configuration
nickel eval example.ncl --field my_server
```

## Specification Compliance

This implementation follows the official MCP specification:
- [MCP Documentation](https://modelcontextprotocol.io/docs)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)

### Implemented Features
- ✅ JSON-RPC 2.0 base protocol
- ✅ All message types (request, response, notification)
- ✅ Full capability negotiation
- ✅ Resource management with subscriptions
- ✅ Tool execution with JSON Schema
- ✅ Prompt templates
- ✅ Sampling/LLM integration
- ✅ Progress tracking
- ✅ Cancellation
- ✅ Pagination
- ✅ All transports (stdio, HTTP/SSE, WebSocket)

## Advanced Features

### Path Invariance
Ensures protocol semantics are preserved across different transport mechanisms:
```nickel
let invariant = categorical.PathInvariant & {
  transform = fun msg => transform_to_http msg,
  verify = fun original transformed => 
    semantically_equal original transformed,
}
```

### Topos-Theoretic Validation
Validates protocol flows using categorical laws:
```nickel
let flow = categorical.CategoricalFlow & {
  initial = 'Uninitialized,
  terminal = 'Ready,
  transitions = [...],
  verify_associativity = true,
  verify_identity = true,
}
```

### Effect Tracking
Tracks computational effects monadically:
```nickel
let computation = categorical.MonadicComputation & {
  computation = call_tool "fetch",
  effects = ['IO { description = "HTTP request" }],
  bind = ...,
  return = ...,
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the code style (4-space indent, clear contracts)
4. Add tests for new features
5. Submit a pull request

## License

[License information]

## Acknowledgments

- MCP specification by Anthropic
- Nickel language by Tweag
- Neural Sheaf Diffusion by Bodnar et al.
- C. elegans connectome data from WormWiring