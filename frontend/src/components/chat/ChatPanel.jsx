import { useState } from 'react';
import Card from '../common/Card';

export default function ChatPanel({ onAsk }) {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const send = async (e) => {
    e.preventDefault();
    if (!message.trim() || loading) return;

    const text = message.trim();
    setMessage('');
    setMessages((prev) => [...prev, { type: 'user', text }]);
    setLoading(true);
    try {
      const res = await onAsk(text);
      setMessages((prev) => [...prev, { type: 'assistant', text: res.answer }]);
    } catch (err) {
      setMessages((prev) => [...prev, { type: 'assistant', text: `Error: ${err.message}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Seyalla Chat" subtitle="Ask about commission, targets, and anomalies.">
      <div className="chat-window">
        {messages.length === 0 && <p className="muted">Try: “How much commission did I earn today?”</p>}
        {messages.map((m, i) => (
          <div key={i} className={`bubble ${m.type}`}>{m.text}</div>
        ))}
      </div>
      <form className="chat-form" onSubmit={send}>
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask Seyalla"
        />
        <button type="submit" disabled={loading}>{loading ? '...' : 'Send'}</button>
      </form>
    </Card>
  );
}
