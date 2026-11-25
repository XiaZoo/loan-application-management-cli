from loan_management.utils.id_generator import generate_customer_id


def test_generate_customer_id():

    customer_id = generate_customer_id()

    assert customer_id.startswith("CUST-")
    assert len(customer_id) == 17



def test_generate_unique_customer_ids():

    #set comprehension, return a set named customer_ids with unique cust unique IDs

    customer_ids = {generate_customer_id() for _ in range(1000)}

    assert len(customer_ids) == 1000