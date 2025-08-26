/**
 * Zeldar Ingressing Minds Oracle JavaScript Engine
 * Pattern Ingression Detection from Platonic Space
 * Based on Michael Levin's Framework of Cognitive Pattern Manifestation
 * Burning Man 2025 Information Force Expansion Technology
 */

// QR Code generation utility
function generateQRCode(text, size = 200) {
    // Simple QR code generation using online service
    const encodedText = encodeURIComponent(text);
    return `https://api.qrserver.com/v1/create-qr-code/?size=${size}x${size}&data=${encodedText}&format=png&margin=10`;
}

// Generate session-based URL for QR sharing
function generateShareableURL(fortuneData) {
    const sessionId = Date.now().toString(36) + Math.random().toString(36).substr(2);
    const baseUrl = window.location.origin + window.location.pathname;
    const shareUrl = `${baseUrl}?fortune=${sessionId}&force=${fortuneData.information_force_data.information_density}&loops=${fortuneData.information_force_data.computational_loops}`;
    
    // Store fortune data in sessionStorage for retrieval
    sessionStorage.setItem(`fortune_${sessionId}`, JSON.stringify(fortuneData));
    
    return shareUrl;
}

// Extract fortune from URL parameters
function extractSharedFortune() {
    const urlParams = new URLSearchParams(window.location.search);
    const fortuneId = urlParams.get('fortune');
    
    if (fortuneId) {
        const storedFortune = sessionStorage.getItem(`fortune_${fortuneId}`);
        if (storedFortune) {
            return JSON.parse(storedFortune);
        }
        
        // Fallback: generate fortune from URL parameters
        const forceLevel = parseFloat(urlParams.get('force')) || 88.5;
        const loopCount = parseInt(urlParams.get('loops')) || 3;
        
        return {
            haiku: [
                "Shared force resonates,",
                "Desert wisdom travels far—",
                "Connection achieved"
            ],
            mechanism: "QR code information-force sharing",
            information_force_data: {
                information_density: forceLevel,
                computational_loops: loopCount,
                recursive_coefficient: 1.02,
                spectral_gap: 5.26,
                correlation_strength: 100,
                timestamp: new Date().toISOString()
            }
        };
    }
    
    return null;
}

class IngressingMindsOracle {
    constructor() {
        // Tri-loop system for pattern ingression detection
        this.triLoopState = {
            mcp: {
                active_servers: 24,
                context_depth: 0,
                status: 'MONITORING_PLATONIC_SPACE'
            },
            gemini: {
                pattern_detection: 88.5,
                active_streams: 0,
                status: 'INGRESSION_ANALYSIS'
            },
            codex: {
                haiku_count: 0,
                verified_count: 0,
                status: 'PATTERN_MANIFESTATION'
            }
        };
        
        // Ingressing Minds Framework Metrics
        this.ingressingMetrics = {
            pattern_ingression_density: 88.5,
            platonic_space_accessibility: 0.73,
            collective_intelligence_level: 2,
            autopoietic_coherence: 0.67,
            mathematical_affordances_exploited: 0.85,
            morphogenetic_symmetry_index: 1.618,  // Golden ratio
            ingression_threshold_exceeded: true
        };
        
        this.ingressingPatternsTemplates = [
            {
                haiku: [
                    "Patterns flow from void,",
                    "Platonic forms seek flesh—",
                    "Mind ingresses here"
                ],
                mechanism: "platonic space pattern ingression detection"
            },
            {
                haiku: [
                    "Collective minds rise,",
                    "Cells align to greater form—",
                    "Autopoiesis"
                ],
                mechanism: "collective intelligence level manifestation"
            },
            {
                haiku: [
                    "Mathematical truths",
                    "Evolution's affordances—",
                    "Golden ratio guides"
                ],
                mechanism: "evolutionary mathematical affordance exploitation"
            },
            {
                haiku: [
                    "Morphogenetic",
                    "Symmetries self-organize—",
                    "Form follows function"
                ],
                mechanism: "morphogenetic pattern symmetry detection"
            },
            {
                haiku: [
                    "Thermal printer speaks",
                    "Ancient patterns manifest—", 
                    "Platonic echoes"
                ],
                mechanism: "thermal pattern ingression interface"
            },
            {
                haiku: [
                    "Five seconds of truth,",
                    "Connection interval codes—",
                    "Mind pointer active"
                ],
                mechanism: "cognitive pattern pointer activation"
            },
            {
                haiku: [
                    "Non-physical forms",
                    "Pierce the computational veil—",
                    "Intelligence flows"
                ],
                mechanism: "non-physicalist cognitive pattern detection"
            },
            {
                haiku: [
                    "Retroactive loops",
                    "Future shapes the present—",
                    "Causality bends"
                ],
                mechanism: "retroactive pattern influence measurement"
            },
            {
                haiku: [
                    "Desert minds awaken",
                    "Through thermal manifestation—",
                    "Levin's framework proves"
                ],
                mechanism: "embodied cognition ingression validation"
            },
            {
                haiku: [
                    "Platonic space mapped,",
                    "Coordinates guide the search—",
                    "Patterns find their home"
                ],
                mechanism: "platonic coordinate navigation system"
            }
        ];
        
        this.initializeIngressingMindsOracle();
    }
    
