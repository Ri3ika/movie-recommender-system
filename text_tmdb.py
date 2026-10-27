import os
import requests

API_KEY = os.getenv("TMDB_API_KEY") or input("Paste your TMDB API key: ").strip()
HOSTS = ["https://api.themoviedb.org", "https://api.tmdb.org"]
IMAGE_URL = "https://image.tmdb.org/t/p/w92/9O7gLzmreU0nGkIB6K3BsJbzvNv.jpg"

for host in HOSTS:
    try:
        r = requests.get(f"{host}/3/movie/550", params={"api_key": API_KEY}, timeout=8)
        print(f"{host} -> status {r.status_code}", "(OK)" if r.status_code == 200 else r.text[:100])
    except requests.RequestException as e:
        print(f"{host} -> FAIL: {type(e).__name__}")

try:
    r = requests.get(IMAGE_URL, timeout=8)
    print(f"image.tmdb.org -> status {r.status_code}")
except requests.RequestException as e:
    print(f"image.tmdb.org -> FAIL: {type(e).__name__}")