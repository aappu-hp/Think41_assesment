// src/components/UserInput.jsx
import React from 'react';
import { useChat } from '../context/ChatContext';
import '../styles/UserInput.css';

const UserInput = () => {
  const { inputValue, setInputValue, sendMessage, loading } = useChat();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!loading) sendMessage();
  };

  return (
    <form className="user-input" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Type your message..."
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        disabled={loading}
      />
      <button type="submit" disabled={loading || !inputValue.trim()}>
        {loading ? '...' : 'Send'}
      </button>
    </form>
  );
};

export default UserInput;
