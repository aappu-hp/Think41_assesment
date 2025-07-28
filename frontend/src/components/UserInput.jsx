import React from 'react';
import { useChat } from '../context/ChatContext';
import '../styles/UserInput.css';

const UserInput = () => {
  const {
    inputValue, setInputValue,
    setLoading, setMessages,
    conversationId, setConversationId
  } = useChat();

  const sendMessage = async () => {
    if (!inputValue.trim()) return;
    setLoading(true);

    const res = await fetch('http://localhost:5000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: 1,
        conversation_id: conversationId,
        message: inputValue
      })
    });

    const data = await res.json();
    setConversationId(data.conversation_id);

    const newMessages = [
      { sender: 'user', content: data.user_message, timestamp: new Date().toISOString() },
      { sender: 'bot', content: data.ai_response, timestamp: new Date().toISOString() }
    ];

    setMessages((prev) => [...prev, ...newMessages]);
    setInputValue('');
    setLoading(false);
  };

  return (
    <div className="user-input">
      <input
        type="text"
        placeholder="Type a message..."
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default UserInput;
