import React, { useState } from "react";

function Chat() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {
    if (!message) return;

    // Show "typing..." placeholder
    setChat([...chat, { user: message, bot: "..." }]);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });
      const data = await response.json();

      // Replace placeholder with AI response
      setChat(prev => [...prev.slice(0, -1), { user: message, bot: data.response }]);
      setMessage("");
    } catch (error) {
      setChat(prev => [...prev.slice(0, -1), { user: message, bot: "Error: server unreachable" }]);
      console.error(error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>AI Pension Chatbot</h2>
      <div style={{ border: "1px solid black", padding: "10px", height: "300px", overflowY: "scroll" }}>
        {chat.map((c, i) => (
          <div key={i}>
            <b>You:</b> {c.user} <br />
            <b>Bot:</b> {c.bot} <br /><br />
          </div>
        ))}
      </div>
      <input
        type="text"
        placeholder="Ask a question..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        style={{ width: "80%" }}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default Chat;