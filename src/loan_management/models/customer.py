from dataclasses import dataclass, field
from datetime import date, datetime, timezone


@dataclass
class Customer:

    """Represent a customer registered in the loan management system"""


    customer_id: str
    full_name: str
    email: str
    phone_number: str
    date_of_birth: date
    address: str
    created_at: datetime = field(default_factory = lambda: datetime.now(timezone.utc))