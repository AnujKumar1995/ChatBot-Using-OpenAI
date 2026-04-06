import React from 'react';

export default function Header({ onClear, messageCount }) {
  return (
    <div className="header">
      <div className="header-left">
        <div className="header-avatar">🤖</div>
        <div>
          <h1>Customer Support</h1>
          <div className="status">
            <span className="status-dot" />
            Online — ready to help
          </div>
        </div>
      </div>
      <div className="header-actions">
        {messageCount > 0 && (
          <button onClick={onClear} title="New conversation">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}
