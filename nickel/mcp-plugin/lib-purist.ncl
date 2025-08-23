# MCP (Model Context Protocol) Plugin for Nickel - Purist Implementation
# Strict compliance with MCP specification without categorical enhancements
# Based on official TypeScript and Python SDK implementations

let { Dyn, Bool, Str, Num, Array, Dict, optional, default, doc } = std.contract in

# Protocol versions
let LATEST_PROTOCOL_VERSION = "2024-11-05" in
let SUPPORTED_PROTOCOL_VERSIONS = ["2024-11-05", "2024-10-07"] in

# JSON-RPC 2.0 Constants
let JSONRPC_VERSION = "2.0" in

# Standard JSON-RPC error codes
let ErrorCodes = {
  PARSE_ERROR = -32700,
  INVALID_REQUEST = -32600,
  METHOD_NOT_FOUND = -32601,
  INVALID_PARAMS = -32602,
  INTERNAL_ERROR = -32603,
} in

# Base Types

# Progress token for async operations
let ProgressToken = std.contract.from_predicate (fun v =>
  std.typeof v == 'String || std.typeof v == 'Number
) in

# Cursor for pagination
let Cursor = Str in

# Request ID can be string, number, or null
let RequestId = std.contract.from_predicate (fun v =>
  v == null || std.typeof v == 'String || std.typeof v == 'Number
) in

# JSON-RPC 2.0 Base Types
let JsonRpcRequest = {
  jsonrpc | Str | std.contract.from_predicate (fun v => v == JSONRPC_VERSION),
  id | RequestId,
  method | Str,
  params | optional | Dyn,
} in

let JsonRpcResponse = {
  jsonrpc | Str | std.contract.from_predicate (fun v => v == JSONRPC_VERSION),
  id | RequestId,
  result | optional | Dyn,
  error | optional | {
    code | Num,
    message | Str,
    data | optional | Dyn,
  },
} in

let JsonRpcNotification = {
  jsonrpc | Str | std.contract.from_predicate (fun v => v == JSONRPC_VERSION),
  method | Str,
  params | optional | Dyn,
} in

# Base Request with meta support for progress tracking
let BaseRequestParams = {
  _meta | optional | {
    progressToken | optional | ProgressToken,
  },
} in

let BaseNotificationParams = {
  _meta | optional | Dict Dyn,
} in

let BaseResult = {
  _meta | optional | Dict Dyn,
} in

# Pagination support
let PaginatedRequest = BaseRequestParams & {
  cursor | optional | Cursor,
} in

let PaginatedResult = BaseResult & {
  nextCursor | optional | Cursor,
} in

# MCP Protocol Version
let ProtocolVersion = std.contract.from_predicate (fun v =>
  std.array.elem v SUPPORTED_PROTOCOL_VERSIONS
) in

# Transport Types
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
  'WebSocket {
    url | Str,
    headers | Dict Str | default = {},
    reconnect | Bool | default = true,
    reconnect_delay | Num | default = 1000,
  },
|] in

# Implementation info
let Implementation = {
  name | Str,
  version | Str,
} in

# Client Capabilities
let ClientCapabilities = {
  experimental | optional | Dict Dyn,
  roots | optional | {
    listChanged | optional | Bool,
  },
  sampling | optional | Dict Dyn,
} in

# Server Capabilities
let ServerCapabilities = {
  experimental | optional | Dict Dyn,
  logging | optional | Dict Dyn,
  prompts | optional | {
    listChanged | optional | Bool,
  },
  resources | optional | {
    subscribe | optional | Bool,
    listChanged | optional | Bool,
  },
  tools | optional | {
    listChanged | optional | Bool,
  },
} in

# Annotations for metadata
let Annotated = {
  annotations | optional | {
    audience | optional | Array Str,
  },
} in

# Resource Types
let TextResourceContents = {
  uri | Str,
  mimeType | optional | Str,
  text | Str,
} in

let BlobResourceContents = {
  uri | Str,
  mimeType | optional | Str,
  blob | Str,  # Base64 encoded
} in

let ResourceContents = std.contract.from_predicate (fun value =>
  (std.record.has_field "text" value && !std.record.has_field "blob" value) ||
  (!std.record.has_field "text" value && std.record.has_field "blob" value)
) in

let Resource = Annotated & {
  uri | Str,
  name | Str,
  description | optional | Str,
  mimeType | optional | Str,
} in

let ResourceTemplate = Annotated & {
  uriTemplate | Str,
  name | Str,
  description | optional | Str,
  mimeType | optional | Str,
} in

# Tool Definition
let ToolInputSchema = {
  type | Str | default = "object",
  properties | optional | Dict Dyn,
  required | optional | Array Str,
  additionalProperties | optional | Bool | default = false,
} in

