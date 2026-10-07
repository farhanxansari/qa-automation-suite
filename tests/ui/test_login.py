"""Module: Login Flow (UI)"""
import re
import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@pytest.mark.p0
def test_TC_LOGIN_01_valid_credentials_log_user_in(page, user):
    LoginPage(page).open().login(user["email"], user["password"])
    expect(page).to_have_url(re.compile(r"/search"))
    expect(page.get_by_role("button", name="Show the shopping cart")).to_be_visible()


@pytest.mark.p0
def test_TC_LOGIN_02_wrong_password_shows_error(page, user):
    login = LoginPage(page).open()
    login.login(user["email"], "WrongPass!1")
    expect(login.error).to_have_text("Invalid email or password.")
    expect(page).to_have_url(re.compile(r"/login"))


@pytest.mark.p1
def test_TC_LOGIN_03_submit_disabled_with_empty_fields(page):
    login = LoginPage(page).open()
    expect(login.submit).to_be_disabled()


@pytest.mark.p0
@pytest.mark.security
@pytest.mark.xfail(reason="BUG-001: SQL injection in login email field bypasses authentication")
def test_TC_LOGIN_04_sql_injection_does_not_bypass_login(page):
    login = LoginPage(page).open()
    login.login("' OR 1=1--", "anything")
    expect(login.error).to_be_visible(timeout=3000)
