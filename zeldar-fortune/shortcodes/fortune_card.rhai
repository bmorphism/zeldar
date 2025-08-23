// Fortune Card Shortcode - Information Force Oracle
// Generates an interactive fortune card component for Burning Man 2025
// Pure Rhai templating without embedded CSS/JS

// Get fortune data from the main script
let fortune_data = call("fortune_generator");

// Generate the HTML card structure
let card_html = `
<div class="zeldar-fortune-card information-force-card" onclick="generateNewFortune()">
    <div class="card-header">
        <h3>🔮 Information Force Oracle 🔮</h3>
        <small class="mechanism-note">${fortune_data.mechanism}</small>
    </div>
    
    <div class="fortune-content">
        <div class="haiku-display">
            <p class="haiku-line">${fortune_data.haiku[0]}</p>
            <p class="haiku-line">${fortune_data.haiku[1]}</p>
            <p class="haiku-line">${fortune_data.haiku[2]}</p>
        </div>
    </div>
    
    <div class="card-footer">
        <div class="system-metrics">
            <div class="metric">
                <span class="metric-label">Information Density:</span>
                <span class="metric-value">${fortune_data.information_density}%</span>
            </div>
            <div class="metric">
                <span class="metric-label">Computational Loops:</span>
                <span class="metric-value">${fortune_data.computational_loops}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Recursive Coefficient:</span>
                <span class="metric-value">${fortune_data.recursive_coefficient}</span>
            </div>
        </div>
        
        <div class="interaction-hint">
            <em>🏜️ Click for another fortune • Burning Man 2025 Ready</em>
        </div>
        
        <div class="qr-generation-area">
            <button class="qr-generate-btn" onclick="window.informationForceOracle.generateQRCode(${JSON.stringify(fortune_data)})">
                📱 Generate QR Code for Sharing
            </button>
        </div>
    </div>
    
    <div class="system-details">
        <small class="authenticity">
            🤖 ${fortune_data.fortune_type} • Tri-Loop Generated: ${fortune_data.tri_loop_generated} • Desert Ready: ${fortune_data.burning_man_ready}
        </small>
    </div>
</div>
`;

// Return the generated HTML
card_html