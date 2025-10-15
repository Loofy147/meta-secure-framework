from urllib.parse import urlparse

def is_blocked(url: str) -> bool:
    """
    Simulates a security check that blocklists a specific domain.
    This function is vulnerable to CVE-2023-24329.
    """
    if not isinstance(url, str):
        return False

    blocked_domain = "evil.com"

    # The vulnerability is in how urlparse handles leading whitespace
    parsed_url = urlparse(url)

    if parsed_url.hostname == blocked_domain:
        print(f"[-] Blocked access to {parsed_url.hostname}")
        return True

    print(f"[+] Allowed access to {parsed_url.hostname}")
    return False

def main():
    """Demonstrates the vulnerability."""

    # Expected behavior: Block the malicious URL
    print("Testing standard blocked URL:")
    is_blocked("http://evil.com/path")

    # The exploit: Bypass the blocklist with leading whitespace
    print("\nTesting bypass with leading whitespace (CVE-2023-24329):")
    is_blocked(" http://evil.com/path")

if __name__ == "__main__":
    main()
