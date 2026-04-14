import json
import threading
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

from web_chat import ChatHandler, parse_chat_payload


def test_parse_chat_payload_validates_required_fields():
    payload, error = parse_chat_payload(b'{"user_id": "u1", "message": "hello"}')
    assert error == ""
    assert payload["user_id"] == "u1"

    _, error_missing_message = parse_chat_payload(b'{"user_id": "u1"}')
    assert error_missing_message == "message is required"


def test_chat_endpoint_round_trip():
    server = ThreadingHTTPServer(("127.0.0.1", 0), ChatHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)

        body = json.dumps({"user_id": "test-user", "message": "My commission is a logo, budget $500, due in 2 weeks"})
        conn.request("POST", "/chat", body=body, headers={"Content-Type": "application/json"})
        response = conn.getresponse()
        data = json.loads(response.read().decode("utf-8"))

        assert response.status == 200
        assert "Perfect" in data["reply"] or "Got it" in data["reply"]
    finally:
        server.shutdown()
        server.server_close()
