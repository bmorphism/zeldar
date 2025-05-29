# MCP Integration Module - Spec-Compliant Implementation
# Strict adherence to Model Context Protocol specification
# Prioritizes latest Streamable HTTP (2025-04-16) over legacy SSE

let MCP = import "./lib.ncl" in
let Transport = import "./transport.ncl" in
let Capabilities = import "./capabilities.ncl" in
let Contracts = import "./contracts.ncl" in
let { Dyn, Bool, Str, Num, Array, Dict, optional, default, doc } = std.contract in

# MCP Protocol Version Constants (from spec)
let ProtocolVersions = {
  latest = "2025-04-16",      # Latest Streamable HTTP
  streamable_http = "2025-04-16",
  legacy_sse = "2024-11-05",  # Legacy SSE support
  initial = "2024-11-05",     # Initial protocol version
} in

# Spec-Compliant Message Types
let SpecCompliantMessages = {
  # Initialize request (spec: 4.2.1)
  InitializeRequest = {
    jsonrpc | Str | default = "2.0",
    id | Str | Num,
    method | Str | default = "initialize",
    params | {
      protocolVersion | Str,
      capabilities | {
        sampling | optional | Bool,
        resources | optional | {
          subscribe | optional | Bool,
          listChanged | optional | Bool,
        },
        tools | optional | {
          listChanged | optional | Bool,
        },
        prompts | optional | {
          listChanged | optional | Bool,
        },
        logging | optional | Bool,
      },
      clientInfo | {
        name | Str,
        version | Str,
      },
    },
  },
  
  # Initialize response (spec: 4.2.1)
  InitializeResponse = {
    jsonrpc | Str | default = "2.0",
    id | Str | Num,
    result | {
      protocolVersion | Str,
      capabilities | {
        sampling | optional | Bool,
        resources | optional | {
          subscribe | optional | Bool,
          listChanged | optional | Bool,
        },
        tools | optional | {
          listChanged | optional | Bool,
        },
        prompts | optional | {
          listChanged | optional | Bool,
        },
        logging | optional | Bool,
      },
      serverInfo | {
        name | Str,
        version | Str,
      },
      instructions | optional | Str,
    },
  },
  
  # Error response (spec: 3.2)
  ErrorResponse = {
    jsonrpc | Str | default = "2.0",
    id | Str | Num | null,
    error | {
      code | Num,
      message | Str,
      data | optional | Dyn,
    },
  },
} in

