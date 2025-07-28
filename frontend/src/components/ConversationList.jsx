import React, { useEffect } from 'react';
import { useChat } from '../context/ChatContext';
import '../styles/ConversationList.css';

const ConversationList = () => {
  const {
    conversations,
    setConversations,
    setMessages,
    setConversationId
  } = useChat();

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const res = await fetch('http://localhost:5000/api/conversations?user_id=1');
        const data = await res.json();
        setConversations(data);
      } catch (e) {
        console.error('Failed to fetch conversations', e);
      }
    };

    fetchConversations();
  }, []);

  const loadConversation = async (cid) => {
    const res = await fetch(`http://localhost:5000/api/messages?conversation_id=${cid}`);
    const data = await res.json();
    setConversationId(cid);
    setMessages(data);
  };

  return (
    <div className="conversation-list">
      <div className="conversation-title">🕓 Conversations</div>
      {conversations.map((conv) => (
        <div key={conv.id} onClick={() => loadConversation(conv.id)} className="conversation-item">
          Conversation #{conv.id}
        </div>
      ))}
    </div>
  );
};

export default ConversationList;
