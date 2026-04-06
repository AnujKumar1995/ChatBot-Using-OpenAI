import React from 'react';

const SUGGESTIONS = [
  "How do I reset my password?",
  "What are your business hours?",
  "I need help with my order",
  "How do I contact a human agent?",
];

export default function QuickActions({ onSelect, visible }) {
  if (!visible) return null;

  return (
    <div className="quick-actions">
      {SUGGESTIONS.map((text) => (
        <button
          key={text}
          className="quick-action-btn"
          onClick={() => onSelect(text)}
        >
          {text}
        </button>
      ))}
    </div>
  );
}
