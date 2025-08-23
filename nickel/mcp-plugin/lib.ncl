# MCP (Model Context Protocol) Plugin for Nickel
# Leveraging Nickel 1.11+ features for type-safe protocol implementation

let { Dyn, Bool, Str, Num, Array, Dict, optional, default, doc } = std.contract in

# JSON-RPC 2.0 Base Types
let JsonRpcVersion = std.contract.from_predicate (fun v => v == "2.0") in

let JsonRpcId = Dyn in  # Can be string, number, or null

let JsonRpcRequest = {
  jsonrpc | JsonRpcVersion,
  id | JsonRpcId,
  method | Str,
  params | optional | Dyn,
} in

let JsonRpcResponse = {
  jsonrpc | JsonRpcVersion,
  id | JsonRpcId,
  result | optional | Dyn,
  error | optional | {
    code | Num,
    message | Str,
    data | optional | Dyn,
  },
} in

let JsonRpcNotification = {
  jsonrpc | JsonRpcVersion,
  method | Str,
  params | optional | Dyn,
} in

# MCP Protocol Version
let ProtocolVersion = std.enum.TagOrString in

# MCP Message Types using Nickel's ADTs
let MCPMessage = fun label value =>
  value
  |> match {
    'Request payload => 
      std.contract.apply JsonRpcRequest label payload,
    'Response payload => 
      std.contract.apply JsonRpcResponse label payload,
    'Notification payload => 
      std.contract.apply JsonRpcNotification label payload,
  } in

# Transport Types using enhanced enum features
let Transport = [|
  'Stdio { 
    command | Str,
    args | Array Str | default = [],
    env | Dict Str | default = {},
  },
  'Http {
    url | Str,
    headers | Dict Str | default = {},
    sse_endpoint | Str | default = "/sse",
  },
|] in

# Capability Definitions
let Capability = [|
  'Resources {
    subscribe | Bool | default = false,
    list_changed | Bool | default = false,
  },
  'Tools {
    list_changed | Bool | default = false,
  },
  'Prompts {
    list_changed | Bool | default = false,
  },
  'Sampling {
    max_tokens | optional | Num,
    temperature | optional | Num,
    top_p | optional | Num,
  },
|] in

# Resource Schema with enhanced pattern matching
let ResourceType = [|
  'Text { 
    content | Str,
    mime_type | Str | default = "text/plain",
  },
  'Binary {
    data | Str,  # Base64 encoded
    mime_type | Str,
  },
|] in

let Resource = {
  uri | Str
    | doc "Unique identifier for the resource (URI format)",
  name | Str
    | doc "Human-readable name for the resource",
  description | optional | Str
    | doc "Optional description of the resource",
  metadata | optional | Dict Dyn
    | doc "Additional metadata for the resource",
  content | ResourceType,
} in

# Tool Definition with JSON Schema support
let ToolParameter = {
  type | Str,
  description | optional | Str,
  enum | optional | Array Dyn,
  default | optional | Dyn,
  # Recursive schema support for complex types
  properties | optional | Dict ToolParameter,
  items | optional | ToolParameter,
  required | optional | Array Str,
} in

let Tool = {
  name | Str
    | doc "Unique identifier for the tool",
  description | Str
    | doc "Human-readable description of the tool's functionality",
  parameters | {
    type | Str | default = "object",
    properties | Dict ToolParameter,
    required | Array Str | default = [],
    additionalProperties | Bool | default = false,
  },
  # Optional metadata for advanced use cases
  metadata | optional | {
    cost | optional | Num,
    timeout | optional | Num,
    retry | optional | {
      max_attempts | Num | default = 3,
      backoff | [| 'Exponential, 'Linear |] | default = 'Exponential,
    },
  },
} in

# Prompt Templates with dynamic arguments
let PromptArgument = {
  name | Str,
  description | Str,
  required | Bool | default = true,
  type | optional | Str | default = "string",
  default | optional | Dyn,
} in

let Prompt = {
  name | Str,
  description | Str,
  template | Str,
  arguments | Array PromptArgument | default = [],
  metadata | optional | Dict Dyn,
} in

# Server Implementation Type
let MCPServer = {
  name | Str,
  version | Str,
  transport | Transport,
  capabilities | Array Capability | default = [],
  resources | Array Resource | default = [],
  tools | Array Tool | default = [],
  prompts | Array Prompt | default = [],
  
  # Handler functions (in practice, these would be external)
  handlers | optional | {
    on_initialize | optional | Dyn,
    on_request | optional | Dyn,
    on_notification | optional | Dyn,
    on_error | optional | Dyn,
  },
} in

# Client Implementation Type
let MCPClient = {
  name | Str,
  version | Str,
  supported_transports | Array [| 'Stdio, 'Http |],
  capabilities | {
    sampling | optional | {
      models | Array Str,
      max_tokens | Num,
    },
  },
} in

