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
    return {
        "message": "Ticket received successfully",
        "ticket": ticket
    }