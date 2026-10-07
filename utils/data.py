"""Test data helpers. Every test creates its own user so tests are independent and can run in any order."""
import uuid

DEFAULT_PASSWORD = "Test@12345"


def unique_email(prefix: str = "qa") -> str:
    return f"{prefix}.{uuid.uuid4().hex[:10]}@test.local"


def registration_payload(email: str, password: str = DEFAULT_PASSWORD) -> dict:
    return {
        "email": email,
        "password": password,
        "passwordRepeat": password,
        "securityQuestion": {"id": 1},
        "securityAnswer": "qa-answer",
    }
