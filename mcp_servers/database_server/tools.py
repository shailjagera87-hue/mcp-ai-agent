from sqlalchemy import or_

from mcp_servers.database_server.database import SessionLocal
from mcp_servers.database_server.models import Customer
from mcp_servers.database_server.schemas import (
    CustomerSearchRequest,
    CustomerIDRequest
)


def search_customers(query: str, limit: int = 10):

    request = CustomerSearchRequest(
        query=query,
        limit=limit
    )

    session = SessionLocal()

    try:
        search_term = f"%{request.query}%"

        customers = (
            session.query(Customer)
            .filter(
                or_(
                    Customer.name.ilike(search_term),
                    Customer.email.ilike(search_term),
                    Customer.city.ilike(search_term)
                )
            )
            .order_by(Customer.id)
            .limit(request.limit)
            .all()
        )

        return {
            "success": True,
            "count": len(customers),
            "customers": [
                {
                    "id": customer.id,
                    "name": customer.name,
                    "email": customer.email,
                    "city": customer.city,
                    "phone": customer.phone
                }
                for customer in customers
            ]
        }

    finally:
        session.close()


def get_customer(customer_id: int):

    request = CustomerIDRequest(
        customer_id=customer_id
    )

    session = SessionLocal()

    try:
        customer = (
            session.query(Customer)
            .filter(Customer.id == request.customer_id)
            .first()
        )

        if not customer:
            return {
                "success": False,
                "error": "CUSTOMER_NOT_FOUND",
                "message": "No customer found with this ID."
            }

        return {
            "success": True,
            "customer": {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "city": customer.city,
                "phone": customer.phone
            }
        }

    finally:
        session.close()