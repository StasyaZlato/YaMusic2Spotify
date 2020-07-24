import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

SCOPE = 'user-library-read'
SCOPE_SAVE = 'user-library-modify'

CLIENT_ID = 'client_app_id'
CLIENT_SECRET = 'client_secret_id'
USERNAME = 'your_spotify_username'

REDIRECT_URI = 'http://localhost:8888/callback'


def search_track(track_info, sp):
    title = track_info['title']
    artists = " ".join(track_info['artists'])

    query = "{0} {1}".format(artists, title)

    return sp.search(q=query, limit=1, type='track')


def divide_chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def search_tracks(tracks_info, sp):
    search_results = []
    for track in tracks_info:
        print("{0} - {1}".format(track['title'], ", ".join(track['artists'])))
        res = search_track(track, sp)
        if len(res['tracks']['items']) > 0:
            search_results.append(res['tracks']['items'][0]['id'])

    print(len(search_results))

    return list(divide_chunks(search_results, 50))


def add_track(search_results, sp_save):
    for sr in search_results:
        sp_save.current_user_saved_tracks_add(tracks=sr)


def main():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE,
                                                   client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   username=USERNAME))

    sp_save = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE_SAVE,
                                                        client_id=CLIENT_ID,
                                                        client_secret=CLIENT_SECRET,
                                                        redirect_uri=REDIRECT_URI,
                                                        username=USERNAME))

    with open("yamusic_likes.json", "r", encoding="utf-8") as f:
        js = json.loads(f.read())

    search_results = search_tracks(js, sp)
    add_track(search_results, sp_save)


main()
