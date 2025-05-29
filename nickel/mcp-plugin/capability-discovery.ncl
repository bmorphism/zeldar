# MCP Capability Discovery and Server Configuration System
# Automated discovery, validation, and configuration of MCP servers
# based on high-level capability requirements

let { Dyn, Bool, Str, Num, Array, Dict, optional, default, doc } = std.contract in

# Import base MCP types
let mcp = import "lib-purist.ncl" in

# High-level capability definitions

let CapabilityCategory = [|
  'DataAccess,      # Access to databases, files, APIs
  'Computation,     # Processing, analysis, ML inference
  'Visualization,   # Rendering, charting, diagramming
  'Communication,   # Messaging, notifications, webhooks
  'Storage,         # Persistent data, caching, archival
  'Security,        # Auth, encryption, validation
  'Integration,     # Third-party services, protocols
  'Monitoring,      # Logging, metrics, observability
|] in

let CapabilityRequirement = {
  # What capability is needed
  category | CapabilityCategory,
  
  # Specific functionality required
  functionality | Str
    | doc "High-level description of required functionality",
  
  # Constraints and preferences
  constraints | optional | {
    # Performance requirements
    latency_ms | optional | Num,
    throughput_rps | optional | Num,
    
    # Resource constraints
    max_memory_mb | optional | Num,
    max_cpu_cores | optional | Num,
    
    # Security requirements
    require_encryption | Bool | default = true,
    require_auth | Bool | default = true,
    allowed_regions | optional | Array Str,
  },
  
  # Priority level
  priority | [| 'Critical, 'High, 'Medium, 'Low |] | default = 'Medium,
  
  # Optional examples of desired behavior
  examples | optional | Array {
    input | Dyn,
    expected_output | Dyn,
  },
} in

# Server discovery mechanisms

let DiscoveryMethod = [|
  'Registry { url | Str },           # Central registry
  'DNS { domain | Str },              # DNS-SD/mDNS
  'Static { servers | Array Str },   # Predefined list
  'Dynamic { endpoint | Str },        # API endpoint
  'P2P { network | Str },            # Peer-to-peer discovery
  'CloudProvider { provider | Str },  # Cloud service discovery
|] in

let ServerMetadata = {
  # Basic info
  name | Str,
  version | Str,
  url | Str,
  
  # Capabilities advertised
  capabilities | {
    categories | Array CapabilityCategory,
    features | Array Str,
    api_version | Str,
  },
  
  # Performance characteristics
  performance | optional | {
    avg_latency_ms | Num,
    max_throughput_rps | Num,
    uptime_percent | Num,
  },
  
  # Requirements
  requirements | optional | {
    min_client_version | optional | Str,
    required_auth | optional | Array Str,
    supported_transports | Array mcp.Transport,
  },
  
  # Trust and verification
  trust | optional | {
    verified | Bool | default = false,
    reputation_score | optional | Num,
    endorsements | optional | Array Str,
  },
} in

# Capability matching engine

let CapabilityMatcher = {
  # Match requirements to server capabilities
  match_score | CapabilityRequirement -> ServerMetadata -> Num,
  
  # Detailed match analysis
  match_details | CapabilityRequirement -> ServerMetadata -> {
    score | Num,
    matched_features | Array Str,
    missing_features | Array Str,
    constraint_violations | Array Str,
    recommendations | optional | Array Str,
  },
  
  # Ranking function
  rank_servers | CapabilityRequirement -> Array ServerMetadata -> Array {
    server | ServerMetadata,
    score | Num,
    rationale | Str,
  },
} in

# Configuration generation