# Connection State Machine using ADTs
let ConnectionState = [|
  'Uninitialized,
  'Initializing { 
    client_info | { name | Str, version | Str },
  },
  'Ready {
    server_info | { name | Str, version | Str },
    capabilities | Array Capability,
  },
  'Error { message | Str, code | Num },
  'Closed,
|] in

# Protocol Messages with full type safety
let Initialize = {
  method | Str | default = "initialize",
  params | {
    protocolVersion | ProtocolVersion,
    capabilities | Dict Bool,
    clientInfo | {
      name | Str,
      version | Str,
    },
  },
} in

let InitializeResult = {
  protocolVersion | ProtocolVersion,
  capabilities | Dict Bool,
  serverInfo | {
    name | Str,
    version | Str,
  },
} in

# Resource Operations
let ListResourcesParams = {
  cursor | optional | Str,
} in

let ListResourcesResult = {
  resources | Array Resource,
  nextCursor | optional | Str,
} in

let ReadResourceParams = {
  uri | Str,
} in

let ReadResourceResult = {
  contents | Array ResourceType,
} in

# Tool Operations
let CallToolParams = {
  name | Str,
  arguments | optional | Dyn,
} in

let CallToolResult = {
  content | Array {
    type | [| 'Text, 'Image, 'Resource |],
    text | optional | Str,
    data | optional | Str,  # Base64 for images
    resource | optional | Resource,
  },
  isError | Bool | default = false,
} in

# Sampling Operations
let CreateMessageParams = {
  messages | Array {
    role | [| 'User, 'Assistant |],
    content | {
      type | [| 'Text, 'Image, 'Resource |],
      text | optional | Str,
      data | optional | Str,
      resource | optional | Resource,
    },
  },
  modelPreferences | optional | {
    hints | Array {
      name | Str,
    },
    costPriority | optional | Num,
    speedPriority | optional | Num,
    intelligencePriority | optional | Num,
  },
  systemPrompt | optional | Str,
  includeContext | [| 'None, 'ThisServer, 'AllServers |] | default = 'ThisServer,
  temperature | optional | Num,
  maxTokens | Num,
  stopSequences | optional | Array Str,
  metadata | optional | Dict Dyn,
} in

let CreateMessageResult = {
  role | [| 'Assistant |],
  content | {
    type | [| 'Text |],
    text | Str,
  },
  model | Str,
  stopReason | optional | [| 'EndTurn, 'StopSequence, 'MaxTokens |],
} in

# Advanced Features using Nickel 1.11+

# Leverage boolean operators in contracts
let ValidServerConfig = fun config =>
  let has_name = std.record.has_field "name" config in
  let has_transport = std.record.has_field "transport" config in
  let valid_version = std.string.is_match "^\\d+\\.\\d+\\.\\d+$" config.version in
  
  # Using new boolean contract operators
  std.contract.from_predicate (fun _ => has_name && has_transport && valid_version)
    "Server must have name, transport, and valid semver version" in

# Type-safe message builder using partial application
let build_request = fun method params => {
  jsonrpc = "2.0",
  id = std.random.uuidv4 {},
  method = method,
  params = params,
} in

let build_notification = fun method params => {
  jsonrpc = "2.0",
  method = method,
  params = params,
} in

# Protocol flow validators using contracts
let ValidProtocolFlow = {
  # Must initialize before any other operations
  initialized | Bool,
  # Track capabilities negotiated
  server_capabilities | Array Capability,
  client_capabilities | Dict Bool,
  
  # Validate operations based on capabilities
  can_list_resources | Bool,
  can_call_tools | Bool,
  can_use_prompts | Bool,
  can_sample | Bool,
} in

# Export public interface
{
  # Core types
  Transport = Transport,
  Capability = Capability,
  Resource = Resource,
  Tool = Tool,
  Prompt = Prompt,
  
  # Server/Client types
  MCPServer = MCPServer,
  MCPClient = MCPClient,
  
  # Message types
  MCPMessage = MCPMessage,
  ConnectionState = ConnectionState,
  
  # Protocol operations
  operations = {
    initialize = Initialize,
    listResources = ListResourcesParams,
    readResource = ReadResourceParams,
    callTool = CallToolParams,
    createMessage = CreateMessageParams,
  },
  
  # Result types
  results = {
    initialize = InitializeResult,
    listResources = ListResourcesResult,
    readResource = ReadResourceResult,
    callTool = CallToolResult,
    createMessage = CreateMessageResult,
  },
  
  # Utilities
  builders = {
    request = build_request,
    notification = build_notification,
  },
  
  # Validators
  validators = {
    server_config = ValidServerConfig,
    protocol_flow = ValidProtocolFlow,
  },
}