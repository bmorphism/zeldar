# MCP Capability Discovery Integration
# Practical examples of discovering and using real MCP servers

let discovery = import "capability-discovery.ncl" in
let mcp = import "lib-purist.ncl" in

# Real-world capability requirements
let real_world_requirements = {
  # Database access requirement
  database_access = discovery.CapabilityRequirement & {
    category = 'DataAccess,
    functionality = "Query and analyze structured data with SQL support",
    constraints = {
      latency_ms = 1000,
      throughput_rps = 500,
    },
    priority = 'High,
    examples = [{
      input = {
        query = "SELECT * FROM users WHERE created_at > '2024-01-01'",
      },
      expected_output = {
        rows = [],
        metadata = { count = 0 },
      },
    }],
  },
  
  # Code generation requirement
  code_generation = discovery.CapabilityRequirement & {
    category = 'Computation,
    functionality = "Generate code from natural language descriptions with syntax highlighting",
    constraints = {
      max_memory_mb = 4096,
    },
    priority = 'Medium,
  },
  
  # File system access requirement
  file_access = discovery.CapabilityRequirement & {
    category = 'DataAccess,
    functionality = "Read and write files with directory traversal and search",
    constraints = {
      require_auth = true,
    },
    priority = 'Critical,
  },
  
  # API integration requirement
  api_integration = discovery.CapabilityRequirement & {
    category = 'Integration,
    functionality = "Call external REST APIs with authentication and rate limiting",
    constraints = {
      latency_ms = 5000,
      require_encryption = true,
    },
    priority = 'High,
  },
} in

