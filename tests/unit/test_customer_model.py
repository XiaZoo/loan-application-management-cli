from datetime import date, datetime
from loan_management.models.customer import Customer


def test_customer_model_creation():

    customer = Customer(
        customer_id="CUST-123456789ABC",
        full_name="John Doe",
        email="john@example.com",
        phone_number="9876543210",
        date_of_birth=date(1998, 5, 15),
        address="Bhubaneswar, Odisha",
    )

    assert customer.customer_id == "CUST-123456789ABC"
    assert customer.full_name == "John Doe"
    assert customer.email == "john@example.com"
    assert customer.phone_number == "9876543210"
    assert customer.date_of_birth == date(1998, 5, 15)
    assert customer.address == "Bhubaneswar, Odisha"


def test_customer_created_at_default_value():

    customer = Customer(
        customer_id="CUST-123456789ABC",
        full_name="John Doe",
        email="john@example.com",
        phone_number="9876543210",
        date_of_birth=date(1998, 5, 15),
        address="Bhubaneswar, Odisha",
    )

    assert isinstance(customer.created_at, datetime)
    assert customer.created_at.tzinfo is not None


def test_each_customer_gets_independent_created_at():

    customer1 = Customer(
        customer_id="CUST-123456789ABC",
        full_name="John Doe",
        email="john@example.com",
        phone_number="9876543210",
        date_of_birth=date(1998, 5, 15),
        address="Bhubaneswar, Odisha",
    )

    customer2 = Customer(
        customer_id="CUST-987654321ABC",
        full_name="Jane Doe",
        email="jane@example.com",
        phone_number="9876543211",
        date_of_birth=date(1997, 8, 20),
        address="Kolkata, West Bengal",
    )

    assert customer1.created_at is not customer2.created_at
