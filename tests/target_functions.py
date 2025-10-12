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

def vulnerable_code_injection(user_input: str):
    """
    Vulnerable to code injection.
    A payload like "1+1" will be executed.
    """
    if not isinstance(user_input, str):
        return "Invalid input"

    try:
        # This is the vulnerability
        result = eval(user_input, {'__builtins__': {}}, {})
        return result
    except Exception:
        return "Execution failed"
