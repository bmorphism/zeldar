# MCP Plugin Example - Leveraging Nickel 1.11+ Features
# Demonstrates advanced usage patterns and best practices

let MCP = import "./lib.ncl" in
let { Dyn, Bool, Str, Num, Array, Dict, optional, default, doc } = std.contract in

# Example 1: Define a Knowledge Base Server
let KnowledgeBaseServer = MCP.MCPServer & {
  name = "knowledge-base-server",
  version = "1.0.0",
  
  transport = 'Stdio {
    command = "node",
    args = ["./kb-server.js"],
    env = {
      KB_PATH = "/data/knowledge",
      LOG_LEVEL = "info",
    },
  },
  
  capabilities = [
    'Resources {
      subscribe = true,
      list_changed = true,
    },
    'Tools {},
    'Prompts {},
  ],
  
  resources = [
    {
      uri = "kb://documents/index",
      name = "Document Index",
      description = "Searchable index of all knowledge base documents",
      content = 'Text {
        content = "Dynamic content loaded from knowledge base",
        mime_type = "application/json",
      },
    },
    {
      uri = "kb://embeddings/semantic-search",
      name = "Semantic Search Embeddings",
      description = "Vector embeddings for semantic search",
      content = 'Binary {
        data = "", # Base64 encoded embeddings
        mime_type = "application/octet-stream",
      },
      metadata = {
        dimensions = 1536,
        model = "text-embedding-ada-002",
      },
    },
  ],
  
  tools = [
    {
      name = "search_knowledge",
      description = "Search the knowledge base using natural language queries",
      parameters = {
        type = "object",
        properties = {
          query = {
            type = "string",
            description = "Natural language search query",
          },
          filters = {
            type = "object",
            description = "Optional filters for search",
            properties = {
              category = {
                type = "string",
                enum = ["technical", "business", "general"],
              },
              date_range = {
                type = "object",
                properties = {
                  start = { type = "string", description = "ISO date" },
                  end = { type = "string", description = "ISO date" },
                },
              },
            },
          },
          limit = {
            type = "integer",
            description = "Maximum number of results",
            default = 10,
          },
        },
        required = ["query"],
      },
      metadata = {
        cost = 0.001,  # Cost per invocation
        timeout = 5.0,  # 5 second timeout
        retry = {
          max_attempts = 3,
          backoff = 'Exponential,
        },
      },
    },
    {
      name = "extract_entities",
      description = "Extract named entities from text",
      parameters = {
        type = "object",
        properties = {
          text = {
            type = "string",
            description = "Text to analyze",
          },
          entity_types = {
            type = "array",
            description = "Types of entities to extract",
            items = {
              type = "string",
              enum = ["person", "organization", "location", "date", "technical_term"],
            },
            default = ["person", "organization", "location"],
          },
        },
        required = ["text"],
      },
    },
  ],
  
  prompts = [
    {
      name = "research_assistant",
      description = "Research assistant prompt for comprehensive information gathering",
      template = m%"
You are a research assistant with access to a comprehensive knowledge base.

Query: {{query}}

Context:
{{#if context}}
{{context}}
{{/if}}

Please provide a thorough analysis addressing:
1. Key findings from the knowledge base
2. Relevant connections and relationships
3. Potential gaps or areas needing clarification
4. Recommendations for further research

{{#if format}}
Format your response as: {{format}}
{{/if}}
      "%,
      arguments = [
        {
          name = "query",
          description = "The research question or topic",
          required = true,
        },
        {
          name = "context",
          description = "Additional context for the research",
          required = false,
        },
        {
          name = "format",
          description = "Desired output format",
          required = false,
          type = "string",
          enum = ["summary", "detailed", "bullet_points"],
          default = "detailed",
        },
      ],
    },
  ],
}
| doc "Knowledge Base MCP Server with semantic search and entity extraction" in

# Example 2: Multi-Transport API Gateway using ADTs
let APIGatewayServer = 
  let auth_middleware = {
    type = "bearer",
    validation = {
      endpoint = "https://auth.example.com/validate",
      cache_ttl = 300,
    },
  } in
  
  MCP.MCPServer & {
    name = "api-gateway",
    version = "2.0.0",
    
    # Demonstrate HTTP transport with SSE
    transport = 'Http {
      url = "https://gateway.example.com",
      headers = {
        "X-API-Version" = "2.0",
        "Authorization" = "Bearer ${API_KEY}",
      },
      sse_endpoint = "/mcp/events",
    },
    
    capabilities = [
      'Tools { list_changed = true },
      'Sampling {
        max_tokens = 8192,
        temperature = 0.7,
        top_p = 0.95,
      },
    ],
    
    tools = std.array.generate (fun i => {
      name = "api_endpoint_%{std.to_string i}",
      description = "Auto-generated API endpoint wrapper",
      parameters = {
        type = "object",
        properties = {
          method = {
            type = "string",
            enum = ["GET", "POST", "PUT", "DELETE"],
            default = "GET",
          },
          path = {
            type = "string",
            description = "API path (e.g., /users/123)",
          },
          body = {
            type = "object",
            description = "Request body for POST/PUT",
            additionalProperties = true,
          },
          headers = {
            type = "object",
            description = "Additional headers",
            additionalProperties = true,
          },
        },
        required = ["method", "path"],
      },
      metadata = {
        cost = if i < 5 then 0.0001 else 0.001,
        timeout = 30.0,
      },
    }) 10,  # Generate 10 API endpoint tools
  } in

# Example 3: Advanced Protocol Flow with State Machine
let ProtocolFlowExample = {
  # Initial state
  initial_state = 'Uninitialized,
  
  # State transitions using pattern matching
  transition = fun state message =>
    state |> match {
      'Uninitialized => 
        if message.method == "initialize" then
          'Initializing { 
            client_info = message.params.clientInfo 
          }
        else
          'Error { 
            message = "Must initialize first", 
            code = -32002 
          },
          
      'Initializing { client_info } =>
        'Ready {
          server_info = { 
            name = "example-server", 
            version = "1.0.0" 
          },
          capabilities = ['Resources {}, 'Tools {}],
        },
        
      'Ready { .. } =>
        # Handle various operations when ready
        if message.method == "tools/call" then
          state  # Stay in Ready state
        else if message.method == "shutdown" then
          'Closed
        else
          state,
          
      'Error { .. } => state,  # Error state is terminal
      'Closed => state,        # Closed state is terminal
    },
  
  # Validate state transitions
  is_valid_transition = fun from_state to_state =>
    (from_state, to_state) |> match {
      ('Uninitialized, 'Initializing _) => true,
      ('Initializing _, 'Ready _) => true,
      ('Initializing _, 'Error _) => true,
      ('Ready _, 'Ready _) => true,
      ('Ready _, 'Closed) => true,
      ('Ready _, 'Error _) => true,
      _ => false,
    },
} in