let Tool = Annotated & {
  name | Str,
  description | optional | Str,
  inputSchema | ToolInputSchema,
} in

# Prompt Templates
let PromptArgument = {
  name | Str,
  description | optional | Str,
  required | optional | Bool,
} in

let Prompt = Annotated & {
  name | Str,
  description | optional | Str,
  arguments | optional | Array PromptArgument,
} in

# Roots (Client feature)
let Root = {
  uri | Str,
  name | optional | Str,
} in

# Protocol Messages

# Cancellation
let CancelledNotificationParams = BaseNotificationParams & {
  requestId | RequestId,
  reason | optional | Str,
} in

# Progress notifications
let ProgressNotificationParams = BaseNotificationParams & {
  progressToken | ProgressToken,
  progress | Num,
  total | optional | Num,
} in

# Logging
let LogLevel = [| 'Debug, 'Info, 'Notice, 'Warning, 'Error, 'Critical, 'Alert, 'Emergency |] in

let LoggingMessageNotificationParams = BaseNotificationParams & {
  level | LogLevel,
  logger | optional | Str,
  data | Dyn,
} in

# Initialization
let InitializeRequestParams = BaseRequestParams & {
  protocolVersion | Str,
  capabilities | ClientCapabilities,
  clientInfo | Implementation,
} in

let InitializeResult = BaseResult & {
  protocolVersion | Str,
  capabilities | ServerCapabilities,
  serverInfo | Implementation,
  instructions | optional | Str,
} in

# Resources
let ListResourcesRequestParams = PaginatedRequest in

let ListResourcesResult = PaginatedResult & {
  resources | Array Resource,
} in

let ListResourceTemplatesRequestParams = PaginatedRequest in

let ListResourceTemplatesResult = PaginatedResult & {
  resourceTemplates | Array ResourceTemplate,
} in

let ReadResourceRequestParams = BaseRequestParams & {
  uri | Str,
} in

let ReadResourceResult = BaseResult & {
  contents | Array ResourceContents,
} in

let SubscribeRequestParams = BaseRequestParams & {
  uri | Str,
} in

let UnsubscribeRequestParams = BaseRequestParams & {
  uri | Str,
} in

let ResourceUpdatedNotificationParams = BaseNotificationParams & {
  uri | Str,
} in

# Tools
let ListToolsRequestParams = PaginatedRequest in

let ListToolsResult = PaginatedResult & {
  tools | Array Tool,
} in

let CallToolRequestParams = BaseRequestParams & {
  name | Str,
  arguments | optional | Dict Dyn,
} in

let ToolContent = [|
  'Text { text | Str },
  'Image { data | Str, mimeType | Str },
  'Resource { uri | Str, text | optional | Str, blob | optional | Str, mimeType | optional | Str },
|] in

let CallToolResult = BaseResult & {
  content | optional | Array ToolContent,
  isError | optional | Bool | default = false,
} in

# Prompts
let ListPromptsRequestParams = PaginatedRequest in

let ListPromptsResult = PaginatedResult & {
  prompts | Array Prompt,
} in

let GetPromptRequestParams = BaseRequestParams & {
  name | Str,
  arguments | optional | Dict Str,
} in

let PromptMessage = {
  role | [| 'User, 'Assistant |],
  content | [|
    'Text { text | Str },
    'Image { data | Str, mimeType | Str },
    'Resource { resource | Resource },
  |],
} in

let GetPromptResult = BaseResult & {
  description | optional | Str,
  messages | Array PromptMessage,
} in

# Completion
let CompleteRequestParams = BaseRequestParams & {
  ref | [| 'Resource { uri | Str }, 'Prompt { name | Str, arguments | optional | Dict Str } |],
  argument | {
    name | Str,
    value | Str,
  },
} in

let Completion = {
  values | Array Str,
  total | optional | Num,
  hasMore | optional | Bool | default = false,
} in

let CompleteResult = BaseResult & {
  completion | Completion,
} in

# Roots
let ListRootsRequestParams = BaseRequestParams in

let ListRootsResult = BaseResult & {
  roots | Array Root,
} in

# Sampling
let SamplingMessage = {
  role | [| 'User, 'Assistant |],
  content | [|
    'Text { text | Str },
    'Image { data | Str, mimeType | Str },
  |],
} in

let ModelPreferences = {
  hints | optional | Array { name | optional | Str },
  costPriority | optional | Num,
  speedPriority | optional | Num,
  intelligencePriority | optional | Num,
} in

