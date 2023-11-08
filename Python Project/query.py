def make_query(transaction_id, query_name, query_type):
    type_flags = {"A": 0, "AAAA": 1, "CNAME": 2, "NS": 3}[query_type]
    name_length = len(query_name)
    query = (
        transaction_id.to_bytes(4, byteorder="big")
        + (0 << 28 | type_flags << 24 | name_length).to_bytes(4, byteorder="big")
        + int(0).to_bytes(4, byteorder="big")
        + query_name.encode()
    )
    return query


def make_response(transaction_id, query_name, type_flags, value):
    value_length = len(value)
    name_length = len(query_name)
    response = (
        transaction_id.to_bytes(4, byteorder="big")
        + (1 << 28 | type_flags << 24 | name_length).to_bytes(4, byteorder="big")
        + value_length.to_bytes(4, byteorder="big")
        + query_name.encode()
        + value.encode()
    )
    return response
