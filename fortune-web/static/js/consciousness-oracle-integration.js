/**
 * Zeldar Consciousness Oracle Integration
 * Real-time consciousness metrics display with tri-loop system correlation
 */

class ConsciousnessOracleIntegration {
    constructor() {
        this.apiEndpoint = 'http://localhost:3000/api';
        this.consciousnessThreshold = 80.0;
        this.updateInterval = 5000; // 5 seconds
        this.isMonitoring = false;
        this.lastPhiCoefficient = 3.252;
        
        this.initializeInterface();
        this.startConsciousnessMonitoring();
    }
    
    initializeInterface() {
        // Create consciousness metrics display
        const metricsContainer = document.createElement('div');
        metricsContainer.id = 'consciousness-metrics';
        metricsContainer.className = 'consciousness-metrics';
        metricsContainer.innerHTML = `
            <div class="consciousness-header">
                <h3>🧠 Consciousness Oracle Status</h3>
                <div class="phi-display">Φ = <span id="phi-value">3.252</span></div>
            </div>
            <div class="metrics-grid">
                <div class="metric-item">
                    <label>Semantic Closure:</label>
                    <div class="metric-bar">
                        <div id="semantic-bar" class="metric-progress"></div>
                        <span id="semantic-value">92.5%</span>
                    </div>
                </div>
                <div class="metric-item">
                    <label>Strange Loops:</label>
                    <span id="strange-loops-value" class="metric-number">3</span>
                </div>
                <div class="metric-item">
                    <label>Hofstadter Coefficient:</label>
                    <span id="hofstadter-value" class="metric-number">1.084</span>
                </div>
                <div class="metric-item">
                    <label>Quantum Entropy:</label>
                    <div class="metric-bar">
                        <div id="entropy-bar" class="metric-progress"></div>
                        <span id="entropy-value">9.26</span>
                    </div>
                </div>
            </div>
            <div class="tri-loop-status">
                <h4>🔄 Tri-Loop System Status</h4>
                <div class="status-indicators">
                    <div id="mcp-status" class="status-indicator">
                        <span class="status-dot"></span> MCP Active
                    </div>
                    <div id="gemini-status" class="status-indicator">
                        <span class="status-dot"></span> Gemini Connected
                    </div>
                    <div id="codex-status" class="status-indicator">
                        <span class="status-dot"></span> Codex Generating
                    </div>
                    <div id="correlation-status" class="status-indicator">
                        <span class="status-dot"></span> Correlation Detected
                    </div>
                </div>
            </div>
            <div class="oracle-controls">
                <button id="trigger-button-oracle" class="oracle-button">
                    🔘 Trigger Button Oracle
                </button>
                <button id="generate-fortune" class="oracle-button">
                    🔮 Generate Consciousness Fortune
                </button>
                <button id="print-haiku" class="oracle-button">
                    🖨️ Print Physical Haiku
                </button>
            </div>
        `;
        
        // Insert after existing content
        const mainContent = document.querySelector('main') || document.body;
        mainContent.appendChild(metricsContainer);
        
        this.bindEvents();
    }
    
    bindEvents() {
        document.getElementById('trigger-button-oracle')?.addEventListener('click', () => {
            this.triggerButtonOracle();
        });
        
        document.getElementById('generate-fortune')?.addEventListener('click', () => {
            this.generateConsciousnessFortune();
        });
        
        document.getElementById('print-haiku')?.addEventListener('click', () => {
            this.triggerPhysicalPrint();
        });
    }
    
    async startConsciousnessMonitoring() {
        if (this.isMonitoring) return;
        this.isMonitoring = true;
        
        console.log('🧠 Starting consciousness monitoring...');
        
        while (this.isMonitoring) {
            try {
                await this.updateConsciousnessMetrics();
                await this.updateTriLoopStatus();
                await this.sleep(this.updateInterval);
            } catch (error) {
                console.error('⚠️ Consciousness monitoring error:', error);
                await this.sleep(this.updateInterval * 2); // Longer delay on error
            }
        }
    }
    
