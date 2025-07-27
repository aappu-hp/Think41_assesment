// src/components/UserInput.jsx
import React from 'react';
import { useChat } from '../context/ChatContext';

const UserInput = () => {
  const { input, setInput, sendMessage } = useChat();
  const userId = 1; // Static for now

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(userId);
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex' }}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask a question..."
        style={{ flex: 1, padding: '10px', fontSize: '16px' }}
      />
      <button type="submit" style={{ padding: '10px' }}>Send</button>
    </form>
  );
};

export default UserInput;
