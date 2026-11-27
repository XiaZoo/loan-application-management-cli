import pytest
from datetime import date, timedelta

from loan_management.models.customer import Customer
from loan_management.exceptions.customer_exception import CustomerValidationError
from loan_management.validators.customer_validator import CustomerValidator



@pytest.fixture
def valid_customer():

    return Customer(
        customer_id="CUST-123456789ABC",
        full_name="John Doe",
        email="john@example.com",
        phone_number="9876543210",
        date_of_birth=date(1998, 5, 15),
        address="Bhubaneswar, Odisha"
    )


def test_validate_valid_customer(valid_customer):

    result = CustomerValidator.validate(valid_customer)

    assert result is None

def test_validate_invalid_email(valid_customer):

    valid_customer.email = "invalid-email"

    with pytest.raises(CustomerValidationError, match="Customer validation failed: A valid email address is required"):
        CustomerValidator.validate(valid_customer)


def test_validate_invalid_phone_number(valid_customer):

    valid_customer.phone_number = "1234567890"

    with pytest.raises(CustomerValidationError, match = "Customer validation failed: Phone number must be a valid 10-digit Indian mobile number."):
        CustomerValidator.validate(valid_customer)

def test_validate_empty_full_name(valid_customer):
    valid_customer.full_name = "    "

    with pytest.raises(CustomerValidationError, match="Customer validation failed: Full name is required"):
        CustomerValidator.validate(valid_customer)

def test_validate_empty_address(valid_customer):

    valid_customer.address = ""

    with pytest.raises(CustomerValidationError, match="Customer validation failed: Address is required"):
        CustomerValidator.validate(valid_customer)

def test_validate_underage_customer(valid_customer):

    valid_customer.date_of_birth = date.today() - timedelta(days= 365 * 17)

    with pytest.raises(CustomerValidationError, match="Customer validation failed: Customer must be at least 18 years old."):
        CustomerValidator.validate(valid_customer)

def test_validate_future_date_of_birth(valid_customer):

    valid_customer.date_of_birth = date.today() + timedelta(days=1)

    with pytest.raises(CustomerValidationError, match="Customer validation failed: Date of birth cannot be in the future."):
        CustomerValidator.validate(valid_customer)

def test_validate_multiple_errors(valid_customer):

    valid_customer.email = "invalid-email"
    valid_customer.phone_number = "12345"
    valid_customer.address = ""

    with pytest.raises(CustomerValidationError) as exec_info:
        CustomerValidator.validate(valid_customer)

    error_message = str(exec_info.value)

    assert "Customer validation failed: A valid email address is required" in error_message
    assert "Phone number must be a valid 10-digit Indian mobile number." in error_message
    assert "Address is required" in error_message