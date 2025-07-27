// src/components/ChatWindow.jsx
import React from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';
import { useChat } from '../context/ChatContext';

const ChatWindow = () => {
  const { loading } = useChat();

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', border: '1px solid #ccc', borderRadius: '8px', padding: '1rem' }}>
      <h2>E-commerce Assistant</h2>
      <MessageList />
      {loading && <p>Loading...</p>}
      <UserInput />
    </div>
  );
};

export default ChatWindow;
