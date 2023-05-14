def check(cond, error_type, error_message):
    if not cond:
        raise error_type(error_message)
