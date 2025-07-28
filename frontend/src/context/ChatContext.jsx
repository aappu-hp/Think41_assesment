// src/context/ChatContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

export const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);

  // Load conversation list on mount or when conversationId changes
  useEffect(() => {
    fetchConversations();
  }, [conversationId]);

  const fetchConversations = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/conversations?user_id=1');
      if (!res.ok) throw new Error('Failed to fetch');
      setConversations(await res.json());
    } catch (err) {
      console.error(err);
    }
  };

  const loadConversation = async (cid) => {
    setConversationId(cid);
    try {
      const res = await fetch(`http://localhost:5000/api/messages?conversation_id=${cid}`);
      if (!res.ok) throw new Error('Failed to fetch messages');
      setMessages(await res.json());
    } catch (err) {
      console.error(err);
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim()) return;
    const userMsg = { sender: 'user', content: inputValue, timestamp: new Date().toISOString() };
    setMessages((m) => [...m, userMsg]);
    setLoading(true);

    try {
      const res = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: 1,
          conversation_id: conversationId,
          message: inputValue,
        }),
      });
      const { ai_response, conversation_id } = await res.json();
      setConversationId(conversation_id);
      const botMsg = { sender: 'bot', content: ai_response, timestamp: new Date().toISOString() };
      setMessages((m) => [...m, botMsg]);
    } catch (err) {
      console.error(err);
    } finally {
      setInputValue('');
      setLoading(false);
      fetchConversations();
    }
  };

  const newChat = () => {
    setConversationId(null);
    setMessages([]);
  };

  return (
    <ChatContext.Provider
      value={{
        messages,
        conversations,
        conversationId,
        inputValue,
        loading,
        setInputValue,
        sendMessage,
        loadConversation,
        newChat,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => useContext(ChatContext);
