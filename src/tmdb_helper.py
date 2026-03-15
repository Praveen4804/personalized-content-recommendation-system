# import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# from src.tmdb_config import TMDB_API_KEY

# SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
# IMAGE_BASE = "https://image.tmdb.org/t/p/original"

# # Create retry-safe session
# session = requests.Session()
# retries = Retry(
#     total=5,
#     backoff_factor=1,
#     status_forcelist=[429, 500, 502, 503, 504]
# )
# session.mount("https://", HTTPAdapter(max_retries=retries))

# def get_hd_banner(movie_title, year=None):
#     params = {
#         "api_key": TMDB_API_KEY,
#         "query": movie_title,
#         "include_adult": False
#     }

#     if year:
#         params["year"] = year

#     try:
#         res = session.get(
#             SEARCH_URL,
#             params=params,
#             timeout=15,
#             verify=False   # 🔑 SSL FIX
#         )

#         if res.status_code != 200:
#             return None

#         results = res.json().get("results")
#         if not results:
#             return None

#         backdrop = results[0].get("backdrop_path")
#         if backdrop:
#             return IMAGE_BASE + backdrop

#     except Exception as e:
#         print(f"⚠️ TMDB error for '{movie_title}': {e}")

#     return None
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.tmdb_config import TMDB_API_KEY

SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
VIDEO_URL = "https://api.themoviedb.org/3/movie/{movie_id}/videos"

POSTER_BASE = "https://image.tmdb.org/t/p/w500"
BANNER_BASE = "https://image.tmdb.org/t/p/original"
YOUTUBE_BASE = "https://www.youtube.com/embed/"

# Retry-safe session
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)
session.mount("https://", HTTPAdapter(max_retries=retries))


def get_tmdb_assets(title, year=None):
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "include_adult": False
    }
    if year:
        params["year"] = year

    try:
        res = session.get(
            SEARCH_URL,
            params=params,
            timeout=15,
            verify=False
        )

        if res.status_code != 200:
            return None, None, None

        results = res.json().get("results")
        if not results:
            return None, None, None

        movie = results[0]
        movie_id = movie["id"]

        poster = movie.get("poster_path")
        banner = movie.get("backdrop_path")

        poster_url = POSTER_BASE + poster if poster else None
        banner_url = BANNER_BASE + banner if banner else None

        # -------- FETCH TRAILER --------
        trailer_url = None
        video_res = session.get(
            VIDEO_URL.format(movie_id=movie_id),
            params={"api_key": TMDB_API_KEY},
            timeout=15,
            verify=False
        )

        if video_res.status_code == 200:
            videos = video_res.json().get("results", [])
            for v in videos:
                if (
                    v["site"] == "YouTube"
                    and v["type"] == "Trailer"
                ):
                    trailer_url = YOUTUBE_BASE + v["key"]
                    break

        return poster_url, banner_url, trailer_url

    except Exception as e:
        print(f"⚠️ TMDB error for '{title}': {e}")
        return None, None, None
