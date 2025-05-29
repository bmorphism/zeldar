#!/bin/bash
# Run MCP Capability Discovery Demo
# Shows how to discover and provision servers based on high-level needs

set -euo pipefail

echo "🔍 MCP Capability Discovery System Demo"
echo "======================================"
echo

# Function to run Nickel evaluation
run_nickel() {
    local file=$1
    local expr=$2
    echo "Evaluating: $expr"
    nickel eval "$file" --field "$expr" 2>/dev/null || {
        echo "Error evaluating $expr"
        return 1
    }
}

# Function to pretty print JSON
pretty_json() {
    if command -v jq &> /dev/null; then
        jq .
    else
        cat
    fi
}

echo "📋 Step 1: Define High-Level Requirements"
echo "-----------------------------------------"
echo "Example: 'I need to analyze heterophilic properties of neural networks'"
echo

echo "🔎 Step 2: Discover Available Servers"
echo "------------------------------------"
run_nickel capability-demo.ncl "discovered_servers" | pretty_json
echo

echo "🎯 Step 3: Match Requirements to Servers"
echo "---------------------------------------"
run_nickel capability-demo.ncl "match_results" | pretty_json
echo

echo "⚙️  Step 4: Generate Optimal Configurations"
echo "------------------------------------------"
run_nickel capability-demo.ncl "generated_configs.neurograph_config" | pretty_json
echo

echo "✅ Step 5: Validate Server Capabilities"
echo "--------------------------------------"
run_nickel capability-demo.ncl "validation_suite.neurograph_tests" | pretty_json
echo

echo "🚀 Step 6: Provision and Deploy"
echo "------------------------------"
run_nickel capability-demo.ncl "provisioning_results.neuroscience_platform" | pretty_json
echo

echo "📊 Summary: Provisioned Services"
echo "-------------------------------"
echo "✓ Compute: NeuroGraph Engine (heterophily analysis)"
echo "✓ Visualization: NeuroVis 3D (interactive rendering)"  
echo "✓ Storage: BioStor Secure (encrypted experiment data)"
echo "✓ Monitoring: Grafana dashboards configured"
echo

echo "🎉 Discovery and provisioning complete!"
echo
echo "Next steps:"
echo "1. Set environment variables for authentication"
echo "2. Run validation tests on provisioned servers"
echo "3. Start using the servers through MCP protocol"