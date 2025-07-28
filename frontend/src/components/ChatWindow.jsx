// src/components/ChatWindow.jsx
import React, { useEffect, useRef } from 'react';
import { useChat } from '../context/ChatContext';
import MessageList from './MessageList';
import UserInput from './UserInput';
import '../styles/ChatWindow.css';

const ChatWindow = () => {
  const { messages, loading } = useChat();
  const bottomRef = useRef();

  // auto-scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  return (
    <section className="chat-window">
      <header className="chat-header">🛍️ AI Support Assistant</header>
      <div className="message-list-container">
        <MessageList />
        <div ref={bottomRef} />
      </div>
      <UserInput />
    </section>
  );
};

export default ChatWindow;
