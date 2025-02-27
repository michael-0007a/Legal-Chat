document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

async function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const chatBox = document.getElementById('chat-box');

    // Add user message to chat box
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
    
    // Clear input
    document.getElementById('user-input').value = '';

    // Send message to Flask backend
    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    });

    const data = await response.json();

    // Add chatbot response to chat box
    chatBox.innerHTML += `<p><strong>Chatbot:</strong> ${data.response}</p>`;
    
    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;
}
