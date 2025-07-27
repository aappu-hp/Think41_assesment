// frontend/src/components/UserInput.jsx
import React, { useState, useContext } from 'react';
import { ChatContext } from '../context/ChatContext';

export default function UserInput({ onSend }) {
  const [text, setText] = useState('');
  const { userId, conversationId, setConversationId } = useContext(ChatContext);

  const handleSend = () => {
    if (!text.trim()) return;
    onSend({ userId, conversationId, text }, setConversationId);
    setText('');
  };

  const handleKey = (e) => {
    if (e.key === 'Enter') handleSend();
  };

  const containerStyle = { display: 'flex', marginTop: '8px' };
  const inputStyle = { flex: 1, padding: '8px', fontSize: '1rem' };
  const buttonStyle = { padding: '8px 16px', marginLeft: '8px' };

  return (
    <div style={containerStyle}>
      <input
        style={inputStyle}
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKey}
        placeholder="Type your message…"
      />
      <button style={buttonStyle} onClick={handleSend}>Send</button>
    </div>
  );
}
