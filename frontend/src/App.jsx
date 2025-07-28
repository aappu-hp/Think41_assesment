import React from 'react';
import ChatWindow from './components/ChatWindow';
import ConversationList from './components/ConversationList';
import './styles/App.css';

const App = () => {
  return (
    <div className="app-container">
      <ConversationList />
      <ChatWindow />
    </div>
  );
};

export default App;