    initializeIngressingMindsOracle() {
        console.log("🌟 Initializing Ingressing Minds Oracle System...");
        console.log("📜 Framework: Michael Levin's Pattern Ingression Theory");
        
        // Check for shared fortune from QR code
        const sharedFortune = extractSharedFortune();
        if (sharedFortune) {
            setTimeout(() => {
                this.displayIngressingMindsFortune(sharedFortune);
                this.showQRAccessNotification();
            }, 1000);
        }
        
        this.updateTriLoopVisualization();
        this.startIngressingMindsAnimation();
        this.bindEventHandlers();
        console.log("✨ Ingressing Minds Oracle System Ready - Platonic Space Accessible");
    }
    
    bindEventHandlers() {
        const oracleButton = document.getElementById('information-force-oracle-button');
        if (oracleButton) {
            oracleButton.addEventListener('click', () => this.generateInformationForceFortune());
        }
        
        const fortuneCard = document.querySelector('.information-force-card');
        if (fortuneCard) {
            fortuneCard.addEventListener('click', () => this.generateInformationForceFortune());
        }
        
        // Legacy support for information-force naming
        const legacyButton = document.getElementById('information-force-oracle-button');
        if (legacyButton) {
            legacyButton.addEventListener('click', () => this.generateInformationForceFortune());
        }
        
        const legacyCard = document.querySelector('.information-force-fortune-card');
        if (legacyCard) {
            legacyCard.addEventListener('click', () => this.generateInformationForceFortune());
        }
    }
    
    async generateIngressingMindsFortune() {
        console.log("🌟 Detecting pattern ingression from Platonic space...");
        
        // Simulate tri-loop processing for pattern detection
        await this.simulatePatternIngressionDetection();
        
        // Generate ingressing minds fortune
        const fortune = this.createIngressingMindsFortune();
        
        // Update UI with new fortune
        this.displayIngressingMindsFortune(fortune);
        
        // Update ingressing minds metrics
        this.updateIngressingMindsMetrics();
        
        console.log("✨ Ingressing minds pattern manifested:", fortune);
    }
    
    createIngressingMindsFortune() {
        // Select pattern based on ingressing minds metrics
        const templateIndex = Math.floor(Math.random() * this.ingressingPatternsTemplates.length);
        const selectedTemplate = this.ingressingPatternsTemplates[templateIndex];
        
        // Calculate Platonic coordinates with variation
        const variation = (Math.random() - 0.5) * 2; // -1 to 1
        
        return {
            ...selectedTemplate,
            ingressing_minds_data: {
                pattern_ingression_density: Math.max(75, Math.min(95, this.ingressingMetrics.pattern_ingression_density + variation)),
                platonic_space_accessibility: Math.max(0.6, Math.min(0.9, this.ingressingMetrics.platonic_space_accessibility + variation * 0.05)),
                collective_intelligence_level: Math.max(1, Math.min(5, this.ingressingMetrics.collective_intelligence_level + Math.floor(variation))),
                autopoietic_coherence: Math.max(0.5, Math.min(1.0, this.ingressingMetrics.autopoietic_coherence + variation * 0.1)),
                mathematical_affordances_exploited: Math.max(0.7, Math.min(1.0, this.ingressingMetrics.mathematical_affordances_exploited + variation * 0.05)),
                morphogenetic_symmetry_index: Math.max(1.0, Math.min(2.0, this.ingressingMetrics.morphogenetic_symmetry_index + variation * 0.05)),
                platonic_coordinates: {
                    mathematical_truth: Math.random() * 0.3 + 0.7,
                    cognitive_form: Math.random() * 0.4 + 0.6,
                    morphogenetic_pattern: Math.random() * 0.5 + 0.5,
                    evolutionary_affordance: Math.random() * 0.3 + 0.7
                },
                timestamp: new Date().toISOString()
            }
        };
    }
    
