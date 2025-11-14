import os
import sys

def check_value_justification():
    """
    Checks the pull request body for a valid Value Justification.
    """
    pr_body = os.getenv("PR_BODY")
    if not pr_body:
        print("PR_BODY environment variable not set.")
        sys.exit(1)

    # Find the Value Justification section
    value_justification_section = ""
    for line in pr_body.splitlines():
        if line.startswith("**Value Justification:**"):
            value_justification_section = line.split(":", 1)[1].strip()
            break

    if not value_justification_section:
        print("Value Justification section not found in PR body.")
        sys.exit(1)

    # Check for keywords or the [DERIVED] prefix
    keywords = ["increase", "decrease", "reduce", "measure", "achieve", "optimize"]
    if any(keyword in value_justification_section.lower() for keyword in keywords) or value_justification_section.lower().startswith("[derived]"):
        print("Value Justification is valid.")
        sys.exit(0)
    else:
        print("Value Justification must contain a keyword or the [DERIVED] prefix.")
        sys.exit(1)

if __name__ == "__main__":
    check_value_justification()
