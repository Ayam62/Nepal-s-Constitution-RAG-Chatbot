const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');

// Handle Enter key
userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // 1. Add User Message to UI
    appendMessage('user', text);
    userInput.value = '';

    // 2. Show Typing Indicator (Optional UI enhancement)
    const loadingId = appendLoading();

    try {
        // 3. Send to Backend
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: text }),
        });

        const data = await response.json();
        
        // 4. Remove loading and show Bot Message
        removeLoading(loadingId);
        appendMessage('bot', data.answer);

    } catch (error) {
        removeLoading(loadingId);
        appendMessage('bot', "Sorry, I encountered an error connecting to the server.");
        console.error('Error:', error);
    }
}

function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');

    const avatar = sender === 'user' ? 'U' : 'AI';
    
    // Convert newlines to <br> for the bot response display
    const formattedText = text.replace(/\n/g, '<br>');

    msgDiv.innerHTML = `
        <div class="avatar">${avatar}</div>
        <div class="bubble">${formattedText}</div>
    `;

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto scroll to bottom
}

function appendLoading() {
    const id = 'loading-' + Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', 'bot-message');
    msgDiv.id = id;
    msgDiv.innerHTML = `
        <div class="avatar">AI</div>
        <div class="bubble" style="color: #94a3b8; font-style: italic;">Thinking...</div>
    `;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return id;
}

function removeLoading(id) {
    const element = document.getElementById(id);
    if (element) element.remove();
}

async function clearChat() {
    if(confirm("Are you sure you want to clear the history?")) {
        await fetch('/clear', { method: 'POST' });
        location.reload(); // Refresh page to reset UI
    }
}