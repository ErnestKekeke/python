document.addEventListener("DOMContentLoaded", function () {
// ................................................


const chatbox = document.getElementById('chatbox');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');

// Function to append message
function appendMessage(sender, message) {
    const div = document.createElement('div');
    div.classList.add('message');
    if (sender === 'You') {
        div.classList.add('user-message');
    } else {
        div.classList.add('bot-message');
    }
    div.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight; // Auto scroll
}

// Handle form submission (Enter or button click)
chatForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const message = userInput.value.trim();
    if (!message) return;

    appendMessage('You', message);

    // Send message to backend
    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => {
        let botMessage = data.reply;

        // Add emojis for fun
        if (/hello|hi|hey/i.test(message)) botMessage += " 👋";
        if (/how are you/i.test(message)) botMessage += " 😄";
        if (/clothes|products|wear/i.test(message)) botMessage += " 🛍️";
        if (/joke/i.test(message)) botMessage += " 😂";

        appendMessage('Bot', botMessage);
    })
    .catch(err => appendMessage('Bot', '⚠️ Error: Could not reach server'));

    userInput.value = '';
});



// ................................................
});