# Transport Detection and Prioritization
let TransportSelector = {
  # Detect transport type from URL or configuration
  detect_transport = fun config =>
    if std.record.has_field "url" config then
      # HTTP-based transport
      if std.record.has_field "sse_endpoint" config && 
         config.use_legacy_sse | default = false then
        'LegacySSE
      else
        'StreamableHTTP  # Default to latest spec
    else if std.record.has_field "command" config then
      'Stdio
    else
      std.contract.blame "Invalid transport configuration",
  
  # Create transport based on detection
  create_transport = fun config =>
    let transport_type = detect_transport config in
    transport_type |> match {
      'StreamableHTTP => create_streamable_http_transport config,
      'LegacySSE => create_legacy_sse_transport config,
      'Stdio => Transport.StdioTransport.create ('StdioConfig config),
    },
  
  # Streamable HTTP Transport (Latest Spec)
  create_streamable_http_transport = fun config =>
    {
      type = 'StreamableHTTP,
      version = ProtocolVersions.streamable_http,
      config = config,
      
      # Connection endpoint (spec: Streamable HTTP transport)
      endpoints = {
        base = config.url,
        # Single endpoint for bidirectional streaming
        stream = "%{config.url}/mcp/v1",
      },
      
      # HTTP/2 with streaming support
      protocol = {
        http_version = "2.0",
        content_type = "application/json+mcp",
        accept = "application/json+mcp",
        # Streaming headers
        headers = config.headers & {
          "MCP-Version" = ProtocolVersions.streamable_http,
          "MCP-Transport" = "streamable-http",
          "Accept-Encoding" = "gzip, deflate",
          "Cache-Control" = "no-cache",
        },
      },
      
      # Frame handling for streaming
      frame_handler = {
        # Parse incoming frames
        parse_frame = fun data =>
          # Length-prefixed JSON frames
          let length = std.string.substring 0 4 data 
            |> std.string.to_bytes 
            |> (fun bytes => 
              bytes[0] * 16777216 + 
              bytes[1] * 65536 + 
              bytes[2] * 256 + 
              bytes[3]
            ) in
          let json_data = std.string.substring 4 (4 + length) data in
          std.deserialize 'Json json_data,
        
        # Create outgoing frames
        create_frame = fun message =>
          let json = std.serialize 'Json message in
          let length = std.string.length json in
          let length_bytes = [
            (length / 16777216) % 256,
            (length / 65536) % 256,
            (length / 256) % 256,
            length % 256,
          ] in
          std.string.from_bytes length_bytes ++ json,
      },
      
      # Bidirectional streaming
      streaming = {
        bidirectional = true,
        keep_alive = {
          enabled = true,
          interval = 30000,  # 30 seconds
          timeout = 60000,   # 60 seconds
        },
        compression = {
          enabled = true,
          algorithm = "gzip",
        },
      },
    },
  
  # Legacy SSE Transport (Backward Compatibility)
  create_legacy_sse_transport = fun config =>
    {
      type = 'LegacySSE,
      version = ProtocolVersions.legacy_sse,
      config = config,
      
      # Separate endpoints for SSE
      endpoints = {
        base = config.url,
        sse = config.sse_endpoint | default = "/sse",
        messages = "/messages",
      },
      
      # SSE-specific configuration
      protocol = {
        http_version = "1.1",
        sse_headers = {
          "Content-Type" = "text/event-stream",
          "Cache-Control" = "no-cache",
          "Connection" = "keep-alive",
          "X-Accel-Buffering" = "no",  # Disable proxy buffering
        },
      },
      
      # SSE event handling
      event_handler = {
        parse_event = fun data =>
          Transport.HttpTransport.create(config).parse_sse data,
        
        create_event = fun event_type data =>
          let event_line = if event_type != null then
            "event: %{event_type}\n"
          else
            "" in
          let data_lines = data 
            |> std.string.split "\n"
            |> std.array.map (fun line => "data: %{line}")
            |> std.array.join "\n" in
          "%{event_line}%{data_lines}\n\n",
      },
    },
} in

