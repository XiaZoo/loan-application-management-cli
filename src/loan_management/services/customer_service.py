from loan_management.repositories.customer_repository import CustomerRepository
from loan_management.models.customer import Customer
from loan_management.validators.customer_validator import CustomerValidator
from loan_management.utils.id_generator import generate_customer_id


class CustomerService:

    """Handles customer related business operations"""

    def __init__(self, repository: CustomerRepository | None = None) -> None:
        self.repository = repository or CustomerRepository()


    def register_customer(self, customer: Customer) -> Customer:
        """generate customer ID, validate and register a customer"""

        customer.customer_id = generate_customer_id()

        CustomerValidator.validate(customer)

        self.repository._add_customer(customer)

        return customer

    def get_customer_by_id(self, customer_id: str) -> Customer | None:

        """Retrieve a customer using their unique customer ID"""

        return self.repository._get_customer_by_id(customer_id)

    def get_all_customers(self) -> list[Customer]:

        """Retrieved all registered customers"""
        return self.repository._get_all_customers()
