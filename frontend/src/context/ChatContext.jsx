// src/context/ChatContext.jsx
import React, { createContext, useContext, useState } from 'react';

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);

  const sendMessage = async (userId) => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          conversation_id: conversationId,
          message: input
        })
      });

      const data = await res.json();
      if (data.ai_response) {
        setMessages((prev) => [
          ...prev,
          { sender: 'bot', content: data.ai_response }
        ]);
        if (!conversationId) setConversationId(data.conversation_id);
      } else {
        setMessages((prev) => [
          ...prev,
          { sender: 'bot', content: 'AI failed to respond.' }
        ]);
      }
    } catch (err) {
      console.error('Error:', err);
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', content: 'Error contacting backend.' }
      ]);
    } finally {
      setInput('');
      setLoading(false);
    }
  };

  return (
    <ChatContext.Provider value={{
      messages, input, setInput, loading, sendMessage
    }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => useContext(ChatContext);
