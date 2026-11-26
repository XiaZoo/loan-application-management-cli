
from datetime import date

import pytest

from loan_management.models.customer import Customer
from loan_management.services.customer_service import CustomerService
from loan_management.repositories.customer_repository import CustomerRepository
from loan_management.exceptions.customer_exception import CustomerValidationError


def build_customer(
    full_name: str = "Rahul Sharma",
    email: str = "rahul@example.com",
    phone_number: str = "9876543210"
) -> Customer:
    """Create a customer object for integration testing."""

    return Customer(
        customer_id="",
        full_name=full_name,
        email=email,
        phone_number=phone_number,
        date_of_birth=date(1995, 5, 17),
        address="Bhubaneswar, Odisha"
    )


def test_complete_customer_management_workflow(tmp_path):

    # Arrange: initialize temporary JSON storage and service

    file_path = tmp_path / "customers.json"

    repository = CustomerRepository(file_path=file_path)
    service = CustomerService(repository=repository)

    customer1 = build_customer()
    customer2 = build_customer(
        full_name="Amit Kumar",
        email="amit@example.com",
        phone_number="8765432109"
    )

    # Act 1: register customers

    registered_customer1 = service.register_customer(customer1)
    registered_customer2 = service.register_customer(customer2)

    # Assert 1: verify customer registration

    assert registered_customer1.customer_id.startswith("CUST-")
    assert registered_customer2.customer_id.startswith("CUST-")

    assert registered_customer1.customer_id != registered_customer2.customer_id

    assert file_path.exists()

    # Act 2: retrieve customer using customer ID

    retrieved_customer = service.get_customer_by_id(
        registered_customer1.customer_id
    )

    # Assert 2: verify individual customer retrieval

    assert retrieved_customer is not None
    assert retrieved_customer == registered_customer1

    # Act 3: retrieve all registered customers

    customers = service.get_all_customers()

    # Assert 3: verify customer collection

    assert len(customers) == 2
    assert registered_customer1 in customers
    assert registered_customer2 in customers

    # Assert 4: verify non-existing customer retrieval

    assert service.get_customer_by_id("CUST-NOT-FOUND") is None

    # Act 4: initialize a fresh service instance

    new_repository = CustomerRepository(file_path=file_path)
    new_service = CustomerService(repository=new_repository)

    persisted_customer = new_service.get_customer_by_id(
        registered_customer1.customer_id
    )

    # Assert 5: verify persistence across service instances

    assert persisted_customer == registered_customer1


def test_invalid_customer_registration_does_not_persist(tmp_path):

    # Arrange

    file_path = tmp_path / "customers.json"

    repository = CustomerRepository(file_path=file_path)
    service = CustomerService(repository=repository)

    invalid_customer = build_customer(full_name="")

    # Act & Assert

    with pytest.raises(CustomerValidationError):

        service.register_customer(invalid_customer)

    # Verify that invalid customer was not persisted

    assert not file_path.exists()
    assert service.get_all_customers() == []
