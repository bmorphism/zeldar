// Fortune Card Shortcode
// Generates an interactive fortune card component
// Styled to mimic historical automaton fortune cards

let fortune_data = call("fortune_generator");

let card_html = `
<div class="zeldar-fortune-card" onclick="generateNewFortune()">
    <div class="card-header">
        <h3>Your Fortune</h3>
        <small class="mechanism-note">${fortune_data.mechanism}</small>
    </div>
    
    <div class="fortune-content">
        <p class="fortune-text">${fortune_data.fortune}</p>
    </div>
    
    <div class="card-footer">
        <div class="system-note">
            <small>${fortune_data.zeldar_wisdom}</small>
        </div>
        <div class="interaction-hint">
            <em>Click for another fortune</em>
        </div>
    </div>
    
    <div class="system-details">
        <small class="authenticity">${fortune_data.historical_authenticity}</small>
    </div>
</div>

<script>
function generateNewFortune() {
    // Simulate coin insertion and mechanical operation
    const card = document.querySelector('.zeldar-fortune-card');
    card.classList.add('mechanical-operation');
    
    // Simulate mechanical delay (like historical automatons)
    setTimeout(() => {
        window.location.reload(); // Simple refresh for new fortune
    }, 800);
}
</script>

<style>
.zeldar-fortune-card {
    border: 1px solid #e9ecef;
    border-radius: 12px;
    padding: 24px;
    margin: 20px 0;
    background: white;
    color: #495057;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s ease;
    max-width: 500px;
    margin: 20px auto;
}

.zeldar-fortune-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.card-header h3 {
    color: #212529;
    text-align: center;
    margin-bottom: 8px;
    font-size: 1.2rem;
    font-weight: 600;
}

.mechanism-note {
    color: #6c757d;
    text-align: center;
    font-style: normal;
    display: block;
    font-size: 0.85rem;
}

.fortune-content {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
}

.fortune-text {
    font-size: 1rem;
    text-align: center;
    line-height: 1.6;
    margin: 0;
    color: #495057;
    font-weight: 500;
}

.card-footer {
    margin-top: 20px;
}

.system-note {
    color: #6c757d;
    text-align: center;
    margin-bottom: 12px;
    font-size: 0.85rem;
}

.interaction-hint {
    color: #007bff;
    text-align: center;
    font-size: 0.85rem;
}

.system-details {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #e9ecef;
}

.authenticity {
    color: #868e96;
    font-size: 0.75rem;
    display: block;
    text-align: center;
}

.mechanical-operation {
    animation: gentlePulse 0.6s ease-in-out;
}

@keyframes gentlePulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.02); }
}
</style>
`;

card_html;