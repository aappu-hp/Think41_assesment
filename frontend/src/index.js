import React from 'react';
import ReactDOM from 'react-dom/client'; // ✅ React 18+ import
import App from './App';
import './styles/App.css';
import { ChatProvider } from './context/ChatContext';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <ChatProvider>
    <App />
  </ChatProvider>
);
