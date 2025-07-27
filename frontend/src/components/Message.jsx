// src/components/Message.jsx
import React from 'react';

const Message = ({ sender, content }) => {
  const isUser = sender === 'user';
  return (
    <div style={{
      textAlign: isUser ? 'right' : 'left',
      margin: '10px 0',
      background: isUser ? '#dcf8c6' : '#f1f0f0',
      padding: '10px',
      borderRadius: '10px',
      maxWidth: '80%',
      alignSelf: isUser ? 'flex-end' : 'flex-start'
    }}>
      <strong>{isUser ? 'You' : 'AI'}:</strong> {content}
    </div>
  );
};

export default Message;
