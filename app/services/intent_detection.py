"""Intent detection: classify user message into chat, scheme_search, eligibility_check, skill_learning."""

from typing import Literal

Intent = Literal["chat", "scheme_search", "eligibility_check", "skill_learning"]

# Keywords (lowercase) for each intent. First match wins in order.
SCHEME_KEYWORDS = [
    "scheme", "schemes", "yojana", "yojna", "available", "government",
    "sarkari", "sarkari yojana", "list", "browse", "search", "find",
    "kya hai", "kya hain", "what schemes", "which schemes",
    "for farmers", "for students", "kisan", "kisano", "vidyarthi",
]

ELIGIBILITY_KEYWORDS = [
    "eligible", "eligibility", "am i eligible", "check eligibility",
    "qualify", "qualification", "kya main eligible", "mera age",
    "my age", "my income", "mera income", "income", "occupation",
    "farmer", "kisan", "student", "check if", "can i get",
]

SKILL_KEYWORDS = [
    "learn", "learning", "skill", "skills", "training", "course",
    "sikhe", "sikhao", "digital", "digital literacy", "padhai",
]


def detect_intent(message: str) -> Intent:
    """
    Rule-based intent detection. Returns one of:
    chat, scheme_search, eligibility_check, skill_learning
    """
    if not message or not message.strip():
        return "chat"

    text = message.strip().lower()

    # Check scheme search
    for kw in SCHEME_KEYWORDS:
        if kw in text:
            return "scheme_search"

    # Check eligibility
    for kw in ELIGIBILITY_KEYWORDS:
        if kw in text:
            return "eligibility_check"

    # Check skill learning
    for kw in SKILL_KEYWORDS:
        if kw in text:
            return "skill_learning"

    return "chat"
