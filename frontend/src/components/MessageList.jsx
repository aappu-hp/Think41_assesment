// src/components/MessageList.jsx
import React from 'react';
import { useChat } from '../context/ChatContext';
import '../styles/MessageList.css';

const MessageList = () => {
  const { messages } = useChat();

  return (
    <div className="message-list">
      {messages.map((m, idx) => (
        <div key={idx} className={`message ${m.sender}`}>
          <div className="avatar">{m.sender === 'user' ? '🧑‍💻' : '🤖'}</div>
          <div className="message-body">
            <div className="content">{m.content}</div>
            <div className="timestamp">🕐 {new Date(m.timestamp).toLocaleTimeString()}</div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MessageList;
