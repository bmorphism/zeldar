# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-06-20

### Added
- Initial implementation of Model Context Protocol (MCP) for OCaml
- JSON-RPC 2.0 message handling
- Resource and tool management APIs
- Server interface for MCP implementations
- Async support with Lwt
- Type-safe message parsing and generation
- Example executable demonstrating usage
- Comprehensive test suite
- Documentation and examples

### Features
- `Mcp.create_message` - Create MCP protocol messages
- `Mcp.message_to_json` / `Mcp.message_of_json` - JSON serialization
- `Mcp.Server` module for server implementations
- Support for resources and tools
- Protocol version management

[Unreleased]: https://github.com/yourusername/mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/mcp/releases/tag/v0.1.0

