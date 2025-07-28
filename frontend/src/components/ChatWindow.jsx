import React from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';
import '../styles/ChatWindow.css';

const ChatWindow = () => {
  return (
    <div className="chat-window">
      <div className="chat-header">🛍️ AI Support Assistant</div>
      <MessageList />
      <UserInput />
    </div>
  );
};

export default ChatWindow;
