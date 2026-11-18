
import os
import requests

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Order Service")

PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL",
    "http://product-service:8000"
)

PAYMENT_SERVICE_URL = os.getenv(
    "PAYMENT_SERVICE_URL",
    "http://payment-service:8000"
)


class OrderRequest(BaseModel):
    product_id: int
    quantity: int


@app.get("/")
def home():
    return {"message": "Order Service is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/orders")
def create_order(order: OrderRequest):

    if order.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    try:
        # Step 1: Get product details
        product_response = requests.get(
            f"{PRODUCT_SERVICE_URL}/products/{order.product_id}",
            timeout=5
        )
        product_response.raise_for_status()

        product = product_response.json()

        # Step 2: Calculate total amount
        total_amount = product["price"] * order.quantity

        # Step 3: Process payment
        payment_response = requests.post(
            f"{PAYMENT_SERVICE_URL}/payments",
            json={
                "order_id": 101,
                "amount": total_amount
            },
            timeout=5
        )
        payment_response.raise_for_status()

        payment = payment_response.json()

        # Step 4: Return order details
        return {
            "order_id": 101,
            "product": product["name"],
            "quantity": order.quantity,
            "total_amount": total_amount,
            "payment_status": payment["payment_status"],
            "order_status": "confirmed"
        }

    except requests.RequestException as error:
        raise HTTPException(
            status_code=503,
            detail=f"Service communication failed: {str(error)}"
        )
