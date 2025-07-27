// frontend/src/components/ChatWindow.jsx
import React, { useState, useContext } from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';
import { ChatContext } from '../context/ChatContext';

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const { conversationId, setConversationId } = useContext(ChatContext);

  const sendMessage = async ({ userId, conversationId: cid, text }, setConvId) => {
    // append user message locally immediately
    setMessages((m) => [...m, { sender: 'user', content: text }]);

    // call backend
    const res = await fetch('http://localhost:5000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: userId,
    conversation_id: cid,
    message: text
  })
});
    const body = await res.json();
    // store new conversation id if created
    if (!cid && body.conversation_id) setConvId(body.conversation_id);

    // append AI response
    setMessages((m) => [...m, { sender: 'bot', content: body.ai_response }]);
  };

  const windowStyle = {
    maxWidth: '600px',
    margin: '20px auto',
    display: 'flex',
    flexDirection: 'column'
  };

  return (
    <div style={windowStyle}>
      <MessageList messages={messages} />
      <UserInput onSend={sendMessage} />
    </div>
  );
}
