import { useState, useCallback, useRef } from 'react';

const API_BASE = process.env.REACT_APP_API_URL || '/api';

export function useChat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const abortRef = useRef(null);

  const sendMessage = useCallback(async (text) => {
    if (!text.trim() || isLoading) return;

    const userMessage = { role: 'user', content: text, timestamp: new Date() };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    const history = messages.map(({ role, content }) => ({ role, content }));

    try {
      abortRef.current = new AbortController();

      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          conversation_history: history,
          session_id: sessionId,
        }),
        signal: abortRef.current.signal,
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || `Server error (${res.status})`);
      }

      const data = await res.json();
      const botMessage = {
        role: 'assistant',
        content: data.message,
        timestamp: new Date(),
        tokens: data.tokens_used,
      };

      setMessages((prev) => [...prev, botMessage]);
      if (data.session_id) setSessionId(data.session_id);
    } catch (err) {
      if (err.name !== 'AbortError') {
        setError(err.message);
      }
    } finally {
      setIsLoading(false);
    }
  }, [messages, isLoading, sessionId]);

  const clearChat = useCallback(() => {
    setMessages([]);
    setSessionId(null);
    setError(null);
    fetch(`${API_BASE}/clear`, { method: 'POST' }).catch(() => {});
  }, []);

  const cancelRequest = useCallback(() => {
    if (abortRef.current) {
      abortRef.current.abort();
      setIsLoading(false);
    }
  }, []);

  return { messages, isLoading, error, sessionId, sendMessage, clearChat, cancelRequest, setError };
}