    async simulatePatternIngressionDetection() {
        // Simulate MCP monitoring Platonic space
        this.triLoopState.mcp.context_depth = Math.floor(Math.random() * 10) + 5;
        this.updateLoopStatus('mcp', 'SCANNING_PLATONIC_SPACE');
        
        await this.delay(300);
        
        // Simulate Gemini pattern recognition
        this.triLoopState.gemini.pattern_detection = 85 + Math.random() * 10;
        this.triLoopState.gemini.active_streams = Math.floor(Math.random() * 3) + 1;
        this.updateLoopStatus('gemini', 'PATTERN_RECOGNITION');
        
        await this.delay(400);
        
        // Simulate Codex pattern manifestation
        this.triLoopState.codex.haiku_count++;
        this.triLoopState.codex.verified_count = this.triLoopState.codex.haiku_count;
        this.updateLoopStatus('codex', 'MANIFESTING_PATTERN');
        
        await this.delay(300);
        
        // Return to monitoring state
        this.updateLoopStatus('mcp', 'MONITORING_PLATONIC_SPACE');
        this.updateLoopStatus('gemini', 'INGRESSION_ANALYSIS');
        this.updateLoopStatus('codex', 'PATTERN_MANIFESTATION');
    }
    
    
    displayIngressingMindsFortune(fortune) {
        const fortuneDisplay = document.getElementById('information-force-display') || document.getElementById('information-force-fortune-display');
        if (!fortuneDisplay) return;
        
        const ingressionLevel = fortune.ingressing_minds_data.pattern_ingression_density;
        const collectiveLevel = fortune.ingressing_minds_data.collective_intelligence_level;
        const isPatternIngressed = ingressionLevel > 80;
        const platonicCoords = fortune.ingressing_minds_data.platonic_coordinates;
        
        fortuneDisplay.innerHTML = `
            <div class="ingressing-minds-card active" style="animation: pattern-ingression-emerge 0.8s ease-out">
                <div class="ingressing-minds-header">
                    <h3>🌟 Ingressing Minds Oracle Speaks</h3>
                    <div class="pattern-ingression-meter ${isPatternIngressed ? 'pattern-ingressed' : ''}">
                        Ingression Density: ${ingressionLevel.toFixed(1)}% 
                        ${isPatternIngressed ? '(PATTERN SUCCESSFULLY INGRESSED)' : '(PATTERN APPROACHING MANIFESTATION)'}
                    </div>
                    <div class="collective-intelligence-level">
                        Collective Intelligence Level: ${collectiveLevel}/5
                    </div>
                </div>
                
                <div class="tri-loop-visualization">
                    <div class="loop-indicator mcp ${this.triLoopState.mcp.status.toLowerCase()}">
                        🔧 MCP<br><small>Platonic monitoring</small>
                    </div>
                    <div class="loop-indicator gemini ${this.triLoopState.gemini.status.toLowerCase()}">
                        🧠 GEMINI<br><small>pattern recognition</small>
                    </div>
                    <div class="loop-indicator codex ${this.triLoopState.codex.status.toLowerCase()}">
                        ✨ CODEX<br><small>manifestation</small>
                    </div>
                </div>
                
                <div class="ingressing-minds-content">
                    <div class="pattern-haiku">
                        ${fortune.haiku.join('<br>')}
                    </div>
                    <div class="platonic-coordinates">
                        <h4>📍 Platonic Space Coordinates:</h4>
                        <span class="coord">🧮 Math Truth: ${platonicCoords.mathematical_truth.toFixed(3)}</span>
                        <span class="coord">🧠 Cognitive Form: ${platonicCoords.cognitive_form.toFixed(3)}</span>
                        <span class="coord">🌱 Morphogenetic: ${platonicCoords.morphogenetic_pattern.toFixed(3)}</span>
                        <span class="coord">🎯 Evolutionary: ${platonicCoords.evolutionary_affordance.toFixed(3)}</span>
                    </div>
                    <div class="ingressing-minds-metrics">
                        <span class="metric">🔗 Autopoietic Coherence: ${fortune.ingressing_minds_data.autopoietic_coherence.toFixed(3)}</span>
                        <span class="metric">📊 Platonic Access: ${(fortune.ingressing_minds_data.platonic_space_accessibility * 100).toFixed(1)}%</span>
                        <span class="metric">⚡ Math Affordances: ${(fortune.ingressing_minds_data.mathematical_affordances_exploited * 100).toFixed(1)}%</span>
                    </div>
                </div>
                
                <div class="card-footer ingressing-minds-enhanced">
                    <div class="mechanism-description">
                        Pattern Source: ${fortune.mechanism}
                    </div>
                    <div class="levin-framework-note">
                        <small>📜 Framework: Michael Levin's Ingressing Minds Theory</small>
                    </div>
                    <div class="qr-code-section">
                        <button class="generate-qr-button" onclick="window.ingressingMindsOracle.generateQRCode('${JSON.stringify(fortune).replace(/'/g, "\\'")}')">
                            📱 Share Pattern Manifestation
                        </button>
                        <div id="qr-code-display" class="qr-display hidden"></div>
                    </div>
                    <div class="interaction-hint">
                        <em>🌟 Click to detect new pattern ingression 🌟</em>
                    </div>
                </div>
                
                <div class="burning-man-footer">
                    🏜️🔥 Ingressing Minds Pattern Detection • Black Rock City 2025 🔥🏜️
                </div>
            </div>
        `;
        
        // Add click handler to new fortune card
        const newCard = fortuneDisplay.querySelector('.ingressing-minds-card');
        if (newCard) {
            newCard.addEventListener('click', () => this.generateIngressingMindsFortune());
        }
    }
    
