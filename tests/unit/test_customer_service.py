import pytest
from unittest.mock import MagicMock, patch
from datetime import date

from loan_management.models.customer import Customer
from loan_management.repositories.customer_repository import CustomerRepository
from loan_management.services.customer_service import CustomerService
from loan_management.validators.customer_validator import CustomerValidationError

@pytest.fixture
def sample_customer():
    return Customer(
        customer_id="CUST-123456789ABC",
        full_name="John Doe",
        email="john@example.com",
        phone_number="9876543210",
        date_of_birth=date(1995, 5, 17),
        address="Bhubaneswar, Odisha"
    )


@pytest.fixture
def mock_repository():
    return MagicMock(spec=CustomerRepository)


@pytest.fixture
def customer_service(mock_repository):
    return CustomerService(repository=mock_repository)

@patch("loan_management.services.customer_service.generate_customer_id", return_value="CUST-123456789ABC")


def test_register_customer_success(mock_id_generator, customer_service, sample_customer, mock_repository):

    sample_customer.customer_id = ""

    result = customer_service.register_customer(sample_customer)

    mock_id_generator.assert_called_once()

    mock_repository._add_customer.assert_called_once_with(sample_customer)

    assert result.customer_id == "CUST-123456789ABC"

def test_register_customer_validation_failure(customer_service, sample_customer, mock_repository):

    sample_customer.email = "invalid-email"

    with pytest.raises(CustomerValidationError):
        customer_service.register_customer(sample_customer)

    mock_repository._add_customer.assert_not_called()

def test_get_customer_by_id(customer_service, sample_customer, mock_repository):

    mock_repository._get_customer_by_id.return_value = sample_customer

    result = customer_service.get_customer_by_id(sample_customer.customer_id)

    mock_repository._get_customer_by_id.assert_called_once_with(sample_customer.customer_id)

    assert result == sample_customer

def test_get_all_customers(customer_service, sample_customer, mock_repository):

    mock_repository._get_all_customers.return_value = [sample_customer]

    result = customer_service.get_all_customers()

    mock_repository._get_all_customers.assert_called_once()

    assert result == [sample_customer]



