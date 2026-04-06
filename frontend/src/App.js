import React, { useEffect } from 'react';
import Header from './components/Header';
import MessageList from './components/MessageList';
import ChatInput from './components/ChatInput';
import QuickActions from './components/QuickActions';
import { useChat } from './hooks/useChat';

export default function App() {
  const { messages, isLoading, error, sendMessage, clearChat, cancelRequest, setError } = useChat();

  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(null), 5000);
      return () => clearTimeout(timer);
    }
  }, [error, setError]);

  return (
    <div className="app">
      <Header onClear={clearChat} messageCount={messages.length} />
      <MessageList messages={messages} isLoading={isLoading} />
      <QuickActions onSelect={sendMessage} visible={messages.length === 0 && !isLoading} />
      <ChatInput onSend={sendMessage} isLoading={isLoading} onCancel={cancelRequest} />
      {error && <div className="error-toast">{error}</div>}
    </div>
  );
}
