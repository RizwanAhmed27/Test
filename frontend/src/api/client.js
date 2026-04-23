const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

async function request(path, body) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`API ${path} failed: ${response.status} ${detail}`);
  }

  return response.json();
}

export const SeyallaApi = {
  chat: (payload) => request('/chat', payload),
  summary: (payload) => request('/summary', payload),
  analytics: (payload) => request('/analytics', payload),
  anomalies: (payload) => request('/anomalies', payload),
  recommendations: (payload) => request('/recommendations', payload),
};
