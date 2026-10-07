"""Thin wrapper over requests so tests read like specs, not HTTP plumbing."""
from dataclasses import dataclass, field

import requests

from utils.data import DEFAULT_PASSWORD, registration_payload, unique_email


@dataclass
class ApiClient:
    base_url: str
    token: str | None = None
    session: requests.Session = field(default_factory=requests.Session)

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def get(self, path, **kw):
        return self.session.get(self.base_url + path, headers=self._headers(), timeout=15, **kw)

    def post(self, path, json=None, **kw):
        return self.session.post(self.base_url + path, json=json, headers=self._headers(), timeout=15, **kw)

    def put(self, path, json=None, **kw):
        return self.session.put(self.base_url + path, json=json, headers=self._headers(), timeout=15, **kw)

    def delete(self, path, **kw):
        return self.session.delete(self.base_url + path, headers=self._headers(), timeout=15, **kw)

    # --- domain helpers -------------------------------------------------
    def register(self, email: str | None = None, password: str = DEFAULT_PASSWORD) -> dict:
        email = email or unique_email()
        r = self.post("/api/Users/", json=registration_payload(email, password))
        assert r.status_code == 201, f"Registration failed: {r.status_code} {r.text}"
        return {"email": email, "password": password, "id": r.json()["data"]["id"]}

    def login(self, email: str, password: str) -> requests.Response:
        return self.post("/rest/user/login", json={"email": email, "password": password})

    def authenticate(self, email: str, password: str) -> dict:
        r = self.login(email, password)
        assert r.status_code == 200, f"Login failed: {r.status_code} {r.text}"
        auth = r.json()["authentication"]
        self.token = auth["token"]
        return auth  # {token, bid, umail}
