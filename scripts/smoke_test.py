"""Проверка настоящего HTTP-сервера; только стандартная библиотека Python."""
import json
import time
from urllib.error import URLError
from urllib.request import urlopen

BASE_URL = "http://127.0.0.1:8000"


def get_json(path):
    with urlopen(BASE_URL + path, timeout=3) as response:
        assert response.status == 200, response.status
        return json.load(response)


def main():
    for attempt in range(30):
        try:
            assert get_json("/health") == {"status": "ok"}
            break
        except (URLError, TimeoutError):
            if attempt == 29:
                raise
            time.sleep(1)
    assert get_json("/")["message"] == "VPe04: GitHub Actions + Docker"
    print("HTTP smoke test: OK")


if __name__ == "__main__":
    main()
