# MCP Transport Layer Implementation
# Leveraging Nickel 1.11+ for type-safe, idempotent transport

let MCP = import "./lib.ncl" in
let Contracts = import "./contracts.ncl" in
let { Dyn, Bool, Str, Num, Array, Dict, optional, default, doc } = std.contract in

# Transport Configuration Types with ADTs
let TransportConfig = [|
  'StdioConfig {
    command | Str,
    args | Array Str | default = [],
    env | Dict Str | default = {},
    working_dir | optional | Str,
    inherit_env | Bool | default = true,
    buffer_size | Num | default = 65536,
  },
  'HttpConfig {
    url | Str,
    headers | Dict Str | default = {},
    sse_endpoint | Str | default = "/sse",
    timeout | Num | default = 30000,  # milliseconds
    retry | {
      max_attempts | Num | default = 3,
      initial_delay | Num | default = 1000,
      max_delay | Num | default = 32000,
      multiplier | Num | default = 2,
    } | default = {},
    tls | optional | {
      verify | Bool | default = true,
      ca_cert | optional | Str,
      client_cert | optional | Str,
      client_key | optional | Str,
    },
  },
|] in

# Connection State with Enhanced Pattern Matching
let ConnectionState = [|
  'Disconnected { 
    reason | optional | Str,
    reconnectable | Bool | default = true,
  },
  'Connecting { 
    attempt | Num | default = 1,
    start_time | Num,  # Unix timestamp
  },
  'Connected {
    transport_info | TransportConfig,
    established_at | Num,  # Unix timestamp
    bytes_sent | Num | default = 0,
    bytes_received | Num | default = 0,
  },
  'Reconnecting {
    attempt | Num,
    last_error | Str,
    next_retry_at | Num,  # Unix timestamp
  },
  'Failed {
    error | Str,
    attempts | Num,
    permanent | Bool | default = false,
  },
|] in

# Message Framing for Different Transports
let MessageFrame = [|
  'StdioFrame {
    # Content-Length header style (LSP-like)
    content_length | Num,
    content_type | Str | default = "application/json",
    body | Str,
  },
  'HttpFrame {
    # HTTP request/response
    method | Str | default = "POST",
    path | Str | default = "/",
    headers | Dict Str,
    body | Str,
  },
  'SSEFrame {
    # Server-Sent Events
    event | optional | Str,
    data | Str,
    id | optional | Str,
    retry | optional | Num,
  },
|] in

# Transport Layer Interface using Contracts
let TransportLayer = {
  # Initialize transport
  initialize | TransportConfig -> { Dyn -> Dyn }
    | doc "Initialize transport and return connection handler",
  
  # Send message
  send | MessageFrame -> { Dyn -> Dyn }
    | doc "Send a message through the transport",
  
  # Receive message
  receive | {} -> { Dyn -> MessageFrame }
    | doc "Receive a message from the transport",
  
  # Close connection
  close | {} -> { Dyn -> Dyn }
    | doc "Close the transport connection gracefully",
  
  # Get connection state
  get_state | {} -> ConnectionState
    | doc "Get current connection state",
  
  # Health check
  health_check | {} -> {
    connected | Bool,
    latency | optional | Num,
    throughput | optional | {
      send_rate | Num,  # bytes/sec
      receive_rate | Num,  # bytes/sec
    },
  },
} in

# Stdio Transport Implementation Pattern
let StdioTransport = {
  create = fun config =>
    config |> match {
      'StdioConfig params =>
        let validate_command = fun cmd =>
          if std.string.length cmd == 0 then
            std.contract.blame "Command cannot be empty"
          else if std.string.contains ".." cmd then
            std.contract.blame "Command cannot contain path traversal"
          else
            cmd in
        
        let safe_config = params & {
          command = validate_command params.command,
          # Sanitize environment variables
          env = params.env |> std.record.filter (fun k v =>
            !(std.string.contains "SECRET" k || std.string.contains "KEY" k)
          ),
        } in
        
        {
          config = safe_config,
          state = 'Disconnected { reason = "Not started" },
          
          # Message framing for stdio
          frame_message = fun message =>
            let json = std.serialize 'Json message in
            let length = std.string.length json in
            'StdioFrame {
              content_length = length,
              body = json,
            },
          
          # Parse incoming frames
          parse_frame = fun raw_data =>
            # Extract Content-Length header
            let header_end = std.string.find "\r\n\r\n" raw_data in
            if header_end >= 0 then
              let header = std.string.substring 0 header_end raw_data in
              let body_start = header_end + 4 in
              let content_length = 
                # Parse Content-Length: <number>
                std.string.find_all "Content-Length: (\\d+)" header
                |> std.array.first
                |> std.option.map (fun m => std.string.to_number (std.array.at 1 m))
                |> std.option.default 0 in
              
              'StdioFrame {
                content_length = content_length,
                body = std.string.substring body_start (body_start + content_length) raw_data,
              }
            else
              std.contract.blame "Invalid stdio frame: missing headers",
        },
        
      _ => std.contract.blame "Invalid transport config for stdio"
    },
  
  # Idempotent connection management
  connect = fun transport =>
    transport.state |> match {
      'Connected _ => transport,  # Already connected, idempotent
      _ => transport & {
        state = 'Connected {
          transport_info = 'StdioConfig transport.config,
          established_at = 1234567890,  # Would use actual timestamp
        },
      },
    },
} in

