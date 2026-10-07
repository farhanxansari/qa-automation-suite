"""Module: Security headers (API)"""
import pytest

pytestmark = [pytest.mark.api, pytest.mark.security]


@pytest.mark.p1
@pytest.mark.parametrize("header,allowed", [
    ("X-Content-Type-Options", ["nosniff"]),
    ("X-Frame-Options", ["DENY", "SAMEORIGIN"]),
])
def test_TC_API_HDR_01_security_header_has_safe_value(api, header, allowed):
    r = api.get("/")
    assert header in r.headers, f"Missing security header: {header}"
    assert r.headers[header].upper() in [v.upper() for v in allowed]


@pytest.mark.p1
@pytest.mark.xfail(reason="BUG-008: Content-Security-Policy header missing (no browser-side XSS mitigation)")
def test_TC_API_HDR_02_csp_header_present(api):
    r = api.get("/")
    assert "Content-Security-Policy" in r.headers


@pytest.mark.p2
def test_TC_API_HDR_03_server_does_not_leak_tech_stack(api):
    r = api.get("/")
    assert "X-Powered-By" not in r.headers, f"Leaks stack: {r.headers.get('X-Powered-By')}"


@pytest.mark.p2
@pytest.mark.skip(reason="HSTS only applies over HTTPS; test environment is served over HTTP")
def test_TC_API_HDR_04_hsts_header_present(api):
    r = api.get("/")
    assert "Strict-Transport-Security" in r.headers