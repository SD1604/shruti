import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/chat";

const LOADING_MESSAGES = [
  "Consulting the verses...",
  "Seeking wisdom in the Gita...",
  "Turning the pages of dharma...",
  "Consulting the timeless teachings...",
  "Unfolding the words of Krishna...",
  "Unfolding Krishna's timeless wisdom...",
  "Letting the wisdom unfold...",
];

function useRotatingLoadingText(active) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (!active) {
      setIndex(0);
      return;
    }
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % LOADING_MESSAGES.length);
    }, 1800);
    return () => clearInterval(interval);
  }, [active]);

  return LOADING_MESSAGES[index];
}

function makeConversation() {
  return { id: Date.now(), title: "New Conversation", messages: [] };
}

function formatTime() {
  return new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
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
        return prev + 3;
      });
    }, speed);
    return () => clearInterval(interval);
  }, [text, speed]);

  return <ReactMarkdown>{text.slice(0, visibleChars)}</ReactMarkdown>;
}

function UserIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      width="16"
      height="16"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
    >
      <circle cx="12" cy="8" r="3.2" />
      <path d="M5 20c0-3.5 3-6 7-6s7 2.5 7 6" />
    </svg>
  );
}

function CopyIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      width="14"
      height="14"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
    >
      <rect x="8" y="8" width="12" height="12" rx="2" />
      <path d="M4 16V6a2 2 0 0 1 2-2h10" />
    </svg>
  );
}

function App() {
  const [conversations, setConversations] = useState([makeConversation()]);
  const [activeId, setActiveId] = useState(conversations[0].id);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState(null);
  const loadingText = useRotatingLoadingText(loading);

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
      messages: [
        ...c.messages,
        { role: "user", text: question, time: formatTime() },
      ],
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

  function handleCopy(text, index) {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 1500);
  }

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-icon">🪷</span>
          <div className="brand-text">
            <span className="brand-name">Shruti</span>
            <span className="brand-subtitle">
              AI ASSISTANT FOR
              <br />
              THE BHAGAVAD GITA
            </span>
          </div>
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

        <div className="sidebar-footer">
          <p className="sidebar-quote">
            "Timeless Wisdom
            <br />
            for a Calmer Tomorrow"
          </p>
          <div className="sidebar-divider" />
          <p className="sidebar-sanskrit">ॐ शान्ति: शान्ति: शान्ति:</p>
          <p className="sidebar-translation">
            May there be peace within, around, and beyond.
          </p>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div className="topbar-spacer" />
          <nav className="topnav">
            <span>BHAGAVAD GITA</span>
            <span className="dot">|</span>
            <span>QUESTIONS</span>
            <span className="dot">|</span>
            <span>CLARITY</span>
            <span className="dot">|</span>
            <span>A HIGHER PERSPECTIVE</span>
          </nav>
          <div className="user-icon">
            <UserIcon />
          </div>
        </header>

        <div className="hero-quotes">
          <div className="hero-quote-left-wrap">
            <div className="hero-vline" />
            <p className="hero-quote-left">
              Different questions.
              <br />
              The same eternal truth.
            </p>
          </div>
          <div className="hero-quote-right-wrap">
            <p className="hero-quote-right">
              "In every question there is a seeker.
              <br />
              In every answer, a light."
            </p>
            <span className="hero-dash">—</span>
          </div>
        </div>

        <div className="section-divider" />

        <div className="chat-window">
          {active.messages.length === 0 && (
            <div className="empty-state">
              <p>What troubles you today?</p>
            </div>
          )}

          {active.messages.map((msg, i) => (
            <div key={i} className={`bubble-row ${msg.role}`}>
              {msg.role === "bot" && (
                <div className="avatar bot-avatar">🪷</div>
              )}

              <div className={`bubble ${msg.role}`}>
                {msg.role === "bot" ? (
                  <StreamedText text={msg.text} />
                ) : (
                  <ReactMarkdown>{msg.text}</ReactMarkdown>
                )}

                {msg.verses && msg.verses.length > 0 && (
                  <div className="verses">
                    {msg.verses.map((v, j) => (
                      <div key={j} className="verse-card">
                        <div className="verse-label">
                          Chapter {v.chapter}, Verse {v.verse_number}
                        </div>
                        {v.sanskrit && (
                          <p className="verse-sanskrit">{v.sanskrit}</p>
                        )}
                        <p className="verse-text">"{v.text}"</p>
                      </div>
                    ))}
                  </div>
                )}

                {msg.role === "bot" && msg.validated === false && (
                  <div className="warning-box">
                    ⚠️ This answer could not be fully verified against the
                    source verses. Please treat it with caution and check the
                    citations below.
                  </div>
                )}

                {msg.role === "bot" && (
                  <button
                    className="copy-btn"
                    onClick={() => handleCopy(msg.text, i)}
                  >
                    <CopyIcon /> {copiedIndex === i ? "Copied" : "Copy"}
                  </button>
                )}
              </div>

              {msg.role === "user" && (
                <div className="avatar user-avatar">
                  <UserIcon />
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="bubble-row bot">
              <div className="avatar bot-avatar">🪷</div>
              <div className="bubble bot loading-bubble">{loadingText}</div>
            </div>
          )}
        </div>

        <div className="input-bar">
          <div className="input-pill">
            <span className="input-icon">📎</span>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask, and the verses shall answer..."
              disabled={loading}
            />
            <button
              onClick={sendMessage}
              disabled={loading}
              className="send-btn-inline"
            >
              ➤
            </button>
          </div>
        </div>

        <div className="corner-tagline">
          <span>ANCIENT WISDOM</span>
          <span>MODERN QUESTIONS</span>
          <span>A BRIGHTER YOU</span>
        </div>
      </main>
    </div>
  );
}

export default App;