# HTTP Transport with SSE Implementation Pattern
let HttpTransport = {
  create = fun config =>
    config |> match {
      'HttpConfig params =>
        # Validate URL
        let validate_url = fun url =>
          if !(std.string.starts_with "http://" url || std.string.starts_with "https://" url) then
            std.contract.blame "URL must start with http:// or https://"
          else if params.tls.verify && std.string.starts_with "http://" url then
            std.contract.blame "TLS verification requires https://"
          else
            url in
        
        {
          config = params & { url = validate_url params.url },
          state = 'Disconnected {},
          sse_buffer = "",  # Buffer for partial SSE frames
          
          # HTTP request builder
          build_request = fun method path body =>
            'HttpFrame {
              method = method,
              path = path,
              headers = params.headers & {
                "Content-Type" = "application/json",
                "Accept" = "application/json",
                "Content-Length" = std.to_string (std.string.length body),
              },
              body = body,
            },
          
          # SSE frame parser
          parse_sse = fun data =>
            let lines = std.string.split "\n" data in
            let parse_line = fun acc line =>
              if std.string.starts_with "event:" line then
                acc & { event = std.string.trim (std.string.substring 6 line) }
              else if std.string.starts_with "data:" line then
                acc & { data = std.string.trim (std.string.substring 5 line) }
              else if std.string.starts_with "id:" line then
                acc & { id = std.string.trim (std.string.substring 3 line) }
              else if std.string.starts_with "retry:" line then
                acc & { retry = std.string.to_number (std.string.trim (std.string.substring 6 line)) }
              else
                acc in
            
            std.array.fold parse_line {} lines
            |> (fun frame => 'SSEFrame frame),
          
          # Exponential backoff for retries
          calculate_backoff = fun attempt =>
            let delay = params.retry.initial_delay * (params.retry.multiplier ^ (attempt - 1)) in
            std.number.min delay params.retry.max_delay,
        },
        
      _ => std.contract.blame "Invalid transport config for HTTP"
    },
  
  # Connection with automatic retry
  connect_with_retry = fun transport attempt =>
    if attempt > transport.config.retry.max_attempts then
      transport & {
        state = 'Failed {
          error = "Max retry attempts exceeded",
          attempts = attempt - 1,
          permanent = false,
        }
      }
    else
      let backoff_delay = transport.calculate_backoff attempt in
      transport & {
        state = 'Reconnecting {
          attempt = attempt,
          last_error = "Connection failed",
          next_retry_at = 1234567890 + backoff_delay,  # Would use actual timestamp
        }
      },
} in

# Transport Manager for Multi-Transport Support
let TransportManager = {
  # Create transport based on config
  create_transport = fun config =>
    config |> match {
      'StdioConfig _ => StdioTransport.create config,
      'HttpConfig _ => HttpTransport.create config,
    },
  
  # Validate transport configuration
  validate_transport = fun config =>
    let validation = config |> match {
      'StdioConfig params =>
        Contracts.SecureTransport "transport" ('Stdio params),
      'HttpConfig params =>
        Contracts.SecureTransport "transport" ('Http params),
    } in
    { valid = true, config = validation },
  
  # Create connection pool for multiple transports
  create_pool = fun configs =>
    let transports = configs |> std.array.map create_transport in
    {
      transports = transports,
      active_transport = 0,
      
      # Round-robin selection
      select_transport = fun pool =>
        let transport = std.array.at pool.active_transport pool.transports in
        let next_active = (pool.active_transport + 1) % std.array.length pool.transports in
        { transport = transport, pool = pool & { active_transport = next_active } },
      
      # Health-based selection
      select_healthy_transport = fun pool =>
        let healthy_transports = pool.transports
          |> std.array.filter (fun t =>
            t.state |> match {
              'Connected _ => true,
              _ => false,
            }
          ) in
        
        if std.array.length healthy_transports > 0 then
          std.array.first healthy_transports
        else
          # Try to reconnect first disconnected transport
          pool.transports
            |> std.array.find (fun t =>
              t.state |> match {
                'Disconnected { reconnectable = true } => true,
                _ => false,
              }
            )
            |> std.option.default (std.array.first pool.transports),
    },
} in

# Export Transport Module
{
  # Types
  TransportConfig = TransportConfig,
  ConnectionState = ConnectionState,
  MessageFrame = MessageFrame,
  TransportLayer = TransportLayer,
  
  # Implementations
  StdioTransport = StdioTransport,
  HttpTransport = HttpTransport,
  
  # Manager
  TransportManager = TransportManager,
  
  # Utilities
  is_connected = fun state =>
    state |> match {
      'Connected _ => true,
      _ => false,
    },
  
  get_transport_type = fun config =>
    config |> match {
      'StdioConfig _ => "stdio",
      'HttpConfig _ => "http",
    },
  
  # Message utilities
  create_json_rpc_frame = fun transport message =>
    transport |> match {
      'StdioConfig _ => StdioTransport.create(transport).frame_message message,
      'HttpConfig _ => HttpTransport.create(transport).build_request "POST" "/rpc" (std.serialize 'Json message),
    },
}