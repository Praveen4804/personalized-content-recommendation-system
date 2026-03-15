# import pandas as pd
# from src.tmdb_helper import get_hd_banner
# import time

# CSV_PATH = "data/movies.csv"

# movies = pd.read_csv(CSV_PATH)

# updated_banners = []

# for index, row in movies.iterrows():
#     title = row["title"]
#     year = row.get("release_year")

#     print(f"Fetching TMDB banner for: {title}")

#     banner = get_hd_banner(title, year)

#     if banner:
#         updated_banners.append(banner)
#     else:
#         # fallback to existing banner if TMDB fails
#         updated_banners.append(row["banner_url"])

#     time.sleep(0.4)  # 🛑 TMDB rate-limit safety

# movies["banner_url"] = updated_banners
# movies.to_csv(CSV_PATH, index=False)

# print("✅ TMDB banner update completed safely")
import pandas as pd
import time
from src.tmdb_helper import get_tmdb_assets

CSV_PATH = "data/movies.csv"

movies = pd.read_csv(CSV_PATH)

new_posters = []
new_banners = []
new_trailers = []

for _, row in movies.iterrows():
    title = row["title"]
    year = row.get("release_year")

    print(f"Fetching TMDB assets for: {title}")

    poster, banner, trailer = get_tmdb_assets(title, year)

    new_posters.append(poster if poster else row["poster_url"])
    new_banners.append(banner if banner else row["banner_url"])
    new_trailers.append(trailer if trailer else row["trailer_url"])

    time.sleep(0.4)  # TMDB safe limit

movies["poster_url"] = new_posters
movies["banner_url"] = new_banners
movies["trailer_url"] = new_trailers

movies.to_csv(CSV_PATH, index=False)

print("✅ TMDB posters + banners + trailers updated successfully")
