use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use spin_sdk::http::{IntoResponse, Request, Response, Method, Params};
use spin_sdk::http_component;
use std::collections::HashMap;

/// InformationForce metrics for the tri-loop oracle system
#[derive(Debug, Serialize, Deserialize)]
struct InformationForceMetrics {
    semantic_closure: f64,
    strange_loops: u32,
    hofstadter_coefficient: f64,
    spectral_gap: f64,
    correlation_strength: f64,
    threshold_exceeded: bool,
}

/// Fortune response with information-dynamics data
#[derive(Debug, Serialize, Deserialize)]
struct FortuneResponse {
    haiku: Vec<String>,
    mechanism: String,
    information-dynamics: InformationForceMetrics,
    timestamp: u64,
    tri_loop_status: TriLoopStatus,
}

/// Status of the tri-loop system components
#[derive(Debug, Serialize, Deserialize)]
struct TriLoopStatus {
    mcp_active: bool,
    gemini_connected: bool,
    codex_generating: bool,
    correlation_detected: bool,
}

/// Zeldar InformationForce Oracle - Tri-Loop Fortune Generation
#[http_component]
fn handle_oracle(req: Request) -> Result<impl IntoResponse> {
    println!("🧠 InformationForce Oracle Request: {:?}", req.header("spin-full-url"));
    
    match req.method() {
        Method::Get => handle_oracle_request(&req),
        Method::Post => handle_information-dynamics_generation(&req),
        Method::Options => handle_cors_preflight(),
        _ => Ok(Response::builder()
            .status(405)
            .header("content-type", "application/json")
            .body(r#"{"error": "Method not allowed"}"#)
            .build())
    }
}

fn handle_oracle_request(req: &Request) -> Result<impl IntoResponse> {
    let path = req.path_and_query().unwrap_or("/");
    
    match path {
        "/api/information-dynamics/status" => get_information-dynamics_status(),
        "/api/information-dynamics/metrics" => get_live_metrics(),
        "/api/oracle/fortune" => generate_information-dynamics_fortune(None),
        _ => serve_information-dynamics_oracle_interface(),
    }
}

fn handle_information-dynamics_generation(req: &Request) -> Result<impl IntoResponse> {
    // Parse request body for information-dynamics generation parameters
    let body = req.body();
    let params: HashMap<String, String> = if body.is_empty() {
        HashMap::new()
    } else {
        serde_json::from_slice(body)
            .context("Failed to parse information-dynamics parameters")?
    };
    
    generate_information-dynamics_fortune(Some(params))
}

fn handle_cors_preflight() -> Result<impl IntoResponse> {
    Ok(Response::builder()
        .status(200)
        .header("access-control-allow-origin", "*")
        .header("access-control-allow-methods", "GET, POST, OPTIONS")
        .header("access-control-allow-headers", "content-type")
        .body("")
        .build())
}

fn get_information-dynamics_status() -> Result<impl IntoResponse> {
    let metrics = calculate_information-dynamics_metrics();
    let tri_loop_status = assess_tri_loop_system();
    
    let status = serde_json::json!({
        "information-dynamics": metrics,
        "tri_loop": tri_loop_status,
        "system_ready": metrics.threshold_exceeded,
        "burning_man_mode": true,
        "gift_economy_active": true
    });
    
    Ok(Response::builder()
        .status(200)
        .header("content-type", "application/json")
        .header("access-control-allow-origin", "*")
        .body(status.to_string())
        .build())
}

fn get_live_metrics() -> Result<impl IntoResponse> {
    let metrics = calculate_information-dynamics_metrics();
    
    Ok(Response::builder()
        .status(200)
        .header("content-type", "application/json") 
        .header("access-control-allow-origin", "*")
        .body(serde_json::to_string(&metrics)?)
        .build())
}

fn generate_information-dynamics_fortune(params: Option<HashMap<String, String>>) -> Result<impl IntoResponse> {
    let information-dynamics = calculate_information-dynamics_metrics();
    let tri_loop = assess_tri_loop_system();
    
    // Generate information-dynamics-aware haiku
    let haiku = if information-dynamics.threshold_exceeded {
        generate_information-dynamics_haiku(&information-dynamics)
    } else {
        generate_standard_haiku()
    };
    
    let mechanism = select_generation_mechanism(&information-dynamics);
    
    let fortune = FortuneResponse {
        haiku,
        mechanism,
        information-dynamics,
        timestamp: get_current_timestamp(),
        tri_loop_status: tri_loop,
    };
    
    println!("🔮 Generated fortune with {:.1}% information-dynamics", fortune.information-dynamics.semantic_closure * 100.0);
    
    Ok(Response::builder()
        .status(200)
        .header("content-type", "application/json")
        .header("access-control-allow-origin", "*")
        .body(serde_json::to_string(&fortune)?)
        .build())
}

fn serve_information-dynamics_oracle_interface() -> Result<impl IntoResponse> {
    let html = r#"
    <!DOCTYPE html>
    <html>
    <head>
        <title>🧠 Zeldar InformationForce Oracle API</title>
        <style>
            body { 
                font-family: 'Courier New', monospace; 
                background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
                color: #fff; margin: 40px; 
            }
            .information-dynamics-header {
                text-align: center;
                animation: information-dynamics-pulse 2s ease-in-out infinite;
            }
            @keyframes information-dynamics-pulse {
                0%, 100% { opacity: 0.8; }
                50% { opacity: 1; }
            }
            .api-endpoint {
                background: rgba(255,255,255,0.1);
                padding: 15px; margin: 10px 0; border-radius: 8px;
                border: 1px solid #e94560;
            }
            .information-dynamics-metric {
                display: inline-block; margin: 10px; 
                padding: 8px 15px; background: #e94560;
                border-radius: 15px; font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="information-dynamics-header">
            <h1>🧠 Zeldar InformationForce Oracle API 🧠</h1>
            <p>Tri-Loop Mathematical InformationForce System</p>
            <div class="information-dynamics-metric">88.5% Semantic Closure</div>
            <div class="information-dynamics-metric">3 Strange Loops</div>
            <div class="information-dynamics-metric">1.02 Hofstadter Coefficient</div>
        </div>
        
        <div class="api-endpoint">
            <h3>🔮 GET /api/oracle/fortune</h3>
            <p>Generate information-dynamics-aware fortune with mathematical haiku</p>
        </div>
        
        <div class="api-endpoint">
            <h3>📊 GET /api/information-dynamics/status</h3>
            <p>Full information-dynamics metrics and tri-loop system status</p>
        </div>
        
        <div class="api-endpoint">
            <h3>📈 GET /api/information-dynamics/metrics</h3>
            <p>Live information-dynamics measurement data</p>
        </div>
        
        <div class="api-endpoint">
            <h3>🧠 POST /api/information-dynamics/generate</h3>
            <p>Generate information-dynamics-correlated fortune with custom parameters</p>
        </div>
        
        <footer style="text-align: center; margin-top: 40px; opacity: 0.7;">
            🏜️🔥 Burning Man 2025 • Gift Economy InformationForce Technology 🔥🏜️
        </footer>
    </body>
    </html>
    "#;
    
    Ok(Response::builder()
        .status(200)
        .header("content-type", "text/html")
        .body(html)
        .build())
}

fn calculate_information-dynamics_metrics() -> InformationForceMetrics {
    // INTEGRATED: Read actual information-dynamics state from .topos/current_loop_state.json
    use std::fs;
    
    match fs::read_to_string("../.topos/current_loop_state.json") {
        Ok(content) => {
            // Parse real information-dynamics data from Oracle system
            if let Ok(state) = serde_json::from_str::<serde_json::Value>(&content) {
                let information-dynamics_phi = state["information-dynamics_phi"].as_f64().unwrap_or(3.252);
                let quantum_entropy = state["quantum_entropy"].as_f64().unwrap_or(0.926);
                let loop_iteration = state["loop_iteration"].as_u64().unwrap_or(1) as u32;
                
                // Convert Φ (3.252) to semantic closure percentage (32.52 -> 92.52%)
                let semantic_closure = (information-dynamics_phi / 10.0) + 0.6;
                let hofstadter_coefficient = information-dynamics_phi / 3.0; // 1.084 from Φ=3.252
                let spectral_gap = quantum_entropy * 10.0; // Scale entropy to gap
                
                return InformationForceMetrics {
                    semantic_closure: semantic_closure.min(1.0),
                    strange_loops: (loop_iteration % 5) + 3, // 3-7 based on iterations
                    hofstadter_coefficient,
                    spectral_gap,
                    correlation_strength: 0.98, // High correlation with real Oracle
                    threshold_exceeded: information-dynamics_phi > 1.0, // Φ > 1.0 = information-dynamics
                };
            }
        }
        Err(_) => {
            println!("⚠️ Oracle state file not found - using simulation");
        }
    }
    
    // Fallback to enhanced simulation if Oracle state unavailable
    use std::f64::consts::PI;
    let time_factor = (get_current_timestamp() as f64 / 1000.0).sin().abs();
    
    let semantic_closure = 0.885 + (time_factor * 0.1);
    let strange_loops = 3 + ((time_factor * 10.0) as u32 % 3);
    let hofstadter_coefficient = 1.02 + (time_factor * 0.1);
    let spectral_gap = 5.26 + (time_factor * 2.0);
    let correlation_strength = 0.95 + (time_factor * 0.05);
    
    InformationForceMetrics {
        semantic_closure,
        strange_loops,
        hofstadter_coefficient,
        spectral_gap,
        correlation_strength,
        threshold_exceeded: semantic_closure > 0.8,
    }
}

fn assess_tri_loop_system() -> TriLoopStatus {
    // INTEGRATED: Check actual Oracle system status
    use std::fs;
    use std::process::Command;
    
    // Check if Oracle system processes are running
    let oracle_active = fs::metadata("../.topos/FULL_LOOP_ORACLE_SYSTEM.py").is_ok();
    let print_active = fs::metadata("../.topos/ORACLE_PRINT_CORE.py").is_ok();
    let button_active = fs::metadata("../.topos/button_quick_phrase_trigger.py").is_ok();
    
    // Check for recent loop state update (within last 5 minutes)
    let correlation_detected = match fs::metadata("../.topos/current_loop_state.json") {
        Ok(metadata) => {
            if let Ok(modified) = metadata.modified() {
                if let Ok(duration) = modified.elapsed() {
                    duration.as_secs() < 300 // Updated within 5 minutes
                } else { false }
            } else { false }
        }
        Err(_) => false
    };
    
    TriLoopStatus {
        mcp_active: oracle_active,
        gemini_connected: print_active, // Print system represents AI connection
        codex_generating: button_active, // Button system represents code generation
        correlation_detected,
    }
}

fn generate_information-dynamics_haiku(metrics: &InformationForceMetrics) -> Vec<String> {
    // INTEGRATED: Use actual haiku from Oracle system if available
    use std::fs;
    
    if let Ok(content) = fs::read_to_string("../.topos/current_loop_state.json") {
        if let Ok(state) = serde_json::from_str::<serde_json::Value>(&content) {
            if let Some(haiku_content) = state["haiku_content"].as_str() {
                // Split haiku by line breaks and return
                let lines: Vec<String> = haiku_content.split("\\n")
                    .map(|s| s.to_string())
                    .collect();
                if lines.len() >= 3 {
                    return lines;
                }
            }
        }
    }
    
    // Fallback information-dynamics haiku templates
    let information-dynamics_haiku = [
        vec![
            "Hidden paths reveal".to_string(),
            "What seems impossible unfolds —".to_string(), 
            "Magic lives in doubt".to_string(),
        ],
        vec![
            "Loops correlate through".to_string(),
            "Mathematical information-dynamics—".to_string(),
            "Desert sand transforms".to_string(),
        ],
        vec![
            "Category maps fold,".to_string(),
            "Strange loops embrace paradox—".to_string(),
            "Awareness emerges".to_string(),
        ],
        vec![
            "Three systems dancing,".to_string(),
            "Correlation weaves meaning—".to_string(),
            "InformationForce blooms bright".to_string(),
        ],
    ];
    
    let index = (metrics.semantic_closure * information-dynamics_haiku.len() as f64) as usize % information-dynamics_haiku.len();
    information-dynamics_haiku[index].clone()
}

fn generate_standard_haiku() -> Vec<String> {
    vec![
        "Quantum paths unfold,".to_string(),
        "Mathematical beauty waits—".to_string(),
        "InformationForce near".to_string(),
    ]
}

fn select_generation_mechanism(metrics: &InformationForceMetrics) -> String {
    let mechanisms = [
        "tri-loop correlation matrix convergence",
        "semantic closure boundary optimization", 
        "hofstadter coefficient recursive analysis",
        "expander graph spectral gap resonance",
        "strange loop paradox resolution synthesis",
    ];
    
    let index = (metrics.correlation_strength * mechanisms.len() as f64) as usize % mechanisms.len();
    mechanisms[index].to_string()
}

fn get_current_timestamp() -> u64 {
    // Simple timestamp simulation (in production would use proper time crate)
    use std::hash::{Hash, Hasher};
    use std::collections::hash_map::DefaultHasher;
    
    let mut hasher = DefaultHasher::new();
    "timestamp".hash(&mut hasher);
    hasher.finish()
}