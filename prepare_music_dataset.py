import pandas as pd

# load dataset
df = pd.read_csv("data/SpotifyFeatures.csv")

# keep only needed columns
df = df[["track_name", "artist_name", "genre"]]

# remove duplicates
df = df.drop_duplicates()

# rename columns
df = df.rename(columns={
    "track_name": "title",
    "artist_name": "artist"
})

# take first 150 songs for project demo
df = df.head(150)

# create new columns
df["music_id"] = range(1, len(df) + 1)
df["language"] = "English"
df["spotify_url"] = "https://open.spotify.com/search/" + df["title"].str.replace(" ", "%20")
df["image"] = "placeholder"

# reorder columns
df = df[["music_id", "title", "artist", "genre", "language", "spotify_url", "image"]]

# save new dataset
df.to_csv("data/music.csv", index=False)

print("music.csv created successfully")