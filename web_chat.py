from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Tuple

from assistant import CommissionAssistant


CHAT_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Commission Assistant Chat</title>
  <style>
    body { font-family: Arial, sans-serif; background: #0b1020; color: #e5e7eb; margin: 0; }
    .container { max-width: 900px; margin: 0 auto; padding: 24px; }
    .card { background: #111827; border: 1px solid #1f2937; border-radius: 14px; overflow: hidden; }
    .header { padding: 14px 18px; border-bottom: 1px solid #1f2937; font-weight: 700; }
    .chat { height: 460px; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
    .msg { max-width: 80%; padding: 10px 12px; border-radius: 12px; line-height: 1.4; white-space: pre-wrap; }
    .user { align-self: flex-end; background: #2563eb; color: #fff; }
    .assistant { align-self: flex-start; background: #1f2937; color: #e5e7eb; }
    .composer { display: flex; gap: 10px; padding: 14px; border-top: 1px solid #1f2937; }
    .composer input { flex: 1; background: #0f172a; border: 1px solid #334155; color: #fff; border-radius: 10px; padding: 10px; }
    .composer button { background: #22c55e; border: none; border-radius: 10px; color: #052e16; font-weight: 700; padding: 0 16px; cursor: pointer; }
    .hint { color: #94a3b8; margin-top: 8px; font-size: 13px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <div class="header">🤖 Commission Assistant</div>
      <div id="chat" class="chat"></div>
      <form id="composer" class="composer">
        <input id="message" placeholder="Type commission details or ask for summary/next steps..." />
        <button type="submit">Send</button>
      </form>
    </div>
    <div class="hint">Try: "My commission is a mascot logo, budget $700, due in 10 days."</div>
  </div>

  <script>
    const chatEl = document.getElementById('chat');
    const formEl = document.getElementById('composer');
    const inputEl = document.getElementById('message');
    const userId = 'web-user';

    function addMessage(text, role) {
      const msg = document.createElement('div');
      msg.className = `msg ${role}`;
      msg.textContent = text;
      chatEl.appendChild(msg);
      chatEl.scrollTop = chatEl.scrollHeight;
    }

    addMessage('Hi! I can manage your commission details, summarize constraints, and draft client replies.', 'assistant');

    formEl.addEventListener('submit', async (event) => {
      event.preventDefault();
      const message = inputEl.value.trim();
      if (!message) return;

      addMessage(message, 'user');
      inputEl.value = '';

      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, message }),
      });

      if (!response.ok) {
        addMessage('Server error. Please try again.', 'assistant');
        return;
      }

      const data = await response.json();
      addMessage(data.reply, 'assistant');
    });
  </script>
</body>
</html>
"""


class ChatHandler(BaseHTTPRequestHandler):
    assistant = CommissionAssistant()

    def _send_json(self, payload: dict, status: int = HTTPStatus.OK) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in {"/", "/index.html"}:
            body = CHAT_HTML.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/health":
            self._send_json({"ok": True})
            return

        self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/chat":
            self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)
            return

        body_size = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(body_size)
        payload, error = parse_chat_payload(raw_body)

        if error:
            self._send_json({"error": error}, status=HTTPStatus.BAD_REQUEST)
            return

        reply = self.assistant.process_message(payload["user_id"], payload["message"])
        self._send_json({"reply": reply})


def parse_chat_payload(raw_body: bytes) -> Tuple[dict, str]:
    try:
        parsed = json.loads(raw_body.decode("utf-8"))
    except json.JSONDecodeError:
        return {}, "Invalid JSON body"

    user_id = str(parsed.get("user_id", "")).strip()
    message = str(parsed.get("message", "")).strip()

    if not user_id:
        return {}, "user_id is required"
    if not message:
        return {}, "message is required"

    return {"user_id": user_id, "message": message}, ""


def run_server(host: str = "127.0.0.1", port: int = 8080) -> None:
    server = ThreadingHTTPServer((host, port), ChatHandler)
    print(f"Commission Assistant chat UI running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
