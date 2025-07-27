// frontend/src/context/ChatContext.jsx
import React, { createContext, useState } from 'react';

export const ChatContext = createContext();

export function ChatProvider({ children }) {
  const [userId] = useState(1);            // hard‑coded user id
  const [conversationId, setConversationId] = useState(null);

  return (
    <ChatContext.Provider value={{ userId, conversationId, setConversationId }}>
      {children}
    </ChatContext.Provider>
  );
}
