import pytest
from datetime import date, datetime, timezone
import json


from loan_management.models.customer import Customer
from loan_management.repositories.customer_repository import CustomerRepository
from loan_management.exceptions.customer_exception import CustomerRepositoryError


@pytest.fixture
def valid_customer():
    return Customer(
        customer_id="CUST-123456789ABC",
        full_name="John Doe",
        email="john@example.com",
        phone_number="9876543210",
        date_of_birth=date(1998, 5, 15),
        address="Bhubaneswar, Odisha",
        created_at=datetime(2026, 11, 25, tzinfo=timezone.utc),
    )


@pytest.fixture
def repository(tmp_path):
    file_path = tmp_path / "customers.json"
    return CustomerRepository(file_path)



def test_get_all_customers_when_file_doesnot_exit(repository):

    customers = repository._get_all_customers()

    assert customers == []


def test_add_customer(repository, valid_customer):

    repository._add_customer(valid_customer)

    customers = repository._get_all_customers()

    assert len(customers) == 1
    assert customers[0].customer_id == valid_customer.customer_id


def test_get_customer_by_id(repository, valid_customer):

    repository._add_customer(valid_customer)

    customer = repository._get_customer_by_id(valid_customer.customer_id)

    assert customer is not None
    assert customer.customer_id == valid_customer.customer_id

def test_get_customer_by_invalid_id(repository):

    customer = repository._get_customer_by_id("invalid-id")

    assert customer is None


def test_get_all_customers(repository, valid_customer):

    repository._add_customer(valid_customer)

    customers = repository._get_all_customers()

    assert len(customers) == 1

def test_customer_persistence_after_repository_recreation(repository, valid_customer):

    repository._add_customer(valid_customer)

    new_repository = CustomerRepository(repository.file_path)

    customer = new_repository._get_customer_by_id(valid_customer.customer_id)

    assert customer is not None
    assert customer.customer_id == valid_customer.customer_id


def test_customer_date_and_datetime_deserialization(repository, valid_customer):

    repository._add_customer(valid_customer)

    customer = repository._get_customer_by_id(valid_customer.customer_id)

    assert customer is not None
    assert customer.date_of_birth == valid_customer.date_of_birth
    assert customer.created_at == valid_customer.created_at
    assert customer.created_at.tzinfo is not None


def test_add_customer_by_duplicate_id(repository, valid_customer):

    repository._add_customer(valid_customer)

    with pytest.raises(CustomerRepositoryError, match="already exists"):
        repository._add_customer(valid_customer)


def test_invalid_json_file(repository):

    repository.file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    repository.file_path.write_text(
        "{invalid json",
        encoding="utf-8",
    )

    with pytest.raises(CustomerRepositoryError):
        repository._get_all_customers()


def test_invalid_customer_record(repository):
    repository.file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    repository.file_path.write_text(
        json.dumps(["invalid-record"]),
        encoding="utf-8",
    )

    with pytest.raises(CustomerRepositoryError):
        repository._get_all_customers()



