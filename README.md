# Commission Assistant AI

A lightweight Python assistant that accepts commission details from a user and behaves like a personal assistant for that commission workflow.

## What it does

- Captures structured commission details (project type, budget, deadline, style, notes).
- Maintains per-user session state in memory.
- Responds like a personal assistant by:
  - summarizing constraints,
  - generating next actions,
  - drafting client-ready messages,
  - answering follow-up planning questions.

## Quick start

```bash
python3 assistant.py
```

Then paste messages such as:

- `My commission is a logo redesign, budget $500, due in 2 weeks.`
- `Prefer minimalist style and blue tones.`
- `Draft a reply to confirm timeline.`
- `What should I do next?`

Type `exit` to quit.

## Notes

- This implementation is intentionally dependency-free.
- Session data is in-memory only and resets on restart.
