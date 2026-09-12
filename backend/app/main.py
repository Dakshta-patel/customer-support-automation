from fastapi import FastAPI

app = FastAPI(
    title="Customer Support Automation API",
    version="1.0.0"
)


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