# Spec-Compliant Server Implementation
let SpecCompliantServer = {
  # Create server with spec validation
  create = fun config =>
    # Validate configuration against spec
    let validated_config = Contracts.ValidMCPServer "server" config in
    
    # Determine transport
    let transport = TransportSelector.create_transport config.transport in
    
    {
      # Server metadata
      info = {
        name = config.name,
        version = config.version,
        protocol_version = transport.version,
      },
      
      # Transport layer
      transport = transport,
      
      # Capabilities
      capabilities = Capabilities.validate_capabilities config.capabilities,
      
      # Resources, Tools, Prompts
      resources = config.resources |> std.array.map (fun r =>
        Contracts.RealizableResource "resource" r
      ),
      tools = config.tools |> std.array.map (fun t =>
        Contracts.EffectfulTool "tool" t
      ),
      prompts = config.prompts,
      
      # Message handlers (spec-compliant)
      handlers = {
        # Initialize handler (spec: 4.2.1)
        handle_initialize = fun request =>
          # Validate protocol version
          let client_version = request.params.protocolVersion in
          let supported = client_version == transport.version ||
                         (client_version == ProtocolVersions.legacy_sse && 
                          transport.type == 'LegacySSE) in
          
          if !supported then
            {
              jsonrpc = "2.0",
              id = request.id,
              error = {
                code = -32602,  # Invalid params
                message = "Unsupported protocol version: %{client_version}",
                data = {
                  supported_versions = [transport.version],
                },
              },
            }
          else
            {
              jsonrpc = "2.0",
              id = request.id,
              result = {
                protocolVersion = transport.version,
                capabilities = {
                  sampling = config.capabilities |> std.array.any (fun c =>
                    c |> match { 'Sampling _ => true, _ => false }
                  ),
                  resources = config.capabilities |> std.array.find (fun c =>
                    c |> match { 'Resources caps => caps, _ => null }
                  ),
                  tools = config.capabilities |> std.array.find (fun c =>
                    c |> match { 'Tools caps => caps, _ => null }
                  ),
                  prompts = config.capabilities |> std.array.find (fun c =>
                    c |> match { 'Prompts caps => caps, _ => null }
                  ),
                },
                serverInfo = {
                  name = config.name,
                  version = config.version,
                },
              },
            },
        
        # Resource handlers (spec: 5.2)
        handle_resources_list = fun request =>
          let cursor = request.params.cursor | default = null in
          let resources = Capabilities.Resources.create({}).manager.list_resources 
            {} cursor 100 in
          
          {
            jsonrpc = "2.0",
            id = request.id,
            result = resources,
          },
        
        # Tool handlers (spec: 5.3)
        handle_tools_call = fun request =>
          let tool_name = request.params.name in
          let arguments = request.params.arguments | default = {} in
          
          let executor = Capabilities.Tools.create({}).executor in
          let result = executor.execute executor tool_name arguments in
          
          {
            jsonrpc = "2.0",
            id = request.id,
            result = result.result,
          },
        
        # Sampling handlers (spec: 5.5)
        handle_sampling_create = fun request =>
          let engine = Capabilities.Sampling.create(config.sampling_config | default = {}).engine in
          let completion = engine.create_completion request.params in
          
          completion |> match {
            'Stream stream =>
              # Return streaming response
              {
                jsonrpc = "2.0",
                id = request.id,
                result = {
                  _stream = true,
                  _streamId = std.random.uuidv4 {},
                },
              },
            'Complete response =>
              {
                jsonrpc = "2.0",
                id = request.id,
                result = response.response,
              },
          },
      },
      
      # Request router
      route_request = fun server request =>
        request.method |> match {
          "initialize" => server.handlers.handle_initialize request,
          "resources/list" => server.handlers.handle_resources_list request,
          "resources/read" => server.handlers.handle_resources_read request,
          "tools/list" => server.handlers.handle_tools_list request,
          "tools/call" => server.handlers.handle_tools_call request,
          "prompts/list" => server.handlers.handle_prompts_list request,
          "prompts/get" => server.handlers.handle_prompts_get request,
          "sampling/create" => server.handlers.handle_sampling_create request,
          _ => {
            jsonrpc = "2.0",
            id = request.id,
            error = {
              code = -32601,  # Method not found
              message = "Method not found: %{request.method}",
            },
          },
        },
    },
} in

# World Resource Implementation (Spec-Compliant)
let WorldResourceImplementation = {
  # Create world:// resource handler
  create = fun =>
    {
      uri_scheme = "world://",
      
      # Parse world URI
      parse_uri = fun uri =>
        if !std.string.starts_with "world://" uri then
          std.contract.blame "Invalid world URI: %{uri}"
        else
          let path = std.string.substring 8 uri in
          let parts = std.string.split "/" path in
          {
            universe = std.array.at 0 parts | default = "default",
            world = std.array.at 1 parts | default = "earth",
            region = std.array.at 2 parts | default = null,
          },
      
      # World resource with streaming
      create_resource = fun uri =>
        let parsed = parse_uri uri in
        {
          uri = uri,
          name = "World: %{parsed.universe}/%{parsed.world}",
          description = "Streamable world state for %{parsed.world} in %{parsed.universe}",
          content = 'Text {
            content = "Initializing world state stream...",
            mime_type = "application/x-world-stream",
          },
          metadata = {
            streaming = true,
            universe = parsed.universe,
            world = parsed.world,
            region = parsed.region,
            update_frequency = 100,  # ms
            supports_tree_sitter = true,
          },
        },
      
      # Stream world updates
      stream_updates = fun resource =>
        let state = {
          tick = 0,
          entities = [],
          events = [],
        } in
        
        # Update generator
        let generate_update = fun state =>
          let new_state = state & {
            tick = state.tick + 1,
            events = if state.tick % 10 == 0 then
              state.events @ [{
                type = "world_event",
                timestamp = std.time.now {},
                description = "Periodic world update",
              }]
            else
              state.events,
          } in
          
          {
            state = new_state,
            frame = Transport.MessageFrame |> match {
              _ => 'SSEFrame {
                event = "world-update",
                data = std.serialize 'Json {
                  tick = new_state.tick,
                  world = resource.metadata.world,
                  timestamp = std.time.now {},
                  entities_count = std.array.length new_state.entities,
                  recent_events = new_state.events |> std.array.slice -5,
                },
              },
            },
          },
        
        # Return stream handler
        {
          initial_state = state,
          generate_update = generate_update,
          should_continue = fun state => state.tick < 1000,  # Stop after 1000 ticks
        },
    },
  
  # Hello tool for world resource
  hello_tool = {
    name = "hello",
    description = "Greet entities in the world with code-aware responses",
    parameters = {
      type = "object",
      properties = {
        target = {
          type = "string",
          description = "Entity or location to greet",
          default = "world",
        },
        language = {
          type = "string",
          enum = ["natural", "nickel", "javascript", "python", "rust"],
          default = "natural",
        },
        include_code_context = {
          type = "boolean",
          default = true,
        },
        format = {
          type = "string",
          enum = ["text", "markdown", "code"],
          default = "text",
        },
      },
      required = [],
      additionalProperties = false,
    },
    
    # Execution handler
    execute = fun args =>
      let greeting = args.language |> match {
        "natural" => "Hello, %{args.target}!",
        "nickel" => "let greeting = \"Hello, %{args.target}!\" in greeting",
        "javascript" => "console.log('Hello, %{args.target}!');",
        "python" => "print(f'Hello, {args.target}!')",
        "rust" => "println!(\"Hello, {}!\", \"%{args.target}\");",
        _ => "Hello, %{args.target}!",
      } in
      
      let formatted = args.format |> match {
        "markdown" => "```%{args.language}\n%{greeting}\n```",
        "code" => greeting,
        _ => greeting,
      } in
      
      {
        content = [
          {
            type = 'Text,
            text = formatted,
          },
        ],
        isError = false,
        metadata = {
          language = args.language,
          target = args.target,
          timestamp = std.time.now {},
        },
      },
  },
} in

# Export Integration Module
{
  # Protocol versions
  ProtocolVersions = ProtocolVersions,
  
  # Spec-compliant types
  SpecCompliantMessages = SpecCompliantMessages,
  
  # Transport selection
  TransportSelector = TransportSelector,
  
  # Server implementation
  SpecCompliantServer = SpecCompliantServer,
  
  # World resource
  WorldResourceImplementation = WorldResourceImplementation,
  
  # Helper to create spec-compliant server
  create_server = fun config =>
    let server_config = config & {
      # Ensure latest protocol by default
      transport = config.transport & {
        use_legacy_sse = config.force_legacy_sse | default = false,
      },
    } in
    SpecCompliantServer.create server_config,
  
  # Version compatibility check
  is_version_compatible = fun client_version server_version =>
    client_version == server_version ||
    (client_version == ProtocolVersions.legacy_sse && 
     server_version == ProtocolVersions.streamable_http),  # Forward compatible
}