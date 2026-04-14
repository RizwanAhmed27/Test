from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class CommissionDetails:
    project_type: Optional[str] = None
    budget: Optional[str] = None
    deadline: Optional[str] = None
    style: Optional[str] = None
    notes: List[str] = field(default_factory=list)


@dataclass
class UserSession:
    user_id: str
    details: CommissionDetails = field(default_factory=CommissionDetails)
    history: List[str] = field(default_factory=list)


class CommissionAssistant:
    """A simple personal-assistant style AI for commission workflows."""

    def __init__(self) -> None:
        self.sessions: Dict[str, UserSession] = {}

    def get_session(self, user_id: str) -> UserSession:
        if user_id not in self.sessions:
            self.sessions[user_id] = UserSession(user_id=user_id)
        return self.sessions[user_id]

    def process_message(self, user_id: str, message: str) -> str:
        session = self.get_session(user_id)
        session.history.append(f"USER: {message}")

        self._extract_details(session.details, message)

        if self._looks_like_draft_request(message):
            reply = self._draft_client_message(session.details)
        elif self._looks_like_next_steps_request(message):
            reply = self._next_steps(session.details)
        elif self._looks_like_summary_request(message):
            reply = self._summary(session.details)
        else:
            reply = self._assistant_response(session.details)

        session.history.append(f"ASSISTANT: {reply}")
        return reply

    def _extract_details(self, details: CommissionDetails, text: str) -> None:
        lowered = text.lower()

        budget_match = re.search(r"\$\s?\d+[\d,]*(?:\.\d{1,2})?", text)
        if budget_match:
            details.budget = budget_match.group(0).replace(" ", "").rstrip(",.")

        deadline_patterns = [
            r"due\s+in\s+\d+\s+(?:days|day|weeks|week|months|month)\b",
            r"due\s+by\s+[A-Za-z]+\s+\d{1,2}",
            r"deadline\s+is\s+[^,.!]+",
        ]
        for pattern in deadline_patterns:
            match = re.search(pattern, lowered)
            if match:
                details.deadline = text[match.start() : match.end()]
                break

        style_markers = ["style", "aesthetic", "look", "vibe", "tone", "prefer"]
        if any(marker in lowered for marker in style_markers):
            details.style = text.strip()

        type_patterns = [
            r"commission\s+is\s+(?:a|an)\s+([^,.!]+)",
            r"need\s+(?:a|an)\s+([^,.!]+)",
            r"project\s+is\s+([^,.!]+)",
        ]
        for pattern in type_patterns:
            match = re.search(pattern, lowered)
            if match:
                original_slice = text[match.start(1) : match.end(1)]
                details.project_type = original_slice.strip()
                break

        if len(text.split()) > 3:
            details.notes.append(text.strip())

    def _looks_like_draft_request(self, text: str) -> bool:
        lowered = text.lower()
        return any(phrase in lowered for phrase in ["draft", "write a reply", "compose", "message to client"])

    def _looks_like_next_steps_request(self, text: str) -> bool:
        lowered = text.lower()
        return any(phrase in lowered for phrase in ["next", "what should i do", "plan", "steps"])

    def _looks_like_summary_request(self, text: str) -> bool:
        lowered = text.lower()
        return any(phrase in lowered for phrase in ["summary", "summarize", "recap"])

    def _summary(self, details: CommissionDetails) -> str:
        bullets = [
            f"Project: {details.project_type or 'Not provided yet'}",
            f"Budget: {details.budget or 'Not provided yet'}",
            f"Deadline: {details.deadline or 'Not provided yet'}",
            f"Style/Preferences: {details.style or 'Not provided yet'}",
        ]
        return "Here is your commission summary:\n- " + "\n- ".join(bullets)

    def _next_steps(self, details: CommissionDetails) -> str:
        steps = [
            "Confirm the exact deliverables and number of revisions with the client.",
            "Lock milestone dates (concept, review, final delivery).",
            "Request any reference files/assets before production starts.",
        ]

        if not details.budget:
            steps.insert(0, "Ask the client to confirm total budget and payment schedule.")
        if not details.deadline:
            steps.insert(0, "Ask for a hard deadline (date/timezone) to avoid timeline ambiguity.")

        return "Recommended next actions:\n1. " + "\n2. ".join(steps)

    def _draft_client_message(self, details: CommissionDetails) -> str:
        project = details.project_type or "your project"
        budget = details.budget or "the budget"
        deadline = details.deadline or "the target deadline"

        return (
            "Hi! Thanks for the commission details. I’ve noted "
            f"{project}, with {budget} and {deadline}. "
            "Before I begin, please confirm deliverables and revision rounds. "
            "Once confirmed, I’ll share a milestone schedule and get started right away."
        )

    def _assistant_response(self, details: CommissionDetails) -> str:
        missing = []
        if not details.project_type:
            missing.append("project type")
        if not details.budget:
            missing.append("budget")
        if not details.deadline:
            missing.append("deadline")

        if missing:
            return (
                "Got it — I’m tracking your commission. "
                f"Please share the following so I can manage it fully: {', '.join(missing)}."
            )

        return (
            "Perfect — I have the key commission constraints recorded. "
            "I can now draft messages, build your task plan, or provide a status recap anytime."
        )


def run_cli() -> None:
    assistant = CommissionAssistant()
    user_id = "default-user"

    print("Commission Assistant AI")
    print("Type your commission details or requests. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Assistant: Goodbye!")
            break

        response = assistant.process_message(user_id, user_input)
        timestamp = datetime.utcnow().strftime("%H:%M:%S UTC")
        print(f"Assistant [{timestamp}]: {response}\n")


if __name__ == "__main__":
    run_cli()
