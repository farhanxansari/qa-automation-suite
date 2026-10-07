import pytest

from utils.api_client import ApiClient


# ---------- API fixtures ----------
@pytest.fixture
def api(base_url) -> ApiClient:
    """Unauthenticated client."""
    return ApiClient(base_url)


@pytest.fixture
def user(base_url) -> dict:
    """A freshly registered user (email, password, id)."""
    return ApiClient(base_url).register()


@pytest.fixture
def auth_api(base_url, user) -> ApiClient:
    """Client logged in as a fresh user. Basket id available as auth_api.bid."""
    client = ApiClient(base_url)
    auth = client.authenticate(user["email"], user["password"])
    client.bid = auth["bid"]
    client.user = user
    return client


# ---------- UI fixtures ----------
@pytest.fixture
def browser_context_args(browser_context_args, base_url):
    return {**browser_context_args, "base_url": base_url, "viewport": {"width": 1366, "height": 900}}


@pytest.fixture
def context(context, base_url):
    # Pre-dismiss the welcome banner + cookie consent so they don't intercept clicks.
    domain = base_url.split("//")[1].split(":")[0]
    context.add_cookies([
        {"name": "welcomebanner_status", "value": "dismiss", "domain": domain, "path": "/"},
        {"name": "cookieconsent_status", "value": "dismiss", "domain": domain, "path": "/"},
    ])
    return context
