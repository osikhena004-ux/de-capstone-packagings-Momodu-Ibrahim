import requests
from omnicart_pipeline.api_client import Client

class DummyResponse:
    def __init__(self, json_data, status=200):
        self._json = json_data
        self.status_code = status

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError(f"{self.status_code}")

class DummySession:
    def __init__(self, pages):
        self.pages = pages
        self.calls = 0

    def get(self, url, params=None, timeout=None):
        _ = (url, params, timeout)
        if self.calls < len(self.pages):
            resp = DummyResponse(self.pages[self.calls], status=200)
        else:
            resp = DummyResponse(json_data=[], status=200)
        self.calls += 1
        return resp

def test_get_products_pagination():
    pages = [
        [{"id": 1, "price": 10, "rating": {"count": 2}, "userId": 1} for _ in range(5)],
        [{"id": 6, "price": 20, "rating": {"count": 1}, "userId": 2}],
    ]
    client = Client(base_url="https://example.com",
                    page_limit=5, session=DummySession(pages))
    products = client.get_products()
    assert len(products) == 6

def test_get_users_simple():
    users = [{"id": 1, "username": "bob"}]
    client = Client(base_url="https://example.com",
                    page_limit=5, session=DummySession([users]))
    fetched = client.get_users()
    assert isinstance(fetched, list)
