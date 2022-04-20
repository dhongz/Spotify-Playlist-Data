
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import numpy as np

sp = spotipy.Spotify(auth_manager= SpotifyOAuth(client_id="7ae0264a93f344aab5b3910711af2097",
                                               client_secret="2266135786b3428485b962c68ee6df6f",
                                               redirect_uri="https://www.spotify.com/us/",
                                               scope="user-library-read")
                                               , requests_session = True, requests_timeout=1800)

# Initialize data frames and variables
data = pd.DataFrame({

    "user": [],
    "user_id": [],
    "song": [],
    "artist": [],
    "song_popularity": [],
    "artist_popularity": [],
    "danceability": [],
    "energy": [],
    "key": [],
    "loudness": [],
    "mode": [],
    "speechiness": [],
    "acousticness": [],
    "instrumentalness": [],
    "liveness": [],
    "valence": [],
    "tempo": [],
    "time_signature": [],
    "genres": []
})

user_id = int(0)
isTrack = True

users_nodup = pd.read_excel('spotifyusernames.xlsx', sheet_name="Combined")
users_nodup = users_nodup.reset_index()

# Remove duplicate users
users = []
for index, row in users_nodup.iterrows():
    if row['Usernames'] not in users:
        users.append(str(row['Usernames']))

# Loop through data
for user in users:
    sp = spotipy.Spotify(auth_manager= SpotifyOAuth(client_id="7ae0264a93f344aab5b3910711af2097",
                                               client_secret="2266135786b3428485b962c68ee6df6f",
                                               redirect_uri="https://www.spotify.com/us/",
                                               scope="user-library-read")
                                               , requests_session = True, requests_timeout=1800)
    try:
        sp._get("https://api.spotify.com/v1/users/" + str(user))
    except:
        print(user + "does not exist.")
        continue
    playlists = sp.user_playlists(user, 6)
    for playlist in playlists['items']:
        tracks = sp.playlist_items(playlist['id'])
        for track in tracks['items']:
            newdata = pd.DataFrame({
                "user": [],
                "user_id": [],
                "song": [],
                "artist": [],
                "song_popularity": [],
                "artist_popularity": [],
                "danceability": [],
                "energy": [],
                "key": [],
                "loudness": [],
                "mode": [],
                "speechiness": [],
                "acousticness": [],
                "instrumentalness": [],
                "liveness": [],
                "valence": [],
                "tempo": [],
                "time_signature": [],
                "genres": []
            })

            if track['track'] != None:
                song = track['track']['name']
                song_id = track['track']['id']
                if song_id != None:
                    isTrack = track['track']['track']
                    if isTrack:
                        popularity = track['track']['popularity']
                        artists = track['track']['album']['artists']
                        combo_artist = []
                        combo_artist_popularity = []
                        combo_genres = []
                        for artist in artists:
                                art = sp.artist(artist['id'])
                                combo_artist.append(artist['name']) 
                                combo_artist_popularity.append(art['popularity']) 
                                for genre in art['genres']:
                                    combo_genres.append(genre)
                        artist_popularity = np.average(combo_artist_popularity)
                        af = sp.audio_features(song_id)
                        audio_features = af[0]
                        if audio_features != None:
                            newdata = pd.DataFrame({
                                "user": [user],
                                "user_id": [user_id],
                                "song": [song],
                                "artist": [combo_artist],
                                "song_popularity": [popularity],
                                "artist_popularity": [artist_popularity],
                                "danceability": [audio_features["danceability"]],
                                "energy": [audio_features["energy"]],
                                "key": [audio_features["key"]],
                                "loudness": [audio_features["loudness"]],
                                "mode": [audio_features["mode"]],
                                "speechiness": [audio_features["speechiness"]],
                                "acousticness": [audio_features["acousticness"]],
                                "instrumentalness": [audio_features["instrumentalness"]],
                                "liveness": [audio_features["liveness"]],
                                "valence": [audio_features["valence"]],
                                "tempo": [audio_features["tempo"]],
                                "time_signature": [audio_features["time_signature"]],
                                "genres": [combo_genres]
                            })
                            data = pd.concat([data, newdata])
                        else:
                            newdata = pd.DataFrame({
                                "user": [user],
                                "user_id": [user_id],
                                "song": [song],
                                "artist": [combo_artist],
                                "song_popularity": [popularity],
                                "artist_popularity": [artist_popularity],
                                "danceability": [float("NaN")],
                                "energy": [float("NaN")],
                                "key": [float("NaN")],
                                "loudness": [float("NaN")],
                                "mode": [float("NaN")],
                                "speechiness": [float("NaN")],
                                "acousticness": [float("NaN")],
                                "instrumentalness": [float("NaN")],
                                "liveness": [float("NaN")],
                                "valence": [float("NaN")],
                                "tempo": [float("NaN")],
                                "time_signature": [float("NaN")],
                                "genres": [combo_genres]
                            })
                            data = pd.concat([data, newdata])
    print("################################################################################")
    print(user)
    user_id += int(1)

data.to_excel("spotifyannarbordata.xlsx")
#data.to_csv(r'/Users/dillonhong/Desktop/spotifyannarbordata_two.csv', index=False, header=True)
