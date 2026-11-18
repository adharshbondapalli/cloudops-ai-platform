
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Payment Service")


class PaymentRequest(BaseModel):
    order_id: int
    amount: float


@app.get("/")
def home():
    return {"message": "Payment Service is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/payments")
def process_payment(payment: PaymentRequest):
    return {
        "order_id": payment.order_id,
        "amount": payment.amount,
        "payment_status": "successful"
    }
