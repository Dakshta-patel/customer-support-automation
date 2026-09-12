from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI(
    title="Customer Support Automation API",
    version="1.0.0"
)


class SupportTicket(BaseModel):
    subject: str
    description: str
    customer_email: EmailStr


def classify_ticket(subject: str, description: str) -> str:
    text = f"{subject} {description}".lower()

    if any(word in text for word in ["login", "password", "otp", "sign in"]):
        return "Account/Login Issue"

    if any(word in text for word in ["payment", "refund", "invoice", "billing"]):
        return "Payment/Billing Issue"

    if any(word in text for word in ["bug", "error", "crash", "not working", "technical"]):
        return "Technical Issue"

    if any(word in text for word in ["account", "profile", "email change"]):
        return "Account Issue"

    return "General Inquiry"


def detect_priority(subject: str, description: str) -> str:
    text = f"{subject} {description}".lower()

    high_priority_words = [
        "urgent",
        "critical",
        "blocked",
        "security",
        "fraud",
        "hacked",
        "data loss"
    ]

    medium_priority_words = [
        "failed",
        "unable",
        "error",
        "not working",
        "problem",
        "issue"
    ]

    if any(word in text for word in high_priority_words):
        return "High"

    if any(word in text for word in medium_priority_words):
        return "Medium"

    return "Low"


@app.get("/")
def home():
    return {
        "message": "Customer Support Automation API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/tickets")
def create_ticket(ticket: SupportTicket):
    category = classify_ticket(
        ticket.subject,
        ticket.description
    )

    priority = detect_priority(
        ticket.subject,
        ticket.description
    )

    return {
        "message": "Ticket received successfully",
        "ticket": ticket,
        "category": category,
        "priority": priority
    }