"""Modules: Product Search, Admin Access Control (UI)"""
import re
import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.search_page import SearchPage

pytestmark = pytest.mark.ui


@pytest.mark.p1
def test_TC_SEARCH_01_search_returns_matching_products(page):
    results = SearchPage(page).search("apple")
    expect(results.product_names.first).to_be_visible()
    for name in results.product_names.all_inner_texts():
        assert "apple" in name.lower()


@pytest.mark.p2
def test_TC_SEARCH_02_no_results_for_gibberish(page):
    results = SearchPage(page).search("zzqqxxnotaproduct")
    expect(page.get_by_text("No results found")).to_be_visible()
    expect(results.product_names).to_have_count(0)


@pytest.mark.p0
@pytest.mark.security
@pytest.mark.xfail(reason="BUG-002: Reflected DOM XSS via search query parameter")
def test_TC_SEARCH_03_search_term_is_not_executed_as_html(page):
    dialogs = []
    page.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))
    SearchPage(page).search('<iframe src="javascript:alert(`xss`)">')
    page.wait_for_timeout(1500)
    assert dialogs == [], f"Injected script executed: {dialogs}"


@pytest.mark.p0
@pytest.mark.security
def test_TC_ACCESS_01_normal_user_cannot_open_admin_page(page, user):
    LoginPage(page).open().login(user["email"], user["password"])
    expect(page).to_have_url(re.compile(r"/search"))
    page.goto("/#/administration")
    page.wait_for_timeout(1000)
    expect(page.get_by_text("Registered Users")).not_to_be_visible()
