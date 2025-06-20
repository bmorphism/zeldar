# MCP - Model Context Protocol for OCaml

A comprehensive OCaml implementation of the Model Context Protocol (MCP).

## Overview

MCP is a protocol that enables AI assistants to securely access and interact with external tools and data sources in a controlled, permission-based manner.

## Features

- Complete MCP protocol implementation
- JSON-RPC 2.0 based communication
- Resource and tool management
- Async/concurrent support with Lwt
- Type-safe message handling

## Installation

```bash
opam install mcp
```

## Usage

### Basic Server

```ocaml
open Mcp

let server = Server.create ()

let resource = {
  uri = "example://resource/1";
  name = "Example Resource";
  description = Some "An example resource";
  mime_type = Some "text/plain";
}

let tool = {
  name = "echo";
  description = "Echoes input";
  input_schema = `Assoc [("type", `String "object")];
}

let () =
  Server.add_resource server resource;
  Server.add_tool server tool;
  Server.set_initialized server
```

### Message Handling

```ocaml
let msg = create_message ~id:"1" ~method_:"resources/list" () in
let json = message_to_json msg in
let parsed = message_of_json json
```

## Development

### Build

```bash
dune build
```

### Test

```bash
dune test
```

### Example

```bash
dune exec bin/main.exe
```

## License

MIT

