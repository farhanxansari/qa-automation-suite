"""Modules: Products, Basket, Access Control (API)"""
import pytest

from utils.schema import assert_schema

pytestmark = pytest.mark.api


# ---------- Products ----------
@pytest.mark.p0
def test_TC_API_PROD_01_product_list_matches_schema(api):
    r = api.get("/api/Products")
    assert r.status_code == 200
    products = r.json()["data"]
    assert len(products) > 0
    for p in products:
        assert_schema(p, "product")


@pytest.mark.p1
def test_TC_API_PROD_02_search_filters_by_term(api):
    data = api.get("/rest/products/search", params={"q": "juice"}).json()["data"]
    assert data, "Expected at least one juice product"
    for p in data:
        assert "juice" in (p["name"] + p["description"]).lower()


@pytest.mark.p2
def test_TC_API_PROD_03_response_time_under_threshold(api):
    r = api.get("/api/Products")
    assert r.elapsed.total_seconds() < 2.0


# ---------- Basket ----------
@pytest.mark.p0
def test_TC_API_BASKET_01_add_item_to_own_basket(auth_api):
    r = auth_api.post("/api/BasketItems/", json={"ProductId": 1, "BasketId": str(auth_api.bid), "quantity": 1})
    assert r.status_code == 200, r.text
    basket = auth_api.get(f"/rest/basket/{auth_api.bid}").json()["data"]
    assert any(p["id"] == 1 for p in basket["Products"])


@pytest.mark.p1
@pytest.mark.parametrize("qty", [0, -1])
@pytest.mark.xfail(reason="BUG-004: Basket quantity accepts zero/negative values (negative order total)")
def test_TC_API_BASKET_02_quantity_boundary_rejected(auth_api, qty):
    item = auth_api.post("/api/BasketItems/", json={"ProductId": 2, "BasketId": str(auth_api.bid), "quantity": 1}).json()["data"]
    r = auth_api.put(f"/api/BasketItems/{item['id']}", json={"quantity": qty})
    assert r.status_code == 400


# ---------- Access control ----------
@pytest.mark.p0
@pytest.mark.security
@pytest.mark.xfail(reason="BUG-005: IDOR - any logged-in user can read another user's basket")
def test_TC_API_ACCESS_01_cannot_read_other_users_basket(auth_api, base_url):
    from utils.api_client import ApiClient
    other = ApiClient(base_url)
    u = other.register()
    other_bid = other.authenticate(u["email"], u["password"])["bid"]
    r = auth_api.get(f"/rest/basket/{other_bid}")
    assert r.status_code in (401, 403)


@pytest.mark.p0
@pytest.mark.security
@pytest.mark.xfail(reason="BUG-006: Non-admin user can list all registered users' emails")
def test_TC_API_ACCESS_02_normal_user_cannot_list_all_users(auth_api):
    r = auth_api.get("/api/Users")
    assert r.status_code == 403


@pytest.mark.p1
@pytest.mark.security
@pytest.mark.xfail(reason="BUG-007: /ftp exposes confidential files via directory listing")
def test_TC_API_ACCESS_03_ftp_directory_not_publicly_listed(api):
    r = api.get("/ftp/")
    assert r.status_code in (401, 403, 404)
