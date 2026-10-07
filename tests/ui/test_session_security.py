"""Module: Session security (UI)"""
import re

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, pytest.mark.security]


def _login_and_get_token_cookie(page, user):
    LoginPage(page).open().login(user["email"], user["password"])
    expect(page).to_have_url(re.compile(r"/search"))
    return next((c for c in page.context.cookies() if c["name"] == "token"), None)


@pytest.mark.p1
@pytest.mark.xfail(reason="BUG-009: Session token cookie missing HttpOnly flag (readable by JavaScript)")
def test_TC_SESSION_01_token_cookie_is_httponly(page, user):
    token = _login_and_get_token_cookie(page, user)
    assert token is not None, "Expected a 'token' cookie after login"
    assert token["httpOnly"], "Session token is readable by JavaScript"