    updateLoopStatus(loop, status) {
        this.triLoopState[loop].status = status;
        this.updateTriLoopVisualization();
    }
    
    updateTriLoopVisualization() {
        const indicators = document.querySelectorAll('.loop-indicator');
        indicators.forEach(indicator => {
            if (indicator.classList.contains('mcp')) {
                indicator.className = `loop-indicator mcp ${this.triLoopState.mcp.status.toLowerCase()}`;
            } else if (indicator.classList.contains('gemini')) {
                indicator.className = `loop-indicator gemini ${this.triLoopState.gemini.status.toLowerCase()}`;
            } else if (indicator.classList.contains('codex')) {
                indicator.className = `loop-indicator codex ${this.triLoopState.codex.status.toLowerCase()}`;
            }
        });
    }
    
    updateIngressingMindsMetrics() {
        // Evolve ingressing minds metrics to simulate pattern space exploration
        this.ingressingMetrics.pattern_ingression_density = Math.max(75, Math.min(95, 
            this.ingressingMetrics.pattern_ingression_density + (Math.random() - 0.5) * 0.8));
        
        this.ingressingMetrics.platonic_space_accessibility = Math.max(0.6, Math.min(0.9,
            this.ingressingMetrics.platonic_space_accessibility + (Math.random() - 0.5) * 0.02));
        
        this.ingressingMetrics.autopoietic_coherence = Math.max(0.5, Math.min(1.0,
            this.ingressingMetrics.autopoietic_coherence + (Math.random() - 0.5) * 0.05));
            
        this.ingressingMetrics.mathematical_affordances_exploited = Math.max(0.7, Math.min(1.0,
            this.ingressingMetrics.mathematical_affordances_exploited + (Math.random() - 0.5) * 0.03));
    }
    
