import os
import sys
import json

def check_security_signoff():
    """
    Checks the knowledge hub for a threat model and verifies its sign-off status.
    """
    pr_body = os.getenv("PR_BODY")
    if not pr_body:
        print("PR_BODY environment variable not set.")
        sys.exit(1)

    # Find the Epic ID from the PR body
    epic_id = ""
    for line in pr_body.splitlines():
        if line.startswith("**Epic:**"):
            epic_id = line.split(":", 1)[1].strip()
            break

    if not epic_id:
        print("Epic ID not found in PR body.")
        sys.exit(1)

    # Load the knowledge hub
    try:
        with open("knowledge_hub.json", "r") as f:
            knowledge_hub = json.load(f)
    except FileNotFoundError:
        print("knowledge_hub.json not found.")
        sys.exit(1)

    # Find the threat model for the epic
    threat_model_path = knowledge_hub.get(epic_id, {}).get("threat_model")
    if not threat_model_path:
        print(f"Threat model not found for Epic {epic_id} in knowledge_hub.json.")
        sys.exit(1)

    # Check for the sign-off in the threat model
    try:
        with open(threat_model_path, "r") as f:
            threat_model_content = f.read()
            if "Signed-off-by" in threat_model_content:
                print("Security Sign-Off is valid.")
                sys.exit(0)
            else:
                print(f"Security Sign-Off not found in {threat_model_path}.")
                sys.exit(1)
    except FileNotFoundError:
        print(f"Threat model file not found: {threat_model_path}")
        sys.exit(1)

if __name__ == "__main__":
    check_security_signoff()
