// src/App.jsx
import React from 'react';
import ChatWindow from './components/ChatWindow';
import ConversationList from './components/ConversationList';
import './styles/App.css';

function App() {
  return (
    <div className="app-container">
      <ConversationList />
      <ChatWindow />
    </div>
  );
}

export default App;
