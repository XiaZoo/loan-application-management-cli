import json
from pathlib import Path
from datetime import date, datetime

from loan_management.models.customer import Customer
from loan_management.exceptions.customer_exception import CustomerRepositoryError

class CustomerRepository:

    """Handles customer data persistence using JSON storage"""

    def __init__(self, file_path: Path | str | None = None) -> None:

        if file_path is None:
            project_root = Path(__file__).resolve().parents[3]
            self.file_path = project_root / "data" / "Customers.json"
        else:
            self.file_path = Path(file_path)


    @staticmethod
    def _serialize_customer(customer: Customer) -> dict[str, str]:

        """convert a customer object into json compatible data."""

        return {
            "customer_id": customer.customer_id,
            "full_name": customer.full_name,
            "email": customer.email,
            "phone_number": customer.phone_number,
            "date_of_birth": customer.date_of_birth.isoformat(),
            "address": customer.address,
            "created_at": customer.created_at.isoformat()

        }

    @staticmethod
    def _deserialize_customer(data: dict[str, str]) -> Customer:

        """Convert JSON customer object into a customer object"""

        return Customer(
            customer_id=data["customer_id"],
            full_name=data["full_name"],
            email=data["email"],
            phone_number=data["phone_number"],
            date_of_birth=date.fromisoformat(data["date_of_birth"]),
            address=data["address"],
            created_at=datetime.fromisoformat(data["created_at"])
        )


    def _read_customers(self) -> list[Customer]:

        """Read customer records from JSON storage"""

        if not self.file_path.exists():
            return []

        try:

            with open(self.file_path, "r", encoding="utf-8") as file:

                data = json.load(file)

            if not isinstance(data, list):
                raise CustomerRepositoryError("Customer storage must contain a JSON array.")

            customers = []

            for record in data:

                if not isinstance(record, dict):
                    raise CustomerRepositoryError("Invalid customer record found in JSON storage")
                else:
                    customers.append(self._deserialize_customer(record))


            return customers

        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exec:
            if isinstance(exec, CustomerRepositoryError):
                raise
            raise CustomerRepositoryError(f"unable to read customer records: {exec}") from exec


    def _write_customer(self, customers: list[Customer]) -> None:

        """Add customer records into JSON storage"""

        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            data = [self._serialize_customer(customer) for customer in customers]

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exec:
            raise CustomerRepositoryError(f"Unable to save the customer records: {exec}") from exec

    def _add_customer(self, customer: Customer) -> None:

        """add a new customer to JSON storage"""

        customers = self._read_customers()

        if any(existing.customer_id == customer.customer_id for existing in customers):
            raise CustomerRepositoryError(f"Customer ID {customer.customer_id} already exists")
        else:
            customers.append(customer)
            self._write_customer(customers)

    def _get_customer_by_id(self, customer_id: str) -> Customer | None:
        """Return a customer based on the unique customer id"""

        customers = self._read_customers()

        for customer in customers:

            if customer.customer_id == customer_id:
                return customer

        return None

    def _get_all_customers(self) -> list[Customer]:

        """Retrieve all customers from JSON storage"""

        return self._read_customers()


    