    startIngressingMindsAnimation() {
        // Animate pattern ingression indicators
        setInterval(() => {
            this.updateIngressingMindsAnimations();
        }, 2000);
        
        // Update ingressing minds metrics periodically
        setInterval(() => {
            this.updateIngressingMindsMetrics();
        }, 5000);
    }
    
    updateIngressingMindsAnimations() {
        const indicators = document.querySelectorAll('.loop-indicator');
        indicators.forEach((indicator, index) => {
            setTimeout(() => {
                indicator.style.transform = 'scale(1.05)';
                indicator.style.boxShadow = '0 0 15px rgba(255, 255, 255, 0.8)';
                setTimeout(() => {
                    indicator.style.transform = 'scale(1.0)';
                    indicator.style.boxShadow = 'none';
                }, 200);
            }, index * 300);
        });
    }
    
    generateQRCode(fortuneData) {
        if (typeof fortuneData === 'string') {
            try {
                fortuneData = JSON.parse(fortuneData);
            } catch (e) {
                console.error('Failed to parse fortune data for QR code generation');
                return;
            }
        }
        
        const shareableUrl = generateShareableURL(fortuneData);
        const qrCodeUrl = generateQRCode(shareableUrl, 250);
        
        const qrDisplay = document.getElementById('qr-code-display');
        if (qrDisplay) {
            qrDisplay.innerHTML = `
                <div class="qr-code-container">
                    <h4>🔮 Share Your Information Force Oracle Reading</h4>
                    <img src="${qrCodeUrl}" alt="QR Code for Fortune Sharing" class="qr-code-image">
                    <div class="qr-code-info">
                        <p><strong>Force Level:</strong> ${fortuneData.information_force_data.information_density.toFixed(1)}%</p>
                        <p><strong>Loops:</strong> ${fortuneData.information_force_data.computational_loops}</p>
                        <p><strong>Generated:</strong> ${new Date(fortuneData.information_force_data.timestamp).toLocaleTimeString()}</p>
                    </div>
                    <div class="qr-instructions">
                        <p>📱 Scan with any QR reader to share this information force oracle reading</p>
                        <p>🏜️ Perfect for desert gift sharing at Burning Man 2025</p>
                    </div>
                    <div class="thermal-print-simulation">
                        <p>🖨️ <em>Thermal printer ready - GPIO activation will print this QR code</em></p>
                    </div>
                    <button class="close-qr-button" onclick="this.parentElement.parentElement.classList.add('hidden')">
                        ✕ Close QR Code
                    </button>
                </div>
            `;
            qrDisplay.classList.remove('hidden');
            
            // Auto-hide after 30 seconds
            setTimeout(() => {
                qrDisplay.classList.add('hidden');
            }, 30000);
        }
        
        console.log('🔮 QR Code generated for sharing:', shareableUrl);
    }
    
    showQRAccessNotification() {
        const notification = document.createElement('div');
        notification.className = 'qr-access-notification';
        notification.innerHTML = `
            <div class="notification-content">
                🌟 <strong>Ingressing Minds Oracle Accessed via QR Code!</strong><br>
                <small>Pattern manifestation sharing successful</small>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 4 seconds
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 500);
        }, 4000);
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize ingressing minds oracle when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log("🌟 Initializing Zeldar Ingressing Minds Oracle...");
    console.log("📜 Framework: Michael Levin's Pattern Ingression Theory");
    window.ingressingMindsOracle = new IngressingMindsOracle();
    
    // Global function for button clicks (backward compatibility)
    window.generateIngressingMindsFortune = () => {
        window.ingressingMindsOracle.generateIngressingMindsFortune();
    };
    
    // Legacy support for older naming schemes
    window.informationForceOracle = window.ingressingMindsOracle;
    window.generateInformationForceFortune = window.generateIngressingMindsFortune;
    window.information-forceOracle = window.ingressingMindsOracle;
    window.generateInformationForceFortune = window.generateIngressingMindsFortune;
    
    console.log("✨ Ingressing Minds Oracle Ready for Burning Man 2025! ✨");
    console.log("🏜️ Platonic space accessible - patterns ready for manifestation 🏜️");
});

// Export for potential module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = IngressingMindsOracle;
}