let CreateMessageRequestParams = BaseRequestParams & {
  messages | Array SamplingMessage,
  modelPreferences | optional | ModelPreferences,
  systemPrompt | optional | Str,
  includeContext | optional | [| 'None, 'ThisServer, 'AllServers |] | default = 'None,
  temperature | optional | Num,
  maxTokens | Num,
  stopSequences | optional | Array Str,
  metadata | optional | Dict Dyn,
} in

let CreateMessageResult = BaseResult & {
  role | [| 'Assistant |],
  content | {
    type | [| 'Text |],
    text | Str,
  },
  model | Str,
  stopReason | optional | Str,
} in

# Ping
let PingRequestParams = BaseRequestParams in

# Connection State Machine
let ConnectionState = [|
  'Uninitialized,
  'Initializing { 
    clientInfo | Implementation,
  },
  'Ready {
    serverInfo | Implementation,
    serverCapabilities | ServerCapabilities,
    clientCapabilities | ClientCapabilities,
  },
  'Error { message | Str, code | Num },
  'Closed,
|] in

# Server Implementation Type
let MCPServer = {
  name | Str,
  version | Str,
  transport | Transport,
  capabilities | ServerCapabilities | default = {},
  resources | Array Resource | default = [],
  tools | Array Tool | default = [],
  prompts | Array Prompt | default = [],
  
  # Handler functions (in practice, these would be external)
  handlers | optional | {
    on_initialize | optional | Dyn,
    on_request | optional | Dyn,
    on_notification | optional | Dyn,
    on_error | optional | Dyn,
    on_progress | optional | Dyn,
    on_cancelled | optional | Dyn,
  },
} in

# Client Implementation Type
let MCPClient = {
  name | Str,
  version | Str,
  supported_transports | Array [| 'Stdio, 'Http, 'WebSocket |],
  capabilities | ClientCapabilities | default = {},
} in

# Type-safe message builders
let build_request = fun method params => {
  jsonrpc = JSONRPC_VERSION,
  id = std.random.uuidv4 {},
  method = method,
  params = params,
} in

let build_notification = fun method params => {
  jsonrpc = JSONRPC_VERSION,
  method = method,
  params = params,
} in

let build_error = fun id code message data => {
  jsonrpc = JSONRPC_VERSION,
  id = id,
  error = {
    code = code,
    message = message,
    data = data,
  },
} in

# Export public interface
{
  # Constants
  JSONRPC_VERSION = JSONRPC_VERSION,
  LATEST_PROTOCOL_VERSION = LATEST_PROTOCOL_VERSION,
  SUPPORTED_PROTOCOL_VERSIONS = SUPPORTED_PROTOCOL_VERSIONS,
  ErrorCodes = ErrorCodes,
  
  # Base types
  ProgressToken = ProgressToken,
  Cursor = Cursor,
  RequestId = RequestId,
  
  # Core types
  Transport = Transport,
  Implementation = Implementation,
  ClientCapabilities = ClientCapabilities,
  ServerCapabilities = ServerCapabilities,
  Resource = Resource,
  ResourceTemplate = ResourceTemplate,
  Tool = Tool,
  Prompt = Prompt,
  Root = Root,
  
  # Server/Client types
  MCPServer = MCPServer,
  MCPClient = MCPClient,
  
  # Message types
  ConnectionState = ConnectionState,
  
  # Request parameter types
  requests = {
    initialize = InitializeRequestParams,
    ping = PingRequestParams,
    
    # Resources
    listResources = ListResourcesRequestParams,
    listResourceTemplates = ListResourceTemplatesRequestParams,
    readResource = ReadResourceRequestParams,
    subscribe = SubscribeRequestParams,
    unsubscribe = UnsubscribeRequestParams,
    
    # Tools
    listTools = ListToolsRequestParams,
    callTool = CallToolRequestParams,
    
    # Prompts
    listPrompts = ListPromptsRequestParams,
    getPrompt = GetPromptRequestParams,
    
    # Completion
    complete = CompleteRequestParams,
    
    # Roots
    listRoots = ListRootsRequestParams,
    
    # Sampling
    createMessage = CreateMessageRequestParams,
  },
  
  # Result types
  results = {
    initialize = InitializeResult,
    listResources = ListResourcesResult,
    listResourceTemplates = ListResourceTemplatesResult,
    readResource = ReadResourceResult,
    listTools = ListToolsResult,
    callTool = CallToolResult,
    listPrompts = ListPromptsResult,
    getPrompt = GetPromptResult,
    complete = CompleteResult,
    listRoots = ListRootsResult,
    createMessage = CreateMessageResult,
  },
  
  # Notification parameter types
  notifications = {
    cancelled = CancelledNotificationParams,
    progress = ProgressNotificationParams,
    resourceUpdated = ResourceUpdatedNotificationParams,
    loggingMessage = LoggingMessageNotificationParams,
  },
  
  # Content types
  ResourceContents = ResourceContents,
  TextResourceContents = TextResourceContents,
  BlobResourceContents = BlobResourceContents,
  ToolContent = ToolContent,
  
  # Utilities
  builders = {
    request = build_request,
    notification = build_notification,
    error = build_error,
  },
}