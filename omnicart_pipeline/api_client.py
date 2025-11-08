import requests
import time

class Client:
    def __init__(self, base_url: str, page_limit: int, session = None, max_retries = 3):
        self.base_url = base_url.rstrip("/")
        self.page_limit = int(page_limit)
        self.session = session or requests.Session()
        self.max_retries = max_retries

    def get_products(self, path, parameters):
        url = f"{self.base_url}{path}"
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.get(url, params = parameters, timeout = 10)
            except requests.RequestException:
                if attempt == self.max_retries:
                    raise
                time.sleep(3 ** attempt)
                continue

            if response.status_code == 200:
                return response.json()

            if response.status_code == (429, 500, 502, 503, 504) and attempt < self.max_retries:
                time.sleep(3 ** attempt)
                continue

            response.raise_for_status()
        return None

    def get_users(self):
        all_items = []
        offset = 0
        while True:
            parameters = {"limit": self.page_limit, "offset": offset}
            items = self.get_products("products", parameters = parameters)
            if not isinstance(items, list):
                raise ValueError("expected list from /products endpoint")
            all_items.extend(items)
            if len(items) < self.page_limit:
                break
            offset += self.page_limit
        return all_items
