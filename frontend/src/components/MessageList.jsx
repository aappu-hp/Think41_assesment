// frontend/src/components/MessageList.jsx
import React, { useEffect, useRef } from 'react';
import Message from './Message';

export default function MessageList({ messages }) {
  const ref = useRef();
  // scroll to bottom on new message
  useEffect(() => {
    ref.current?.scrollTo(0, ref.current.scrollHeight);
  }, [messages]);
  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    overflowY: 'auto',
    height: '400px',
    padding: '8px',
    border: '1px solid #CCC',
    borderRadius: '4px',
  };
  return (
    <div style={containerStyle} ref={ref}>
      {messages.map((msg, i) => (
        <Message key={i} sender={msg.sender}>
          {msg.content}
        </Message>
      ))}
    </div>
  );
}