let ServerConfiguration = {
  # Connection settings
  connection | {
    transport | mcp.Transport,
    timeout_ms | Num | default = 30000,
    retry_attempts | Num | default = 3,
    retry_delay_ms | Num | default = 1000,
  },
  
  # Authentication
  auth | optional | {
    method | [| 'None, 'ApiKey, 'OAuth2, 'mTLS, 'Custom |],
    credentials | optional | Dyn,
  },
  
  # Feature flags
  features | {
    enable_caching | Bool | default = true,
    enable_compression | Bool | default = true,
    enable_telemetry | Bool | default = false,
  },
  
  # Resource limits
  limits | {
    max_request_size_mb | Num | default = 10,
    max_response_size_mb | Num | default = 100,
    request_timeout_ms | Num | default = 60000,
  },
} in

# Validation framework

let ValidationTest = {
  # Test metadata
  name | Str,
  description | Str,
  category | [| 'Connectivity, 'Functionality, 'Performance, 'Security |],
  
  # Test specification
  test | {
    # Setup phase
    setup | optional | Dyn,
    
    # Test execution
    execute | {
      method | Str,
      params | optional | Dyn,
      expected_result | optional | Dyn,
    },
    
    # Cleanup phase
    cleanup | optional | Dyn,
  },
  
  # Success criteria
  criteria | {
    timeout_ms | Num | default = 5000,
    retry_on_failure | Bool | default = false,
    required_for_approval | Bool | default = true,
  },
} in

let ValidationSuite = {
  # Basic connectivity tests
  connectivity_tests | Array ValidationTest,
  
  # Capability-specific tests
  capability_tests | Array ValidationTest,
  
  # Performance benchmarks
  performance_tests | optional | Array ValidationTest,
  
  # Security validation
  security_tests | optional | Array ValidationTest,
  
  # Overall validation policy
  policy | {
    min_pass_rate | Num | default = 0.95,
    required_categories | Array [| 'Connectivity, 'Functionality |],
    max_total_duration_ms | Num | default = 300000,
  },
} in

# Discovery service

let DiscoveryService = {
  # Discovery configuration
  methods | Array DiscoveryMethod,
  
  # Cache settings
  cache | {
    enabled | Bool | default = true,
    ttl_seconds | Num | default = 3600,
    max_entries | Num | default = 1000,
  },
  
  # Discovery filters
  filters | optional | {
    # Geographic filters
    regions | optional | Array Str,
    
    # Capability filters
    required_categories | optional | Array CapabilityCategory,
    required_features | optional | Array Str,
    
    # Trust filters
    min_reputation | optional | Num,
    require_verified | Bool | default = false,
  },
  
  # Discovery hooks
  hooks | optional | {
    on_server_found | optional | ServerMetadata -> Dyn,
    on_server_lost | optional | Str -> Dyn,
    on_discovery_error | optional | Dyn -> Dyn,
  },
} in

# Configuration wizard

let ConfigurationWizard = {
  # Analyze requirements and generate config
  generate_config | CapabilityRequirement -> ServerMetadata -> ServerConfiguration,
  
  # Interactive configuration
  interactive_config | {
    # Questions to ask user
    questions | Array {
      id | Str,
      prompt | Str,
      type | [| 'Boolean, 'Number, 'String, 'Choice |],
      options | optional | Array Str,
      default | optional | Dyn,
      validation | optional | Dyn -> Bool,
    },
    
    # Configuration builder
    build_config | Dict Dyn -> ServerConfiguration,
  },
  
  # Configuration optimization
  optimize_config | ServerConfiguration -> ServerMetadata -> ServerConfiguration,
  
  # Configuration validation
  validate_config | ServerConfiguration -> ServerMetadata -> {
    valid | Bool,
    errors | Array Str,
    warnings | Array Str,
    suggestions | Array Str,
  },
} in

# Automated provisioning

let ProvisioningPipeline = {
  # Pipeline stages
  stages | [
    'Discovery,
    'Matching,
    'Configuration,
    'Validation,
    'Deployment,
    'Monitoring,
  ],
  
  # Stage implementations
  implementations | {
    # Discover available servers
    discovery | CapabilityRequirement -> DiscoveryService -> Array ServerMetadata,
    
    # Match and rank servers
    matching | CapabilityRequirement -> Array ServerMetadata -> Array {
      server | ServerMetadata,
      score | Num,
      config | ServerConfiguration,
    },
    
    # Configure selected server
    configuration | ServerMetadata -> ServerConfiguration -> {
      configured_server | Dyn,
      connection_string | Str,
      credentials | optional | Dyn,
    },
    
    # Validate configuration
    validation | Dyn -> ValidationSuite -> {
      passed | Bool,
      results | Array {
        test | Str,
        passed | Bool,
        duration_ms | Num,
        error | optional | Str,
      },
    },
    
    # Deploy to production
    deployment | Dyn -> {
      deployed | Bool,
      endpoint | Str,
      health_check_url | optional | Str,
    },
    
    # Setup monitoring
    monitoring | Dyn -> {
      metrics_endpoint | Str,
      alerts_configured | Bool,
      dashboards | Array Str,
    },
  },
  
  # Pipeline execution
  execute | CapabilityRequirement -> {
    status | [| 'Success, 'PartialSuccess, 'Failed |],
    selected_server | optional | ServerMetadata,
    configuration | optional | ServerConfiguration,
    validation_results | optional | Dyn,
    deployment_info | optional | Dyn,
    errors | Array Str,
  },
} in

# MCP Tools for capability discovery

let DiscoveryTools = {
  # Discover servers by capability
  discover_by_capability | mcp.Tool & {
    name = "discover_mcp_servers",
    description = "Discover MCP servers that match capability requirements",
    inputSchema = {
      type = "object",
      properties = {
        capability | {
          type = "string",
          description = "High-level capability description",
        },
        category | {
          type = "string",
          enum = ["data_access", "computation", "visualization", "communication", 
                  "storage", "security", "integration", "monitoring"],
        },
        constraints | {
          type = "object",
          properties = {
            max_latency_ms | { type = "number" },
            min_throughput_rps | { type = "number" },
            required_regions | { 
              type = "array",
              items = { type = "string" },
            },
          },
        },
      },
      required = ["capability"],
    },
  },
  
  # Test server capabilities
  test_server | mcp.Tool & {
    name = "test_mcp_server",
    description = "Run validation tests on an MCP server",
    inputSchema = {
      type = "object",
      properties = {
        server_url | {
          type = "string",
          format = "uri",
        },
        test_suite | {
          type = "string",
          enum = ["basic", "full", "performance", "security"],
          default = "basic",
        },
        capability_tests | {
          type = "array",
          items = {
            type = "object",
            properties = {
              method | { type = "string" },
              params | { type = "object" },
              expected | { type = "object" },
            },
          },
        },
      },
      required = ["server_url"],
    },
  },
  
  # Generate configuration
  generate_config | mcp.Tool & {
    name = "generate_server_config",
    description = "Generate optimal configuration for an MCP server",
    inputSchema = {
      type = "object",
      properties = {
        server_metadata | {
          type = "object",
          description = "Server metadata from discovery",
        },
        requirements | {
          type = "object",
          description = "Capability requirements",
        },
        optimization_goal | {
          type = "string",
          enum = ["latency", "throughput", "reliability", "cost"],
          default = "latency",
        },
      },
      required = ["server_metadata", "requirements"],
    },
  },
  
  # Deploy configuration
  deploy_server | mcp.Tool & {
    name = "deploy_mcp_server",
    description = "Deploy and configure an MCP server connection",
    inputSchema = {
      type = "object",
      properties = {
        server | {
          type = "object",
          description = "Server metadata and configuration",
        },
        environment | {
          type = "string",
          enum = ["development", "staging", "production"],
          default = "development",
        },
        monitoring | {
          type = "boolean",
          default = true,
          description = "Enable monitoring and alerting",
        },
      },
      required = ["server"],
    },
  },
} in

# Example high-level capability specifications

let ExampleCapabilities = {
  # Need: "I need to analyze time series data"
  time_series_analysis | CapabilityRequirement & {
    category = 'Computation,
    functionality = "Analyze time series data with anomaly detection and forecasting",
    constraints = {
      latency_ms = 1000,
      throughput_rps = 100,
    },
    examples = [{
      input = {
        data = [1.0, 1.2, 1.1, 5.0, 1.3],  # 5.0 is anomaly
        method = "detect_anomalies",
      },
      expected_output = {
        anomalies = [{ index = 3, value = 5.0, score = 0.95 }],
      },
    }],
  },
  
  # Need: "I need to visualize graph structures"
  graph_visualization | CapabilityRequirement & {
    category = 'Visualization,
    functionality = "Render interactive graph visualizations with layout algorithms",
    constraints = {
      max_memory_mb = 2048,
    },
    priority = 'High,
  },
  
  # Need: "I need secure data storage"
  secure_storage | CapabilityRequirement & {
    category = 'Storage,
    functionality = "Store sensitive data with encryption at rest and in transit",
    constraints = {
      require_encryption = true,
      require_auth = true,
      allowed_regions = ["us-east", "eu-west"],
    },
    priority = 'Critical,
  },
} in

# Export the discovery system
{
  # Core types
  CapabilityCategory = CapabilityCategory,
  CapabilityRequirement = CapabilityRequirement,
  ServerMetadata = ServerMetadata,
  ServerConfiguration = ServerConfiguration,
  
  # Discovery and matching
  DiscoveryService = DiscoveryService,
  CapabilityMatcher = CapabilityMatcher,
  
  # Validation
  ValidationTest = ValidationTest,
  ValidationSuite = ValidationSuite,
  
  # Configuration
  ConfigurationWizard = ConfigurationWizard,
  
  # Provisioning
  ProvisioningPipeline = ProvisioningPipeline,
  
  # MCP tools
  tools = DiscoveryTools,
  
  # Example usage
  examples = ExampleCapabilities,
  
  # Main discovery function
  discover_and_provision = fun requirement => {
    # Create discovery service
    discovery_service = {
      methods = [
        'Registry { url = "https://mcp-registry.io/api/v1" },
        'DNS { domain = "mcp.local" },
      ],
      filters = {
        required_categories = [requirement.category],
        require_verified = requirement.priority == 'Critical,
      },
    },
    
    # Create provisioning pipeline
    pipeline = {
      stages = ['Discovery, 'Matching, 'Configuration, 'Validation, 'Deployment],
      execute = fun req =>
        # Simplified execution
        {
          status = 'Success,
          selected_server = null,
          configuration = null,
          errors = [],
        },
    },
    
    # Execute pipeline
    pipeline.execute requirement
  },
}