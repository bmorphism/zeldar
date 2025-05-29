# MCP Contract Validators with Topos-Theoretic Properties
# Integrates with the existing categorical computing framework

let MCP = import "./lib.ncl" in
let Topos = import "../lib.ncl" in
let { not, and_scalar, or_scalar } = std.contract in

# Enhanced contract validators using Nickel 1.11+ features

# Transport Security Contract
let SecureTransportContract = fun label value =>
  value |> match {
    'Stdio config => 
      # Stdio must not expose sensitive data in args
      let has_secrets = config.args 
        |> std.array.any (fun arg => 
          std.string.contains "password" arg ||
          std.string.contains "secret" arg ||
          std.string.contains "key" arg
        ) in
      if has_secrets then
        std.contract.blame_with_message "Stdio transport must not contain secrets in args" label
      else
        config,
        
    'Http config =>
      # HTTP must use HTTPS in production
      let is_secure = std.string.starts_with "https://" config.url in
      let has_auth = std.record.has_field "Authorization" config.headers in
      
      if not is_secure && has_auth then
        std.contract.blame_with_message "HTTP transport with auth must use HTTPS" label
      else
        config,
  } in

# Tool Parameter Validation Contract
let ValidToolParameterContract = 
  let valid_types = ["string", "number", "integer", "boolean", "object", "array"] in
  
  fun label param =>
    # Check type is valid
    let type_valid = std.array.elem param.type valid_types in
    
    # If object, must have properties
    let object_valid = 
      if param.type == "object" then
        std.record.has_field "properties" param
      else
        true in
    
    # If array, must have items
    let array_valid =
      if param.type == "array" then
        std.record.has_field "items" param
      else
        true in
    
    # If enum is present, must have valid values
    let enum_valid =
      if std.record.has_field "enum" param then
        std.array.length param.enum > 0
      else
        true in
    
    if type_valid && object_valid && array_valid && enum_valid then
      param
    else
      std.contract.blame_with_message 
        "Invalid tool parameter: %{std.serialize 'Json param}" 
        label in

# Capability Compatibility Contract
let CompatibleCapabilitiesContract = fun label caps =>
  let has_prompts = caps |> std.array.any (fun c => 
    c |> match {
      'Prompts _ => true,
      _ => false,
    }
  ) in
  
  let has_tools = caps |> std.array.any (fun c =>
    c |> match {
      'Tools _ => true,
      _ => false,
    }
  ) in
  
  # Prompts require tools
  if has_prompts && not has_tools then
    std.contract.blame_with_message 
      "Prompts capability requires Tools capability" 
      label
  else
    caps in

# Resource URI Contract with pattern validation
let ValidResourceURIContract = fun label uri =>
  let patterns = [
    "^[a-zA-Z][a-zA-Z0-9+.-]*://",  # Standard URI scheme
    "^resource://",                   # MCP resource scheme
    "^file://",                      # File URI
    "^https?://",                    # HTTP(S) URI
  ] in
  
  let matches_pattern = patterns 
    |> std.array.any (fun pattern => 
      std.string.is_match pattern uri
    ) in
  
  if matches_pattern then
    uri
  else
    std.contract.blame_with_message 
      "Invalid resource URI format: %{uri}" 
      label in

# Path Invariance Contract for MCP
# Ensures tool compositions maintain categorical properties
let MCPPathInvarianceContract = fun label server =>
  # Extract tool dependency graph
  let tool_deps = server.tools 
    |> std.array.map (fun tool =>
      let deps = 
        if std.record.has_field "metadata" tool &&
           std.record.has_field "depends_on" tool.metadata then
          tool.metadata.depends_on
        else
          [] in
      { name = tool.name, deps = deps }
    ) in
  
  # Check for circular dependencies
  let has_cycle = fun visited current =>
    if std.array.elem current visited then
      true
    else
      let current_deps = tool_deps 
        |> std.array.find (fun t => t.name == current)
        |> std.option.map (fun t => t.deps)
        |> std.option.default [] in
      
      current_deps 
        |> std.array.any (fun dep => 
          has_cycle (visited @ [current]) dep
        ) in
  
  let has_circular_deps = tool_deps 
    |> std.array.any (fun tool => 
      has_cycle [] tool.name
    ) in
  
  if has_circular_deps then
    std.contract.blame_with_message 
      "Circular tool dependencies detected" 
      label
  else
    server in

# Realizability Contract for Resources
# Ensures resources can be realized in the effective topos
let RealizableResourceContract = fun label resource =>
  let realizer = Topos.Realizer (fun r =>
    # Check URI is valid
    let uri_valid = ValidResourceURIContract label r.uri == r.uri in
    
    # Check content is realizable based on type
    let content_realizable = r.content |> match {
      'Text { content, mime_type } =>
        std.string.length content < 1000000 &&  # 1MB limit for text
        std.string.is_match "^[\\w/+-]+$" mime_type,
        
      'Binary { data, mime_type } =>
        # Check base64 encoding
        std.string.is_match "^[A-Za-z0-9+/]*={0,2}$" data &&
        std.string.is_match "^[\\w/+-]+$" mime_type,
    } in
    
    uri_valid && content_realizable
  ) in
  
  let result = realizer.apply resource in
  if result.realized then
    resource
  else
    std.contract.blame_with_message 
      "Resource is not realizable in the effective topos" 
      label in

