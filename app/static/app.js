const form = document.querySelector("#chat-form");
const input = document.querySelector("#message");
const messagesElement = document.querySelector("#messages");
const button = form.querySelector("button");
const conversation = [];

function addMessage(role, content) {
  const element = document.createElement("div");
  element.className = `message ${role}`;
  element.textContent = content;
  messagesElement.appendChild(element);
  messagesElement.scrollTop = messagesElement.scrollHeight;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const content = input.value.trim();
  if (!content) return;

  conversation.push({ role: "user", content });
  addMessage("user", content);
  input.value = "";
  button.disabled = true;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: conversation }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Something went wrong");
    conversation.push({ role: "assistant", content: data.message });
    addMessage("assistant", data.message);
  } catch (error) {
    addMessage("assistant", `Error: ${error.message}`);
  } finally {
    button.disabled = false;
    input.focus();
  }
});

