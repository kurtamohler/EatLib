def check(cond, error_type, error_message):
    if not cond:
        raise error_type(error_message)

def check_type(obj, expected_type, obj_name):
    if not isinstance(obj, expected_type):
        raise TypeError(
            f"Expected '{obj_name}' to be a {expected_type} but got {type(obj)}")

def check_value(cond, error_message):
    check(cond, ValueError, error_message)
