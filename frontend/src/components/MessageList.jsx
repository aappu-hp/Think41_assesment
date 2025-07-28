import React, { useEffect, useRef } from 'react';
import { useChat } from '../context/ChatContext';
import Message from './Message';
import '../styles/MessageList.css';

const MessageList = () => {
  const { messages, loading } = useChat();
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="message-list">
      {messages.map((msg) => (
        <Message key={msg.id} message={msg} />
      ))}
      {loading && <div className="loading">🤖 Thinking...</div>}
      <div ref={bottomRef}></div>
    </div>
  );
};

export default MessageList;
