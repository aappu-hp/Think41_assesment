// frontend/src/App.jsx
import React from 'react';
import { ChatProvider } from './context/ChatContext';
import ChatWindow from './components/ChatWindow';

function App() {
  return (
    <ChatProvider>
      <ChatWindow />
    </ChatProvider>
  );
}

export default App;
