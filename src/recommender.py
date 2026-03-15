# def recommend_movies(movies, user, history):
#     movies = movies.copy()
#     movies["score"] = 0

#     # Preference-based
#     movies.loc[movies.genre == user["preferred_genre"], "score"] += 4
#     movies.loc[movies.language == user["preferred_language"], "score"] += 3
#     movies.loc[movies.region == user["region"], "score"] += 2

#     # Viewing history learning
#     user_history = history[history.user_id == user["user_id"]]

#     if not user_history.empty:
#         watched_ids = user_history.movie_id.tolist()
#         watched_movies = movies[movies.movie_id.isin(watched_ids)]

#         fav_genres = watched_movies.genre.unique()
#         fav_languages = watched_movies.language.unique()

#         movies.loc[movies.genre.isin(fav_genres), "score"] += 5
#         movies.loc[movies.language.isin(fav_languages), "score"] += 3

#     # Popularity fallback
#     movies["score"] += movies["popularity_score"] / 20

#     return movies.sort_values("score", ascending=False)
import pandas as pd

def recommend_movies(movies, user, history):
    movies = movies.copy()
    movies["score"] = 0.0

    #  Signup preferences (cold start)
    movies.loc[movies["genre"] == user["preferred_genre"], "score"] += 3
    movies.loc[movies["language"] == user["preferred_language"], "score"] += 3
    movies.loc[movies["region"] == user["region"], "score"] += 2

    #  Viewing history (strong signal)
    user_history = history[history["user_id"] == user["user_id"]]

    if not user_history.empty:
        watched_ids = user_history["movie_id"].tolist()
        watched_movies = movies[movies["movie_id"].isin(watched_ids)]

        fav_genres = watched_movies["genre"].value_counts()
        fav_languages = watched_movies["language"].value_counts()

        for genre, count in fav_genres.items():
            movies.loc[movies["genre"] == genre, "score"] += count * 5

        for lang, count in fav_languages.items():
            movies.loc[movies["language"] == lang, "score"] += count * 3

        # Remove already watched movies
        movies = movies[~movies["movie_id"].isin(watched_ids)]

    # Popularity fallback
    movies["score"] += movies["popularity_score"] / 20

    return movies.sort_values("score", ascending=False)