# Monadic Effect Contract for Tools
# Ensures tools properly declare their computational effects
let EffectfulToolContract = fun label tool =>
  let declared_effects = 
    if std.record.has_field "metadata" tool &&
       std.record.has_field "effects" tool.metadata then
      tool.metadata.effects
    else
      [] in
  
  # Analyze tool parameters for implicit effects
  let has_file_params = 
    std.record.values tool.parameters.properties
    |> std.array.any (fun p => 
      std.record.has_field "description" p &&
      (std.string.contains "file" p.description ||
       std.string.contains "path" p.description)
    ) in
  
  let has_network_params =
    std.record.values tool.parameters.properties
    |> std.array.any (fun p =>
      std.record.has_field "description" p &&
      (std.string.contains "url" p.description ||
       std.string.contains "endpoint" p.description)
    ) in
  
  # Check declared effects match inferred effects
  let should_have_io = has_file_params && not (std.array.elem "io" declared_effects) in
  let should_have_network = has_network_params && not (std.array.elem "network" declared_effects) in
  
  if should_have_io || should_have_network then
    std.contract.blame_with_message 
      "Tool '%{tool.name}' has undeclared effects" 
      label
  else
    tool in

# Natural Transformation Contract
# Validates transformations between MCP configurations
let NaturalTransformationContract = fun label transform =>
  let source_valid = MCP.validators.server_config transform.source in
  let target_valid = MCP.validators.server_config transform.target in
  
  # Check functoriality: capabilities are preserved or enhanced
  let caps_preserved = 
    transform.source.capabilities
    |> std.array.all (fun src_cap =>
      transform.target.capabilities
      |> std.array.any (fun tgt_cap =>
        # Same capability type
        (src_cap |> match {
          'Resources _ => tgt_cap |> match { 'Resources _ => true, _ => false },
          'Tools _ => tgt_cap |> match { 'Tools _ => true, _ => false },
          'Prompts _ => tgt_cap |> match { 'Prompts _ => true, _ => false },
          'Sampling _ => tgt_cap |> match { 'Sampling _ => true, _ => false },
        })
      )
    ) in
  
  if source_valid && target_valid && caps_preserved then
    transform
  else
    std.contract.blame_with_message 
      "Invalid natural transformation between MCP servers" 
      label in

# Compositional Contract for Server Arrays
let ComposableServersContract = fun label servers =>
  # Check all servers have unique names
  let names = servers |> std.array.map (fun s => s.name) in
  let unique_names = names |> std.array.length == (names |> std.array.deduplicate |> std.array.length) in
  
  # Check transport compatibility for composition
  let transport_compatible = servers
    |> std.array.sliding_window 2
    |> std.array.all (fun pair =>
      if std.array.length pair == 2 then
        let s1 = std.array.at 0 pair in
        let s2 = std.array.at 1 pair in
        # Both stdio or both http
        (s1.transport |> match {
          'Stdio _ => s2.transport |> match { 'Stdio _ => true, _ => false },
          'Http _ => s2.transport |> match { 'Http _ => true, _ => false },
        })
      else
        true
    ) in
  
  if unique_names && transport_compatible then
    servers
  else
    std.contract.blame_with_message 
      "Servers are not composable" 
      label in

# Export contract collection
{
  # Security contracts
  SecureTransport = SecureTransportContract,
  
  # Validation contracts
  ValidToolParameter = ValidToolParameterContract,
  ValidResourceURI = ValidResourceURIContract,
  CompatibleCapabilities = CompatibleCapabilitiesContract,
  
  # Categorical contracts
  MCPPathInvariance = MCPPathInvarianceContract,
  RealizableResource = RealizableResourceContract,
  EffectfulTool = EffectfulToolContract,
  NaturalTransformation = NaturalTransformationContract,
  ComposableServers = ComposableServersContract,
  
  # Composite validator for full server
  ValidMCPServer = fun label server =>
    server
    |> SecureTransportContract label
    |> std.contract.apply (fun l s => 
      s & {
        capabilities = CompatibleCapabilitiesContract l s.capabilities,
        tools = s.tools |> std.array.map (EffectfulToolContract l),
        resources = s.resources |> std.array.map (RealizableResourceContract l),
      }
    ) label
    |> MCPPathInvarianceContract label,
  
  # Helper to validate server collections
  validate_collection = fun servers =>
    servers
    |> std.record.map (fun name server =>
      {
        valid = (ValidMCPServer name server; true) 
          |> std.contract.catch (fun _ => false),
        server = server,
      }
    ),
}