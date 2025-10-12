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

def complex_nested_logic(a, b):
    """
    A function with deep conditional logic, designed to be difficult for a pure
    fuzzer to solve. The "vulnerability" is a specific path that is hard to reach.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        return "Type error"

    if a > 1000:
        if b < 50:
            if a * b == 60000:
                # This is the "vulnerability" we want to find
                return "VULNERABILITY_REACHED"
            else:
                return "Third level fail"
        else:
            return "Second level fail"
    else:
        return "First level fail"
