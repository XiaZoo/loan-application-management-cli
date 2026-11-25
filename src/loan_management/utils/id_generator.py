
import uuid


def generate_customer_id() -> str:

    """Generate a unique identifier for a customer."""
    return f"CUST-{uuid.uuid4().hex[:12].upper()}"
 