# Example 4: Compositional Server Builder
let CompositionalServerBuilder = {
  # Base server template
  base = {
    name = "compositional-server",
    version = "1.0.0",
    transport = 'Stdio { command = "node", args = [] },
    capabilities = [],
    resources = [],
    tools = [],
    prompts = [],
  },
  
  # Builder functions using function composition
  with_name = fun name server => server & { name = name },
  
  with_transport = fun transport server => server & { transport = transport },
  
  add_capability = fun cap server => 
    server & { capabilities = server.capabilities @ [cap] },
  
  add_tool = fun tool server =>
    server & { tools = server.tools @ [tool] },
  
  add_resource = fun resource server =>
    server & { resources = server.resources @ [resource] },
  
  # Compose multiple tools at once
  add_tools = fun tools server =>
    std.array.fold (fun acc tool => add_tool tool acc) server tools,
  
  # Build with validation
  build = fun server =>
    let validation = MCP.validators.server_config server in
    if validation then
      server
    else
      std.contract.blame "Invalid server configuration",
} in

# Example 5: Type-safe Message Flow
let MessageFlowExample = {
  # Create initialization flow
  init_flow = fun client_name client_version =>
    let request = MCP.builders.request "initialize" {
      protocolVersion = "2024-11-05",
      capabilities = {
        sampling = true,
        resources = true,
        tools = true,
      },
      clientInfo = {
        name = client_name,
        version = client_version,
      },
    } in
    
    let response = {
      jsonrpc = "2.0",
      id = request.id,
      result = {
        protocolVersion = "2024-11-05",
        capabilities = {
          resources = { subscribe = true },
          tools = { listChanged = true },
        },
        serverInfo = {
          name = "example-server",
          version = "1.0.0",
        },
      },
    } in
    
    { request = request, response = response },
  
  # Tool invocation flow
  tool_flow = fun tool_name args =>
    let request = MCP.builders.request "tools/call" {
      name = tool_name,
      arguments = args,
    } in
    
    let response = {
      jsonrpc = "2.0",
      id = request.id,
      result = {
        content = [
          {
            type = 'Text,
            text = "Tool execution result",
          },
        ],
        isError = false,
      },
    } in
    
    { request = request, response = response },
} in

# Example 6: Advanced Capability Negotiation
let CapabilityNegotiation = {
  # Define capability compatibility matrix
  compatibility_matrix = {
    resources = {
      requires = [],
      enhances = ["tools"],  # Resources enhance tools
    },
    tools = {
      requires = [],
      enhances = ["sampling"],  # Tools enhance sampling
    },
    prompts = {
      requires = ["tools"],  # Prompts require tools
      enhances = ["sampling"],
    },
    sampling = {
      requires = [],
      enhances = [],
    },
  },
  
  # Negotiate optimal capabilities
  negotiate = fun server_caps client_caps =>
    let requested = std.record.fields client_caps 
      |> std.array.filter (fun k => std.record.get k client_caps) in
    
    let available = server_caps 
      |> std.array.map (fun cap => 
        cap |> match {
          'Resources _ => "resources",
          'Tools _ => "tools",
          'Prompts _ => "prompts",
          'Sampling _ => "sampling",
        }
      ) in
    
    let negotiated = requested 
      |> std.array.filter (fun r => std.array.elem r available) in
    
    {
      negotiated = negotiated,
      missing = requested |> std.array.filter (fun r => !(std.array.elem r available)),
      additional = available |> std.array.filter (fun a => !(std.array.elem a requested)),
    },
} in

# Export all examples
{
  servers = {
    knowledge_base = KnowledgeBaseServer,
    api_gateway = APIGatewayServer,
  },
  
  patterns = {
    protocol_flow = ProtocolFlowExample,
    server_builder = CompositionalServerBuilder,
    message_flow = MessageFlowExample,
    capability_negotiation = CapabilityNegotiation,
  },
  
  # Utility to create a full server from builder pattern
  create_custom_server = fun config =>
    CompositionalServerBuilder.base
    |> CompositionalServerBuilder.with_name config.name
    |> CompositionalServerBuilder.with_transport config.transport
    |> CompositionalServerBuilder.add_tools config.tools
    |> CompositionalServerBuilder.build,
  
  # Validate all examples
  validation = {
    kb_server_valid = MCP.validators.server_config KnowledgeBaseServer,
    api_gateway_valid = MCP.validators.server_config APIGatewayServer,
  },
}