import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/chat";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage() {
    if (!input.trim()) return;

    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userMessage.text }),
      });
      const data = await response.json();

      const botMessage = {
        role: "bot",
        text: data.answer,
        validated: data.validated,
        verses: data.retrieved_verses,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "Something went wrong reaching the server.",
          validated: false,
          verses: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") sendMessage();
  }

  return (
    <div className="app">
      <h1>Shruti — Bhagavad Gita RAG</h1>

      <div className="chat-window">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <p>{msg.text}</p>
            {msg.role === "bot" && msg.verses && msg.verses.length > 0 && (
              <div className="verses">
                {msg.verses.map((v, j) => (
                  <div key={j} className="verse-card">
                    <strong>
                      Ch. {v.chapter}, V. {v.verse_number}
                    </strong>
                    <p>{v.text}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && <p className="loading">Thinking...</p>}
      </div>

      <div className="input-row">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask something about the Bhagavad Gita..."
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
