from assistant import CommissionAssistant


def test_extracts_core_details_and_summarizes():
    ai = CommissionAssistant()
    ai.process_message("u1", "My commission is a character illustration, budget $1200, due in 3 weeks.")
    summary = ai.process_message("u1", "summary")

    assert "character illustration" in summary
    assert "$1200" in summary
    assert "due in 3 weeks" in summary


def test_generates_next_steps_with_missing_items():
    ai = CommissionAssistant()
    result = ai.process_message("u2", "What should I do next?")

    assert "hard deadline" in result.lower()
    assert "budget" in result.lower()


def test_draft_message_uses_captured_details():
    ai = CommissionAssistant()
    ai.process_message("u3", "Need a website landing page, budget $800, due in 2 weeks")
    draft = ai.process_message("u3", "Draft a reply to client")

    assert "website landing page" in draft
    assert "$800" in draft
