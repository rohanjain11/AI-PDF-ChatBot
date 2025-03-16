import React, { useState } from 'react';
import axios from 'axios';
import { TailSpin } from 'react-loader-spinner';

const Chat = () => {
  const [userQuestion, setUserQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!userQuestion.trim()) return;
  
    setChatHistory((prevHistory) => [
      { question: userQuestion, answer: '⏳ Thinking...' }, // Temporary message
      ...prevHistory,
    ]);
  
    setUserQuestion('');
    setLoading(true);
  
    try {
      const response = await axios.post(
        'http://localhost:8000/query/',
        { question: userQuestion },
        { headers: { 'Content-Type': 'application/json' } }
      );
  
      setChatHistory((prevHistory) => [
        { question: userQuestion, answer: response.data.answer || 'No answer found.' },
        ...prevHistory.slice(1), // Remove "Thinking..." message
      ]);
    } catch (error) {
      console.error('Error querying PDF:', error);
      setChatHistory((prevHistory) => [
        { question: userQuestion, answer: '⚠️ Error retrieving answer. Try again.' },
        ...prevHistory.slice(1),
      ]);
    } finally {
      setLoading(false);
    }
  };
  

  // Function to clear chat history
  const clearChat = () => {
    setChatHistory([]);
  };

  return (
    <div className="chat-container">
      <h2>Ask a Question</h2>
      <div className="chat-input">
        <input
          type="text"
          value={userQuestion}
          onChange={(e) => setUserQuestion(e.target.value)}
          placeholder="Enter your question"
        />
        <button onClick={askQuestion} className="ask-button" disabled={loading}>
          {loading ? <TailSpin height="20" width="20" color="#ffffff" ariaLabel="loading" /> : 'Ask'}
        </button>
      </div>

      {/* Clear Chat Button */}
      {chatHistory.length > 0 && (
        <button onClick={clearChat} className="clear-chat">
          Clear Chat 🗑️
        </button>
      )}

      {/* Chat History */}
      <div className="chat-history">
        {chatHistory.map((chat, index) => (
          <div key={index} className="chat-message">
            <p className="chat-question">❓ <strong>{chat.question}</strong></p>
            <p className="chat-answer">💡 {chat.answer}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Chat;
