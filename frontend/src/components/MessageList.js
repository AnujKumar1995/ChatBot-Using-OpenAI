import React, { useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';

function formatTime(date) {
  return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function MessageBubble({ message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`message ${message.role}`}>
      <div className="msg-avatar">
        {isUser ? '👤' : '🤖'}
      </div>
      <div>
        <div className="msg-content">
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <ReactMarkdown>{message.content}</ReactMarkdown>
          )}
        </div>
        {message.timestamp && (
          <div className="msg-time">{formatTime(message.timestamp)}</div>
        )}
      </div>
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="typing-indicator">
      <div className="msg-avatar" style={{ background: '#818CF8', color: 'white', width: 32, height: 32, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 14 }}>
        🤖
      </div>
      <div className="typing-dots">
        <span /><span /><span />
      </div>
    </div>
  );
}

export default function MessageList({ messages, isLoading }) {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="welcome">
        <div className="welcome-icon">💬</div>
        <h2>How can we help you?</h2>
        <p>
          Ask us anything about our products, services, or policies. 
          We're here to help you 24/7.
        </p>
      </div>
    );
  }

  return (
    <div className="messages">
      {messages.map((msg, i) => (
        <MessageBubble key={i} message={msg} />
      ))}
      {isLoading && <TypingIndicator />}
      <div ref={endRef} />
    </div>
  );
}
