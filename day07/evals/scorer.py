def score_invoice(expected :dict, actual:dict) -> dict:
    fields = list(expected.keys())
    details = {}
    for field in fields:
        expected_value = expected[field]
        actual_value= actual.get(field)
        if field == 'total_amount':
            match = float(expected_value) == float(actual_value)
        else:
            match = str(expected_value) == str(actual_value)
        details[field] = {'expected': expected_value, 'actual': actual_value, 'match': match}
    accuracy = sum(d["match"] for d in details.values()) / len(fields)
    return {'details': details, 'accuracy': accuracy} 