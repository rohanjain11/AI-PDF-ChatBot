import React, { useEffect, useRef, useState } from "react";
import { queryPDF } from "../api";

const Chat = ({ isPdfUploaded }) => {
  const [userQuestion, setUserQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  const askQuestion = async () => {
    const trimmed = userQuestion.trim();
    if (!trimmed || !isPdfUploaded) return;

    setChatHistory((prev) => [
      ...prev,
      { role: "user", text: trimmed },
      { role: "ai", text: null },
    ]);

    setUserQuestion("");
    setLoading(true);

    try {
      const data = await queryPDF(trimmed);
      const answer = data?.answer || "No answer found.";

      setChatHistory((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = { role: "ai", text: answer };
        return updated;
      });
    } catch (err) {
      console.error("Query error:", err);
      let message = "Something went wrong. Try again.";
      if (err.response?.data) {
        const d = err.response.data.detail;
        if (typeof d === "string") message = d;
        else if (Array.isArray(d) && d.length) message = d[0].msg || String(d[0]);
      } else if (err.code === "ERR_NETWORK" || !err.response) {
        message = "Cannot reach the server.";
      }

      setChatHistory((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = { role: "ai", text: `⚠️ ${message}` };
        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => setChatHistory([]);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !loading) askQuestion();
  };

  return (
    <>
      <div className="chat-area">
        {chatHistory.length === 0 && (
          <div className="empty-state">
            <div className="empty-state-icon">💬</div>
            <h3>{isPdfUploaded ? "Ask anything" : "Upload a PDF to begin"}</h3>
            <p>
              {isPdfUploaded
                ? "Type a question below and the AI will answer based on your document."
                : "Once you upload a document, you can have a conversation about its contents here."}
            </p>
          </div>
        )}

        {chatHistory.map((msg, i) => (
          <div key={i} className={`chat-bubble ${msg.role}`}>
            <div className="bubble-label">
              {msg.role === "user" ? "You" : "AI"}
            </div>
            <div className="bubble-content">
              {msg.text === null ? (
                <div className="thinking-dots">
                  <span />
                  <span />
                  <span />
                </div>
              ) : (
                msg.text
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-bar">
        {chatHistory.length > 0 && (
          <button className="btn-clear" onClick={clearChat} title="Clear chat">
            🗑
          </button>
        )}
        <input
          type="text"
          value={userQuestion}
          onChange={(e) => setUserQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={
            isPdfUploaded
              ? "Ask a question about your document..."
              : "Upload a PDF first"
          }
          disabled={!isPdfUploaded}
        />
        <button
          className="btn-send"
          onClick={askQuestion}
          disabled={loading || !userQuestion.trim() || !isPdfUploaded}
          title="Send"
        >
          {loading ? (
            <span style={{ fontSize: 14 }}>⏳</span>
          ) : (
            "➤"
          )}
        </button>
      </div>
    </>
  );
};

export default Chat;
