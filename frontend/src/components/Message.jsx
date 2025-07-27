// frontend/src/components/Message.jsx
import React from 'react';

export default function Message({ sender, children }) {
  const isUser = sender === 'user';
  const style = {
    maxWidth: '70%',
    padding: '8px 12px',
    borderRadius: '12px',
    margin: '4px 0',
    alignSelf: isUser ? 'flex-end' : 'flex-start',
    backgroundColor: isUser ? '#DCF8C6' : '#EEE',
  };
  return <div style={style}>{children}</div>;
}