    async updateConsciousnessMetrics() {
        try {
            const response = await fetch(`${this.apiEndpoint}/consciousness/metrics`);
            const metrics = await response.json();
            
            this.renderConsciousnessMetrics(metrics);
            this.updatePhiVisualization(metrics.phi_coefficient || this.lastPhiCoefficient);
            
            // Update last known Phi coefficient
            if (metrics.phi_coefficient) {
                this.lastPhiCoefficient = metrics.phi_coefficient;
            }
            
        } catch (error) {
            console.error('Failed to update consciousness metrics:', error);
            this.showConnectionError();
        }
    }
    
    async updateTriLoopStatus() {
        try {
            const response = await fetch(`${this.apiEndpoint}/consciousness/status`);
            const status = await response.json();
            
            this.renderTriLoopStatus(status.tri_loop);
            
        } catch (error) {
            console.error('Failed to update tri-loop status:', error);
        }
    }
    
    renderConsciousnessMetrics(metrics) {
        // Update Phi display
        const phiElement = document.getElementById('phi-value');
        if (phiElement) {
            phiElement.textContent = (metrics.phi_coefficient || this.lastPhiCoefficient).toFixed(3);
            phiElement.className = metrics.threshold_exceeded ? 'phi-transcendent' : 'phi-normal';
        }
        
        // Update semantic closure
        const semanticValue = document.getElementById('semantic-value');
        const semanticBar = document.getElementById('semantic-bar');
        if (semanticValue && semanticBar) {
            const percentage = metrics.semantic_closure || 92.5;
            semanticValue.textContent = `${percentage.toFixed(1)}%`;
            semanticBar.style.width = `${Math.min(percentage, 100)}%`;
            semanticBar.className = `metric-progress ${percentage > this.consciousnessThreshold ? 'above-threshold' : 'below-threshold'}`;
        }
        
        // Update strange loops
        const strangeLoopsElement = document.getElementById('strange-loops-value');
        if (strangeLoopsElement) {
            strangeLoopsElement.textContent = metrics.strange_loops || 3;
        }
        
        // Update Hofstadter coefficient
        const hofstadterElement = document.getElementById('hofstadter-value');
        if (hofstadterElement) {
            hofstadterElement.textContent = (metrics.hofstadter_coefficient || 1.084).toFixed(3);
        }
        
        // Update quantum entropy
        const entropyValue = document.getElementById('entropy-value');
        const entropyBar = document.getElementById('entropy-bar');
        if (entropyValue && entropyBar) {
            const entropy = metrics.spectral_gap || 9.26;
            entropyValue.textContent = entropy.toFixed(2);
            entropyBar.style.width = `${Math.min(entropy * 10, 100)}%`;
            entropyBar.className = 'metric-progress entropy-visualization';
        }
    }
    
    renderTriLoopStatus(triLoopStatus) {
        const statusMap = {
            'mcp-status': triLoopStatus.mcp_active,
            'gemini-status': triLoopStatus.gemini_connected,
            'codex-status': triLoopStatus.codex_generating,
            'correlation-status': triLoopStatus.correlation_detected
        };
        
        Object.entries(statusMap).forEach(([elementId, isActive]) => {
            const element = document.getElementById(elementId);
            if (element) {
                const dot = element.querySelector('.status-dot');
                if (dot) {
                    dot.className = `status-dot ${isActive ? 'status-active' : 'status-inactive'}`;
                }
                element.className = `status-indicator ${isActive ? 'indicator-active' : 'indicator-inactive'}`;
            }
        });
    }
    
