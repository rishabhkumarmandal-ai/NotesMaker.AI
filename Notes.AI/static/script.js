document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const chatForm = document.getElementById("chat-form");
    const userMessageInput = document.getElementById("user-message");
  
    function appendMessage(content, sender) {
      const messageDiv = document.createElement("div");
      messageDiv.textContent = content;
      messageDiv.classList.add(sender);
      chatBox.appendChild(messageDiv);
      chatBox.scrollTop = chatBox.scrollHeight; 
    }
  
    chatForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const userMessage = userMessageInput.value.trim();
      if (!userMessage) return;
  
      appendMessage(userMessage, "user");
      userMessageInput.value = "";
  
      // Send the message to the backend
      try {
        const response = await fetch("/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_id: "123", message: userMessage }),
        });
        const data = await response.json();
        if (data.message) {
          appendMessage(data.message, "bot");
        }
      } catch (error) {
        appendMessage("Error: Unable to reach the server.", "bot");
      }
    });
  });
  