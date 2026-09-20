import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/chat";

function makeConversation() {
  return { id: Date.now(), title: "New Conversation", messages: [] };
}

function StreamedText({ text, speed = 15 }) {
  const [visibleChars, setVisibleChars] = useState(0);

  useEffect(() => {
    setVisibleChars(0);
    const interval = setInterval(() => {
      setVisibleChars((prev) => {
        if (prev >= text.length) {
          clearInterval(interval);
          return prev;
        }
        return prev + 3; // reveal a few characters per tick, feels smoother than 1-by-1
      });
    }, speed);
    return () => clearInterval(interval);
  }, [text, speed]);

  return <ReactMarkdown>{text.slice(0, visibleChars)}</ReactMarkdown>;
}

function App() {
  const [conversations, setConversations] = useState([makeConversation()]);
  const [activeId, setActiveId] = useState(conversations[0].id);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const active = conversations.find((c) => c.id === activeId);

  function updateActiveConversation(updater) {
    setConversations((prev) =>
      prev.map((c) => (c.id === activeId ? updater(c) : c)),
    );
  }

  function startNewConversation() {
    const fresh = makeConversation();
    setConversations((prev) => [fresh, ...prev]);
    setActiveId(fresh.id);
  }

  async function sendMessage() {
    if (!input.trim() || loading) return;
    const question = input.trim();
    setInput("");
    setLoading(true);

    updateActiveConversation((c) => ({
      ...c,
      title: c.messages.length === 0 ? question.slice(0, 40) : c.title,
      messages: [...c.messages, { role: "user", text: question }],
    }));

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: question }),
      });
      const data = await response.json();

      updateActiveConversation((c) => ({
        ...c,
        messages: [
          ...c.messages,
          {
            role: "bot",
            text: data.answer,
            validated: data.validated,
            verses: data.retrieved_verses,
          },
        ],
      }));
    } catch (err) {
      updateActiveConversation((c) => ({
        ...c,
        messages: [
          ...c.messages,
          {
            role: "bot",
            text: "The connection to the server was lost. Please try again.",
            verses: [],
          },
        ],
      }));
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") sendMessage();
  }

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-icon">🪷</span>
          <span className="brand-name">Shruti</span>
        </div>

        <button className="new-convo-btn" onClick={startNewConversation}>
          + New Conversation
        </button>

        <div className="convo-list">
          {conversations.map((c) => (
            <div
              key={c.id}
              className={`convo-item ${c.id === activeId ? "active" : ""}`}
              onClick={() => setActiveId(c.id)}
            >
              {c.title}
            </div>
          ))}
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <h1>BHAGAVAD GITA</h1>
        </header>

        <div className="chat-window">
          {active.messages.length === 0 && (
            <div className="empty-state">
              <p>What troubles you today?</p>
            </div>
          )}

          {active.messages.map((msg, i) => (
            <div key={i} className={`bubble-row ${msg.role}`}>
              {msg.role === "bot" && <div className="avatar">S</div>}
              <div className={`bubble ${msg.role}`}>
                {msg.role === "bot" ? (
                  <StreamedText text={msg.text} />
                ) : (
                  <ReactMarkdown>{msg.text}</ReactMarkdown>
                )}

                {msg.role === "bot" && msg.validated === false && (
                  <div className="warning-box">
                    ⚠️ This answer could not be fully verified against the
                    source verses. Please treat it with caution and check the
                    citations below.
                  </div>
                )}

                {msg.verses && msg.verses.length > 0 && (
                  <div className="verses">
                    {msg.verses.map((v, j) => (
                      <div key={j} className="verse-card">
                        <div className="verse-label">
                          Chapter {v.chapter}, Verse {v.verse_number}
                        </div>
                        <p className="verse-text">"{v.text}"</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="bubble-row bot">
              <div className="avatar">S</div>
              <div className="bubble bot loading-bubble">
                Consulting the verses...
              </div>
            </div>
          )}
        </div>

        <div className="input-bar">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask, and the verses shall answer..."
            disabled={loading}
          />
          <button onClick={sendMessage} disabled={loading} className="send-btn">
            ➤
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;
