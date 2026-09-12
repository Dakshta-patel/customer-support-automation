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


def generate_response(category: str, priority: str) -> str:
    if category == "Account/Login Issue":
        response = (
            "Please verify your login details and request a new OTP. "
            "If the issue continues, please share the time of the failed attempt."
        )

    elif category == "Payment/Billing Issue":
        response = (
            "Please verify your payment details and check whether the amount "
            "was deducted from your account. If the amount was deducted, "
            "please share the transaction reference."
        )

    elif category == "Technical Issue":
        response = (
            "Please share the steps that caused the issue, the exact error "
            "message, and any relevant screenshots or logs."
        )

    elif category == "Account Issue":
        response = (
            "Please provide more details about the account issue so that "
            "we can help you resolve it."
        )

    else:
        response = (
            "Thank you for contacting support. Please provide any additional "
            "details that may help us understand your request."
        )

    if priority == "High":
        response = (
            "This request has been marked as high priority. "
            + response
        )

    return response


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

    suggested_response = generate_response(
        category,
        priority
    )

    return {
        "message": "Ticket received successfully",
        "ticket": ticket,
        "category": category,
        "priority": priority,
        "suggested_response": suggested_response
    }