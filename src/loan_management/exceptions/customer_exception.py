
class CustomerValidationError(ValueError):
    """Raised when a customer information fails validations"""


class CustomerRepositoryError(Exception):
    """Raised when customer data persistence or retrieval fails."""
