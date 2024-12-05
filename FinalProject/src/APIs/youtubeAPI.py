import requests

API_KEY = ""
BASE_URL = "https://www.googleapis.com/youtube/v3"

def search_videos(query, max_results=10, published_after=None):
    search_url = f"{BASE_URL}/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": API_KEY,
    }
    if published_after:
        params["publishedAfter"] = published_after

    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        raise Exception(f"Failed to fetch videos: {response.status_code}")
