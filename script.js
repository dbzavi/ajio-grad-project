document.addEventListener('DOMContentLoaded', () => {
    renderDashboard();
});

function renderDashboard() {
    // Render Chart
    const ctx = document.getElementById('insightsChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: insightsData.map(d => d.theme),
            datasets: [{
                data: insightsData.map(d => d.count),
                backgroundColor: [
                    '#ef4444', '#f59e0b', '#3b82f6', '#8b5cf6', '#10b981'
                ],
                borderWidth: 0,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#f8fafc' } }
            }
        }
    });

    // Render Themes
    const container = document.getElementById('themes-container');
    insightsData.forEach(item => {
        const card = document.createElement('div');
        card.className = 'theme-card';
        card.innerHTML = `
            <h3>${item.theme}</h3>
            <span class="count">${item.count} Mentions</span>
            <p>${item.description}</p>
            <div class="quote">"${item.quotes[0]}"</div>
        `;
        container.appendChild(card);
    });

    // Setup Chat
    setupChat();
}

function setupChat() {
    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('chat-send');
    const history = document.getElementById('chat-history');

    async function handleSend() {
        const text = input.value.trim();
        if(!text) return;
        
        // Append user msg
        const uMsg = document.createElement('div');
        uMsg.className = 'chat-msg user';
        uMsg.innerHTML = `<strong>You:</strong> ${text}`;
        history.appendChild(uMsg);
        input.value = '';
        history.scrollTop = history.scrollHeight;

        // Simulate typing
        const typingMsg = document.createElement('div');
        typingMsg.className = 'chat-msg bot';
        typingMsg.innerHTML = `<em>InsightBot is thinking...</em>`;
        history.appendChild(typingMsg);
        history.scrollTop = history.scrollHeight;

        await new Promise(r => setTimeout(r, 1500));

        // Get response from Python backend
        let answer = "";
        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: text })
            });
            const data = await res.json();
            answer = data.answer;
        } catch (e) {
            console.error(e);
            answer = "Sorry, the RAG backend server is currently unreachable. Make sure python app.py is running.";
        }
        
        // Remove typing, append bot msg
        history.removeChild(typingMsg);
        const bMsg = document.createElement('div');
        bMsg.className = 'chat-msg bot';
        bMsg.innerHTML = `<strong>InsightBot:</strong> ${answer}`;
        history.appendChild(bMsg);
        bMsg.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    sendBtn.addEventListener('click', handleSend);
    input.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') handleSend();
    });
}
