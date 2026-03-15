from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
import json

# Project modules
from src.music_loader import load_music
from src.data_loader import load_movies, load_users, load_history, save_history
from src.recommender import recommend_movies

app = Flask(__name__)
app.secret_key = "vibe_secret_key"


# ================= LANDING PAGE =================
@app.route("/")
def landing():
    return render_template("landing.html")


# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        users = load_users()

        user = users[users.username == username]

        if not user.empty:
            if check_password_hash(user.iloc[0]["password"], password):
                session["user"] = user.iloc[0].to_dict()
                return redirect("/home")

    return render_template("login.html")


# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        users = load_users()

        new_user = {
            "user_id": len(users) + 1,
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "age": request.form.get("age"),
            "preferred_language": request.form.get("language"),
            "preferred_genre": request.form.get("genre"),
            "region": request.form.get("region"),
            "signup_date": date.today()
        }

        users = users._append(new_user, ignore_index=True)
        users.to_csv("data/users.csv", index=False)

        return redirect("/login")

    return render_template("signup.html")


# ================= HOME PAGE =================
@app.route("/home")
def home():

    if "user" not in session:
        return redirect("/login")

    movies = load_movies()
    history = load_history()
    user = session["user"]

    genre = request.args.get("genre")
    language = request.args.get("language")

    genres = sorted(movies["genre"].dropna().unique())
    languages = sorted(movies["language"].dropna().unique())

    filtered_movies = movies.copy()

    if genre:
        filtered_movies = filtered_movies[filtered_movies["genre"] == genre]

    if language:
        filtered_movies = filtered_movies[filtered_movies["language"] == language]

    recommended = recommend_movies(movies, user, history)

    hero_movies = recommended.head(5).to_dict("records")

    return render_template(
        "index.html",
        hero_movies=hero_movies,
        hero_movie=hero_movies[0] if hero_movies else None,
        recommended_movies=filtered_movies.to_dict("records"),
        popular_movies=movies.sort_values(
            "popularity_score", ascending=False
        ).to_dict("records"),
        all_movies=movies.to_dict("records"),
        genres=genres,
        languages=languages,
        selected_genre=genre,
        selected_language=language
    )


# ================= MOVIES TAB =================
@app.route("/movies")
def movies():
    return redirect("/home")


# ================= MOVIE DETAIL =================
@app.route("/movie/<int:movie_id>")
def movie_detail(movie_id):

    movies = load_movies()

    movie = movies[movies.movie_id == movie_id].iloc[0]

    if "user" in session:

        save_history({
            "user_id": session["user"]["user_id"],
            "movie_id": movie_id,
            "watch_count": 1,
            "last_watched": date.today()
        })

    return render_template("movie_detail.html", movie=movie)


# ================= MUSIC PAGE =================
@app.route("/music", methods=["GET", "POST"])
def music():

    music_df = load_music()
    songs = music_df.to_dict("records")

    if request.method == "POST":

        q = request.form.get("song", "").lower()

        if q:
            songs = music_df[
                music_df["title"].str.lower().str.contains(q, na=False)
            ].to_dict("records")

    return render_template("music.html", songs=songs)


# ================= SHOWS PAGE =================
@app.route("/shows")
def shows():
    return render_template("shows.html")


# ================= GAMES PAGE =================
@app.route("/games")
def games():

    games_list = [
        {"title": "Slope", "url": "https://www.crazygames.com/embed/slope"},
        {"title": "2048", "url": "https://www.crazygames.com/embed/2048"},
        {"title": "Basketball Stars", "url": "https://www.crazygames.com/embed/basketball-stars"},
        {"title": "Drift Boss", "url": "https://www.crazygames.com/embed/drift-boss"},
        {"title": "Subway Surfers", "url": "https://www.crazygames.com/embed/subway-surfers"},
        {"title": "Moto X3M", "url": "https://www.crazygames.com/embed/moto-x3m"},
        {"title": "Stickman Hook", "url": "https://www.crazygames.com/embed/stickman-hook"},
        {"title": "Run 3", "url": "https://www.crazygames.com/embed/run-3"}
    ]

    # Generate dynamic images
    for g in games_list:
        g["image"] = f"https://image.pollinations.ai/prompt/{g['title']}%20game%20cover"

    return render_template("games.html", games=games_list)


# ================= GAME PLAYER =================
@app.route("/play")
def play():

    url = request.args.get("url")

    return render_template("game_player.html", game_url=url)


# ================= LIVE SEARCH =================
@app.route("/live-search")
def live_search():

    q = request.args.get("q", "").lower()

    if len(q) < 2:
        return jsonify([])

    movies = load_movies()

    results = movies[
        movies["title"].str.lower().str.contains(q, na=False)
    ][["movie_id", "title"]].head(8)

    return jsonify([
        {"id": int(r.movie_id), "title": r.title}
        for r in results.itertuples()
    ])


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ================= RUN SERVER =================
if __name__ == "__main__":
    app.run(debug=True)