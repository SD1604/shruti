"""
The Citation Validator Node — the last checkpoint before an answer is
considered "final." It asks the LLM a second, independent question: does
this answer actually stick to what the source verses say, or did it
invent something? This is what stops small hallucinations from silently
slipping through.
"""

from agent.state import AgentState
from agent.llm_client import generate_answer


def build_validation_prompt(answer: str, verses: list[dict]) -> str:
    verses_text = "\n\n".join(
        f"[Chapter {v['chapter']}, Verse {v['verse_number']}]\n{v['text']}"
        for v in verses
    )
    return f"""You are a strict fact-checker. You will be shown some SOURCE VERSES and an ANSWER that was supposedly based only on those verses.

Check whether every claim in the ANSWER is actually supported by the SOURCE VERSES. The answer should not add outside knowledge, invent interpretations not present in the text, or misrepresent what a verse says.

SOURCE VERSES:
{verses_text}

ANSWER TO CHECK:
{answer}

Respond in EXACTLY this format, nothing else:
VERDICT: PASS or FAIL
NOTES: one or two sentences explaining your verdict"""


def parse_verdict(validation_response: str) -> tuple[bool, str]:
    lines = validation_response.strip().split("\n")
    verdict_line = next((l for l in lines if l.upper().startswith("VERDICT:")), "")
    notes_line = next((l for l in lines if l.upper().startswith("NOTES:")), "")

    passed = "PASS" in verdict_line.upper()
    notes = notes_line.replace("NOTES:", "").replace("Notes:", "").strip()
    return passed, notes


def citation_validator_node(state: AgentState) -> AgentState:
    prompt = build_validation_prompt(state["answer"], state["retrieved_verses"])
    validation_response = generate_answer(prompt)
    passed, notes = parse_verdict(validation_response)

    state["validated"] = passed
    state["validation_notes"] = notes
    return state