# Discovery results mapping to actual MCP servers
let discovered_real_servers = {
  # SQLite MCP Server
  sqlite_server = {
    name = "SQLite MCP Server",
    version = "1.0.0",
    url = "stdio://sqlite-mcp",
    
    capabilities = {
      categories = ['DataAccess],
      features = ["sql_queries", "database_management", "transactions"],
      api_version = "2024-11-05",
    },
    
    performance = {
      avg_latency_ms = 50,
      max_throughput_rps = 1000,
      uptime_percent = 99.99,
    },
    
    requirements = {
      supported_transports = ['Stdio],
    },
    
    # MCP server configuration
    mcp_config = mcp.MCPServer & {
      name = "sqlite-mcp",
      version = "1.0.0",
      transport = 'Stdio {
        command = "npx",
        args = ["-y", "@modelcontextprotocol/server-sqlite", "path/to/database.db"],
      },
      capabilities = {
        resources = { subscribe = false, listChanged = false },
        tools = { listChanged = false },
      },
      tools = [{
        name = "query",
        description = "Execute SQL query on the database",
        inputSchema = {
          type = "object",
          properties = {
            query = {
              type = "string",
              description = "SQL query to execute",
            },
          },
          required = ["query"],
        },
      }],
    },
  },
  
  # Filesystem MCP Server
  filesystem_server = {
    name = "Filesystem MCP Server",
    version = "1.0.0",
    url = "stdio://filesystem-mcp",
    
    capabilities = {
      categories = ['DataAccess],
      features = ["file_read", "file_write", "directory_listing", "search"],
      api_version = "2024-11-05",
    },
    
    trust = {
      verified = true,
      reputation_score = 0.95,
    },
    
    mcp_config = mcp.MCPServer & {
      name = "filesystem-mcp",
      version = "1.0.0",
      transport = 'Stdio {
        command = "npx",
        args = ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"],
      },
      capabilities = {
        resources = { subscribe = true, listChanged = true },
        tools = { listChanged = false },
      },
      resources = [{
        uri = "file:///allowed/path",
        name = "Allowed Directory",
        description = "Base directory for file operations",
        mimeType = "text/directory",
      }],
      tools = [
        {
          name = "read_file",
          description = "Read contents of a file",
          inputSchema = {
            type = "object",
            properties = {
              path = { type = "string" },
            },
            required = ["path"],
          },
        },
        {
          name = "write_file",
          description = "Write contents to a file",
          inputSchema = {
            type = "object",
            properties = {
              path = { type = "string" },
              content = { type = "string" },
            },
            required = ["path", "content"],
          },
        },
      ],
    },
  },
  
  # HTTP/Fetch MCP Server
  fetch_server = {
    name = "Fetch MCP Server",
    version = "1.0.0",
    url = "stdio://fetch-mcp",
    
    capabilities = {
      categories = ['Integration],
      features = ["http_requests", "api_calls", "rate_limiting"],
      api_version = "2024-11-05",
    },
    
    mcp_config = mcp.MCPServer & {
      name = "fetch-mcp",
      version = "1.0.0",
      transport = 'Stdio {
        command = "npx",
        args = ["-y", "@modelcontextprotocol/server-fetch"],
      },
      tools = [{
        name = "fetch",
        description = "Make HTTP requests to external APIs",
        inputSchema = {
          type = "object",
          properties = {
            url = { type = "string", format = "uri" },
            method = { 
              type = "string",
              enum = ["GET", "POST", "PUT", "DELETE", "PATCH"],
              default = "GET",
            },
            headers = { type = "object" },
            body = { type = "string" },
          },
          required = ["url"],
        },
      }],
    },
  },
} in

# Automated configuration generation
let auto_configs = {
  # Generate config for SQLite server
  sqlite_config = discovery.ConfigurationWizard.generate_config 
    real_world_requirements.database_access
    discovered_real_servers.sqlite_server,
  
  # Generate config for filesystem server
  filesystem_config = discovery.ConfigurationWizard.generate_config
    real_world_requirements.file_access
    discovered_real_servers.filesystem_server,
} in

# Composite server configuration for multiple capabilities
let composite_server_config = {
  # Combine multiple servers for comprehensive capabilities
  name = "Research Platform Composite",
  servers = {
    database = discovered_real_servers.sqlite_server.mcp_config,
    filesystem = discovered_real_servers.filesystem_server.mcp_config,
    api = discovered_real_servers.fetch_server.mcp_config,
  },
  
  # Routing rules to direct requests to appropriate servers
  routing = {
    rules = [
      {
        pattern = "sql:*",
        target = "database",
        method = "query",
      },
      {
        pattern = "file:*", 
        target = "filesystem",
        method = "auto",  # Automatically choose read/write
      },
      {
        pattern = "https:*",
        target = "api",
        method = "fetch",
      },
    ],
  },
  
  # Unified capabilities
  combined_capabilities = {
    resources = {
      subscribe = true,
      listChanged = true,
    },
    tools = {
      listChanged = false,
    },
  },
} in

# Practical usage examples
let usage_examples = {
  # Example 1: Discover database server
  discover_database = {
    requirement = real_world_requirements.database_access,
    discovery_result = discovered_real_servers.sqlite_server,
    
    # Generated MCP client configuration
    client_config = {
      servers = {
        sqlite = {
          command = "npx",
          args = ["-y", "@modelcontextprotocol/server-sqlite", "./research.db"],
        },
      },
    },
    
    # Example usage after discovery
    example_usage = {
      initialize = mcp.builders.request "initialize" {
        protocolVersion = mcp.LATEST_PROTOCOL_VERSION,
        capabilities = {},
        clientInfo = {
          name = "research-client",
          version = "1.0.0",
        },
      },
      
      query_data = mcp.builders.request "tools/call" {
        name = "query",
        arguments = {
          query = "SELECT neuron_id, type FROM neurons WHERE type = 'Motor'",
        },
      },
    },
  },
  
  # Example 2: Setup multi-server environment
  multi_server_setup = {
    requirements = [
      real_world_requirements.database_access,
      real_world_requirements.file_access,
      real_world_requirements.api_integration,
    ],
    
    # Discovered servers
    servers = [
      discovered_real_servers.sqlite_server,
      discovered_real_servers.filesystem_server, 
      discovered_real_servers.fetch_server,
    ],
    
    # Combined configuration for Claude Desktop or similar MCP client
    mcp_config_json = {
      mcpServers = {
        sqlite = {
          command = "npx",
          args = ["-y", "@modelcontextprotocol/server-sqlite", "./research.db"],
        },
        filesystem = {
          command = "npx",
          args = ["-y", "@modelcontextprotocol/server-filesystem", "./research-data"],
        },
        fetch = {
          command = "npx",
          args = ["-y", "@modelcontextprotocol/server-fetch"],
          config = {
            rateLimiting = {
              maxRequestsPerMinute = 60,
            },
          },
        },
      },
    },
  },
} in

# Discovery workflow for CLI integration
let cli_discovery_workflow = {
  # Step 1: List available capabilities
  list_capabilities = "mcp-discover list-categories",
  
  # Step 2: Search for servers by capability
  search_servers = "mcp-discover search --category DataAccess --features sql",
  
  # Step 3: Test server
  test_server = "mcp-discover test --server sqlite-mcp --suite basic",
  
  # Step 4: Generate config
  generate_config = "mcp-discover configure --server sqlite-mcp --output mcp-config.json",
  
  # Step 5: Install and run
  install_and_run = [
    "npm install -g @modelcontextprotocol/server-sqlite",
    "mcp-server-sqlite ./database.db",
  ],
} in

# Export the integration examples
{
  # Real-world requirements
  requirements = real_world_requirements,
  
  # Discovered servers
  servers = discovered_real_servers,
  
  # Configurations
  auto_configs = auto_configs,
  composite_config = composite_server_config,
  
  # Usage examples
  examples = usage_examples,
  
  # CLI workflow
  cli_workflow = cli_discovery_workflow,
  
  # Quick start guide
  quick_start = {
    description = "Get started with MCP capability discovery",
    
    steps = [
      "1. Define your capability requirements",
      "2. Run discovery to find matching servers", 
      "3. Test and validate server capabilities",
      "4. Generate optimal configuration",
      "5. Deploy and start using the servers",
    ],
    
    example_command = "nickel eval discovery-integration.ncl --field examples.discover_database",
  },
}