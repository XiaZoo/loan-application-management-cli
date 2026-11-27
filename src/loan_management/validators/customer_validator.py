import re
from datetime import date, datetime


from loan_management.models.customer import Customer
from loan_management.exceptions.customer_exception import CustomerValidationError

class CustomerValidator:

    """Validate customer information before registration"""

    EMAIL_PATTERN = re.compile(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )

    PHONE_PATTERN = re.compile(r"^[6-9]\d{9}$")

    @staticmethod
    def validate(customer: Customer) -> None:

        """Validate all mandatory customer fields"""

        errors = []

        #validate full_name

        if not isinstance(customer.full_name, str) or not customer.full_name.strip():
            errors.append("Full name is required")

        #validate email

        if not isinstance(customer.email, str) or not CustomerValidator.EMAIL_PATTERN.fullmatch(customer.email.strip()):
            errors.append("A valid email address is required")

        #validate phone number

        if not isinstance(customer.phone_number, str) or not CustomerValidator.PHONE_PATTERN.fullmatch(customer.phone_number.strip()):
            errors.append("Phone number must be a valid 10-digit Indian mobile number.")

        #validate date of birth

        if not isinstance(customer.date_of_birth, date) or isinstance(customer.date_of_birth, datetime):
            errors.append("A valid date of birth is required")
        else:
            today = date.today()
            dob = customer.date_of_birth

            if today < dob:
                errors.append("Date of birth cannot be in the future.")

            else:
                age = today.year - dob.year - ((today.month, today.day) > (dob.month, dob.day))

                if age < 18:
                    errors.append("Customer must be at least 18 years old.")

        #validate address

        if not isinstance(customer.address, str) or not customer.address.strip():
            errors.append("Address is required")


        #if any error is present

        if errors:
            raise CustomerValidationError("Customer validation failed: " + " ".join(errors))