# Streamable HTTP World Resource with Tree-Sitter Integration
# Working backwards from the requirement: world:// resource + hello tool

let MCP = import "./lib.ncl" in
let Transport = import "./transport.ncl" in
let Contracts = import "./contracts.ncl" in
let TreeSitter = import "../tree-sitter-integration.ncl" in

# Define the World Resource with streaming capabilities
let WorldResource = {
  # Resource definition
  uri = "world://universe/earth",
  name = "World State Stream",
  description = "Streamable representation of world state with code analysis",
  
  # Streaming content generator
  content = 'Text {
    content = "Streaming world state...",
    mime_type = "text/event-stream",
  },
  
  # Metadata for streaming configuration
  metadata = {
    streaming = true,
    chunk_size = 1024,
    update_interval = 1000,  # milliseconds
    tree_sitter_enabled = true,
    supported_languages = ["nickel", "javascript", "python", "rust"],
  },
} in

# Hello Tool that operates on World Resource
let HelloTool = {
  name = "hello",
  description = "Greet the world with code-aware transformations",
  
  parameters = {
    type = "object",
    properties = {
      target = {
        type = "string",
        description = "Target to greet (defaults to 'world')",
        default = "world",
      },
      language = {
        type = "string",
        description = "Programming language for greeting generation",
        enum = ["nickel", "javascript", "python", "rust", "natural"],
        default = "natural",
      },
      stream = {
        type = "boolean",
        description = "Whether to stream the response",
        default = false,
      },
      analyze_code = {
        type = "boolean",
        description = "Use tree-sitter to analyze code context",
        default = true,
      },
    },
    required = [],
  },
  
  # Tool metadata includes streaming capabilities
  metadata = {
    supports_streaming = true,
    requires_auth = ["write", "stream"],
    effects = ["io", "network"],
    tree_sitter_integration = true,
  },
} in

# Streaming HTTP Server Configuration
let StreamingWorldServer = MCP.MCPServer & {
  name = "world-streaming-server",
  version = "1.0.0",
  
  # HTTP transport with SSE for streaming
  transport = 'Http {
    url = "https://world.example.com",
    headers = {
      "X-API-Version" = "1.0",
      "X-Streaming-Enabled" = "true",
    },
    sse_endpoint = "/world/stream",
    timeout = 0,  # No timeout for streaming
    retry = {
      max_attempts = 5,
      initial_delay = 1000,
      max_delay = 30000,
      multiplier = 2,
    },
  },
  
  capabilities = [
    'Resources {
      subscribe = true,
      list_changed = true,
    },
    'Tools {
      list_changed = false,
    },
    'Sampling {
      max_tokens = 8192,
      temperature = 0.7,
    },
  ],
  
  resources = [WorldResource],
  tools = [HelloTool],
} in

# Authentication Configurations
let AuthConfig = [|
  'NoAuth,
  'BasicAuth {
    username | Str,
    password | Str,
  },
  'BearerAuth {
    token | Str,
    refresh_endpoint | optional | Str,
  },
  'ApiKeyAuth {
    key | Str,
    header_name | Str | default = "X-API-Key",
  },
  'OAuth2 {
    client_id | Str,
    client_secret | Str,
    token_endpoint | Str,
    scopes | Array Str | default = ["read", "write"],
  },
|] in

# Streaming Protocol Implementation
let StreamingProtocol = {
  # Initialize streaming connection
  init_stream = fun config auth =>
    let headers = config.headers & (auth |> match {
      'NoAuth => {},
      'BasicAuth { username, password } => {
        "Authorization" = "Basic " ++ std.string.base64 (username ++ ":" ++ password),
      },
      'BearerAuth { token, .. } => {
        "Authorization" = "Bearer " ++ token,
      },
      'ApiKeyAuth { key, header_name } => {
        "%{header_name}" = key,
      },
      'OAuth2 params => {
        # Would implement OAuth2 flow
        "Authorization" = "Bearer <oauth2_token>",
      },
    }) in
    
    {
      endpoint = config.url ++ config.sse_endpoint,
      headers = headers,
      state = 'Connecting { start_time = 1234567890 },
    },
  
  # Generate SSE frames for world updates
  generate_world_frame = fun world_state =>
    let tree_sitter_context = if world_state.analyze_code then
      TreeSitter.analyze_context {
        language = world_state.language,
        code = world_state.content,
      }
    else
      null in
    
    'SSEFrame {
      event = "world-update",
      data = std.serialize 'Json {
        timestamp = std.time.now {},
        state = world_state,
        tree_sitter = tree_sitter_context,
      },
      id = std.random.uuidv4 {},
    },
  
  # Handle hello tool invocation with streaming
  stream_hello_response = fun params =>
    let greeting_generator = fun language target =>
      language |> match {
        "nickel" => m%"
          let greeting = \"Hello, %{target}!\" in
          { message = greeting, timestamp = std.time.now {} }
        "%,
        "javascript" => m%"
          const greeting = `Hello, ${"%{target}"}!`;
          console.log({ message: greeting, timestamp: Date.now() });
        "%,
        "python" => m%"
          greeting = f\"Hello, %{target}!\"
          print({\"message\": greeting, \"timestamp\": time.time()})
        "%,
        "rust" => m%"
          let greeting = format!(\"Hello, {}!\", \"%{target}\");
          println!(\"{{\\\"message\\\": \\\"{}\\\", \\\"timestamp\\\": {}}}\", greeting, std::time::SystemTime::now());
        "%,
        "natural" => "Hello, %{target}! Welcome to the streaming world.",
        _ => "Hello, %{target}!",
      } in
    
    let code = greeting_generator params.language params.target in
    let chunks = if params.stream then
      # Split into streamable chunks
      std.string.split_at code 50  # 50 chars per chunk
    else
      [code] in
    
    chunks |> std.array.map (fun chunk => 'SSEFrame {
      event = "hello-response",
      data = std.serialize 'Json {
        chunk = chunk,
        complete = false,
        language = params.language,
        analyzed = params.analyze_code && TreeSitter.is_valid_code params.language chunk,
      },
    }) @ ['SSEFrame {
      event = "hello-complete",
      data = std.serialize 'Json { complete = true },
    }],
} in

