// src/components/ConversationList.jsx
import React from 'react';
import { useChat } from '../context/ChatContext';
import '../styles/ConversationList.css';

const ConversationList = () => {
  const { conversations, conversationId, loadConversation, newChat } = useChat();

  return (
    <aside className="conversation-list">
      <button className="new-chat-btn" onClick={newChat}>
        + New Chat
      </button>
      {conversations.map((c) => (
        <div
          key={c.id}
          className={`conversation-item ${c.id === conversationId ? 'active' : ''}`}
          onClick={() => loadConversation(c.id)}
        >
          🗨️ Chat #{c.id}
        </div>
      ))}
    </aside>
  );
};

export default ConversationList;
