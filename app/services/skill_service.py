"""Skill learning: digital literacy topics and content."""

from typing import Optional

# Static skill topics — can be moved to DB later
SKILLS = [
    {
        "id": "1",
        "title": "Digital Literacy Basics",
        "description": "Learn basic digital skills: using smartphone, internet, and common apps.",
        "content": "Start with your smartphone basics: open apps, use the camera, make calls. Then try the internet: search for information, use Google. Common apps to learn: WhatsApp, YouTube, and your bank's app.",
        "topics": ["Smartphone basics", "Internet search", "Common apps"],
    },
    {
        "id": "2",
        "title": "Banking & UPI",
        "description": "Learn to use UPI, digital payments, and basic banking online.",
        "content": "UPI lets you pay and receive money using your phone. Install GPay, PhonePe, or your bank's app. Link your bank account. You can pay bills, transfer money, and receive payments. Always verify the recipient before sending.",
        "topics": ["UPI", "Digital payments", "Banking apps"],
    },
    {
        "id": "3",
        "title": "Government Services Online",
        "description": "Access government services like DigiLocker, Aadhaar, and schemes online.",
        "content": "DigiLocker stores your documents digitally. You can use Aadhaar for verification. Many government schemes have online forms. Visit the official portal or use the Setu assistant to find schemes you're eligible for.",
        "topics": ["DigiLocker", "Aadhaar", "Scheme applications"],
    },
    {
        "id": "4",
        "title": "Staying Safe Online",
        "description": "Learn to protect yourself from scams and fraud online.",
        "content": "Never share OTP, passwords, or Aadhaar number with strangers. Government never asks for money in advance. Verify links before clicking. Check if a website is secure (https). Report suspicious calls or messages.",
        "topics": ["OTP safety", "Scam awareness", "Secure browsing"],
    },
]


def list_skills() -> list[dict]:
    """Return all skill topics."""
    return SKILLS


def get_skill(skill_id: str) -> Optional[dict]:
    """Get one skill by id."""
    for s in SKILLS:
        if s["id"] == skill_id:
            return s
    return None


def format_skills_for_chat() -> str:
    """Format skills list for chat response."""
    lines = ["I can help you learn these digital skills:\n"]
    for s in SKILLS:
        lines.append(f"• **{s['title']}** — {s['description']}")
    lines.append("\nAsk me about any topic or say 'Tell me more about banking' for details.")
    return "\n".join(lines)
