# import pandas as pd

# MOVIE_PATH = "data/movies.csv"
# USER_PATH = "data/users.csv"
# HISTORY_PATH = "data/viewing_history.csv"


# def load_movies():
#     return pd.read_csv(MOVIE_PATH)


# def load_users():
#     return pd.read_csv(USER_PATH)


# def load_history():
#     return pd.read_csv(HISTORY_PATH)


# def save_user(user):
#     df = load_users()
#     df = pd.concat([df, pd.DataFrame([user])])
#     df.to_csv(USER_PATH, index=False)


# def save_history(entry):
#     df = load_history()
#     df = pd.concat([df, pd.DataFrame([entry])])
#     df.to_csv(HISTORY_PATH, index=False)
import pandas as pd

def load_movies():
    return pd.read_csv("data/movies.csv")

def load_users():
    return pd.read_csv("data/users.csv")

def load_history():
    return pd.read_csv("data/viewing_history.csv")

def save_history(entry):
    df = load_history()
    df = pd.concat([df, pd.DataFrame([entry])])
    df.to_csv("data/viewing_history.csv", index=False)
