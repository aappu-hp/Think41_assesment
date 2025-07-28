import React from 'react';
import '../styles/MessageList.css';

const Message = ({ message }) => {
  const isUser = message.sender === 'user';
  const avatar = isUser ? '🧑‍💻' : '🤖';

  return (
    <div className={`message-row ${isUser ? 'user' : 'bot'}`}>
      <div className="message-avatar">{avatar}</div>
      <div className="message-bubble">
        <div className="message-content">{message.content}</div>
        <div className="message-time">
          🕐 {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

export default Message;
