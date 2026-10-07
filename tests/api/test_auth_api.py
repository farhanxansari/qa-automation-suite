"""Module: Authentication API"""
import pytest

from utils.data import registration_payload, unique_email
from utils.schema import assert_schema

pytestmark = pytest.mark.api


@pytest.mark.p0
def test_TC_API_AUTH_01_login_returns_valid_token_contract(api, user):
    r = api.login(user["email"], user["password"])
    assert r.status_code == 200
    assert_schema(r.json(), "login_response")
    assert r.json()["authentication"]["umail"] == user["email"]


@pytest.mark.p0
@pytest.mark.parametrize("email,password", [
    ("nobody@test.local", "Test@12345"),   # unknown user
    ("", ""),                              # empty
])
def test_TC_API_AUTH_02_invalid_login_returns_401(api, email, password):
    r = api.login(email, password)
    assert r.status_code == 401
    assert "token" not in r.text


@pytest.mark.p1
def test_TC_API_AUTH_03_duplicate_email_registration_rejected(api, user):
    r = api.post("/api/Users/", json=registration_payload(user["email"]))
    assert r.status_code == 400


@pytest.mark.p0
def test_TC_API_AUTH_04_protected_endpoint_requires_token(api):
    r = api.get("/rest/user/whoami")
    assert r.status_code == 200 and r.json().get("user") == {}, "Anonymous whoami must not reveal a user"
    assert api.get("/api/Users").status_code == 401


@pytest.mark.p1
def test_TC_API_AUTH_05_tampered_token_rejected(auth_api):
    auth_api.token = auth_api.token[:-4] + "abcd"
    assert auth_api.get("/api/Users").status_code == 401


@pytest.mark.p0
@pytest.mark.security
@pytest.mark.xfail(reason="BUG-001: SQL injection in login email field bypasses authentication")
def test_TC_API_AUTH_06_sql_injection_rejected(api):
    r = api.login("' OR 1=1--", "x")
    assert r.status_code == 401


@pytest.mark.p2
@pytest.mark.xfail(reason="BUG-003: Registration accepts malformed email addresses")
def test_TC_API_AUTH_07_registration_rejects_malformed_email(api):
    r = api.post("/api/Users/", json=registration_payload("not-an-email-" + unique_email().split("@")[0]))
    assert r.status_code == 400
