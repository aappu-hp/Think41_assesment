import React, { createContext, useContext, useState } from 'react';

export const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [conversationId, setConversationId] = useState(null);
  const [conversations, setConversations] = useState([]);

  return (
    <ChatContext.Provider value={{
      messages, setMessages,
      loading, setLoading,
      inputValue, setInputValue,
      conversationId, setConversationId,
      conversations, setConversations
    }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => useContext(ChatContext);