# Tree-Sitter Integration for Code Analysis
let TreeSitterIntegration = {
  # Analyze code in world context
  analyze_world_code = fun resource =>
    let code_blocks = TreeSitter.extract_code_blocks resource.content in
    let analyses = code_blocks |> std.array.map (fun block =>
      TreeSitter.analyze {
        language = block.language,
        code = block.content,
        context = "world-resource",
      }
    ) in
    
    {
      resource = resource,
      code_blocks = code_blocks,
      analyses = analyses,
      summary = {
        total_blocks = std.array.length code_blocks,
        languages = code_blocks |> std.array.map (fun b => b.language) |> std.array.deduplicate,
        has_errors = analyses |> std.array.any (fun a => a.has_errors),
      },
    },
  
  # Generate code-aware greetings
  generate_contextual_greeting = fun context language =>
    let imports = context.imports |> std.array.join ", " in
    let functions = context.functions |> std.array.map (fun f => f.name) |> std.array.join ", " in
    
    m%"
    Hello! I see you're working with %{language}.
    Your code imports: %{imports}
    Functions defined: %{functions}
    
    Let me help you with your %{context.primary_construct} implementation.
    "%,
} in

# Complete Streaming Configuration
let StreamingConfiguration = {
  # Create server with auth
  create_authenticated_server = fun auth_config =>
    let base_server = StreamingWorldServer in
    let transport_with_auth = base_server.transport |> match {
      'Http config =>
        let auth_headers = auth_config |> match {
          'NoAuth => {},
          'BasicAuth { username, password } => {
            "Authorization" = "Basic " ++ std.string.base64 (username ++ ":" ++ password),
          },
          'BearerAuth { token, .. } => {
            "Authorization" = "Bearer " ++ token,
          },
          'ApiKeyAuth { key, header_name } => {
            "%{header_name}" = key,
          },
          'OAuth2 _ => {
            "Authorization" = "Bearer <oauth2_token>",
          },
        } in
        'Http (config & { headers = config.headers & auth_headers }),
      _ => base_server.transport,
    } in
    
    base_server & { transport = transport_with_auth },
  
  # Example configurations
  examples = {
    # No authentication
    public_server = create_authenticated_server 'NoAuth,
    
    # Basic authentication
    basic_auth_server = create_authenticated_server ('BasicAuth {
      username = "world_user",
      password = "secure_password",
    }),
    
    # Bearer token authentication
    bearer_auth_server = create_authenticated_server ('BearerAuth {
      token = "eyJhbGciOiJIUzI1NiIs...",
      refresh_endpoint = "/auth/refresh",
    }),
    
    # API key authentication
    api_key_server = create_authenticated_server ('ApiKeyAuth {
      key = "world_api_key_12345",
      header_name = "X-World-API-Key",
    }),
  },
  
  # Stream handler
  handle_stream = fun server request =>
    request.method |> match {
      "hello" => StreamingProtocol.stream_hello_response request.params,
      "resources/read" => 
        if request.params.uri == "world://universe/earth" then
          [StreamingProtocol.generate_world_frame {
            content = WorldResource.content.content,
            language = "natural",
            analyze_code = true,
          }]
        else
          [MCP.builders.error_frame "Resource not found"],
      _ => [MCP.builders.error_frame "Method not supported"],
    },
} in

# Export the complete streaming world implementation
{
  # Core components
  WorldResource = WorldResource,
  HelloTool = HelloTool,
  StreamingWorldServer = StreamingWorldServer,
  
  # Authentication
  AuthConfig = AuthConfig,
  
  # Protocols
  StreamingProtocol = StreamingProtocol,
  TreeSitterIntegration = TreeSitterIntegration,
  
  # Configuration
  StreamingConfiguration = StreamingConfiguration,
  
  # Utilities
  test_streaming = fun =>
    let config = StreamingConfiguration.examples.api_key_server in
    let request = {
      method = "hello",
      params = {
        target = "universe",
        language = "nickel",
        stream = true,
        analyze_code = true,
      },
    } in
    StreamingConfiguration.handle_stream config request,
}