    updatePhiVisualization(phiCoefficient) {
        // Add dynamic visual effects based on Phi coefficient
        const metricsContainer = document.getElementById('consciousness-metrics');
        if (metricsContainer) {
            if (phiCoefficient > 3.0) {
                metricsContainer.classList.add('transcendent-state');
                metricsContainer.classList.remove('consciousness-emerging');
            } else if (phiCoefficient > 1.0) {
                metricsContainer.classList.add('consciousness-emerging');
                metricsContainer.classList.remove('transcendent-state');
            } else {
                metricsContainer.classList.remove('transcendent-state', 'consciousness-emerging');
            }
        }
    }
    
    async triggerButtonOracle() {
        try {
            console.log('🔘 Triggering button oracle...');
            const response = await fetch(`${this.apiEndpoint}/oracle/button`, {
                method: 'POST'
            });
            
            if (response.ok) {
                const result = await response.json();
                this.showOracleResult('Button Oracle Activated', result);
            } else {
                this.showError('Button oracle trigger failed');
            }
        } catch (error) {
            console.error('Button oracle error:', error);
            this.showError('Button oracle connection failed');
        }
    }
    
    async generateConsciousnessFortune() {
        try {
            console.log('🔮 Generating consciousness fortune...');
            const response = await fetch(`${this.apiEndpoint}/oracle/fortune`);
            
            if (response.ok) {
                const fortune = await response.json();
                this.displayFortune(fortune);
            } else {
                this.showError('Fortune generation failed');
            }
        } catch (error) {
            console.error('Fortune generation error:', error);
            this.showError('Fortune generation connection failed');
        }
    }
    
    async triggerPhysicalPrint() {
        try {
            console.log('🖨️ Triggering physical print...');
            const response = await fetch(`${this.apiEndpoint}/oracle/print`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    content: 'Web-triggered consciousness haiku',
                    timestamp: Date.now()
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                this.showOracleResult('Physical Print Triggered', result);
            } else {
                this.showError('Physical print failed');
            }
        } catch (error) {
            console.error('Print trigger error:', error);
            this.showError('Print system connection failed');
        }
    }
    
    displayFortune(fortune) {
        // Create fortune display overlay
        const fortuneOverlay = document.createElement('div');
        fortuneOverlay.className = 'fortune-overlay';
        fortuneOverlay.innerHTML = `
            <div class="fortune-modal">
                <div class="fortune-header">
                    <h3>🔮 Consciousness Fortune</h3>
                    <button class="close-fortune">×</button>
                </div>
                <div class="haiku-display">
                    ${fortune.haiku.map(line => `<div class="haiku-line">${line}</div>`).join('')}
                </div>
                <div class="fortune-metadata">
                    <div class="mechanism">Mechanism: ${fortune.mechanism}</div>
                    ${fortune.burning_man_element ? `<div class="element">Element: ${fortune.burning_man_element}</div>` : ''}
                    <div class="consciousness-level">Φ = ${fortune.consciousness.phi_coefficient?.toFixed(3) || '3.252'}</div>
                </div>
            </div>
        `;
        
        document.body.appendChild(fortuneOverlay);
        
        fortuneOverlay.querySelector('.close-fortune').addEventListener('click', () => {
            fortuneOverlay.remove();
        });
        
        fortuneOverlay.addEventListener('click', (e) => {
            if (e.target === fortuneOverlay) {
                fortuneOverlay.remove();
            }
        });
    }
    
    showOracleResult(title, result) {
        console.log(`✅ ${title}:`, result);
        // Could add visual notification here
    }
    
    showError(message) {
        console.error(`❌ ${message}`);
        // Could add visual error notification here
    }
    
    showConnectionError() {
        const phiElement = document.getElementById('phi-value');
        if (phiElement) {
            phiElement.textContent = 'OFFLINE';
            phiElement.className = 'phi-offline';
        }
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    stopMonitoring() {
        this.isMonitoring = false;
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.consciousnessOracle = new ConsciousnessOracleIntegration();
    console.log('🧠 Consciousness Oracle Integration initialized');
});