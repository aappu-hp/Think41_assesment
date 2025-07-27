// src/components/MessageList.jsx
import React from 'react';
import { useChat } from '../context/ChatContext';
import Message from './Message';

const MessageList = () => {
  const { messages } = useChat();

  return (
    <div style={{ minHeight: '200px', marginBottom: '1rem' }}>
      {messages.map((msg, idx) => (
        <Message key={idx} sender={msg.sender} content={msg.content} />
      ))}
    </div>
  );
};

export default MessageList;
