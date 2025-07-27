// src/App.jsx
import React from 'react';
import ChatWindow from './components/ChatWindow';
import { ChatProvider } from './context/ChatContext';

const App = () => {
  return (
    <ChatProvider>
      <ChatWindow />
    </ChatProvider>
  );
};

export default App;
