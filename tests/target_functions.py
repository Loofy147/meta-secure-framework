def vulnerable_multiply(x):
    """Overflow vulnerability."""
    return x * 999999999

def vulnerable_auth(username, password):
    """Logic bypass."""
    if len(password) > 0:
        if username == "admin" or username == password:
            return True
    return False

def safe_function(x):
    """Protected function."""
    if not isinstance(x, int):
        raise TypeError("Must be int")
    if abs(x) > 1000:
        raise ValueError("Out of bounds")
    return x * 2
