# Commission Assistant AI

A lightweight Python assistant that accepts commission details from a user and behaves like a personal assistant for commission workflow management.

## Features

- Captures structured commission details (project type, budget, deadline, style, notes).
- Maintains per-user session state in memory.
- Responds like a personal assistant by:
  - summarizing constraints,
  - generating next actions,
  - drafting client-ready messages,
  - answering follow-up planning questions.
- Includes a chatbot-like web UI.

## Run the chatbot web UI

```bash
python3 web_chat.py
```

Open: `http://127.0.0.1:8080`

### Suggested prompts

- `My commission is a logo redesign, budget $500, due in 2 weeks.`
- `Prefer minimalist style and blue tones.`
- `Draft a reply to confirm timeline.`
- `What should I do next?`

## Run the CLI (optional)

```bash
python3 assistant.py
```

Type `exit` to quit.

## Testing

```bash
pytest -q
python3 -m py_compile assistant.py web_chat.py tests/test_assistant.py tests/test_web_chat.py
```

## Notes

- Implementation is dependency-free (Python standard library only).
- Session data is in-memory and resets on restart.
