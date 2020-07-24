from yandex_music.client import Client
import json

USER_MAIL = 'your_ya_music_login'
USER_PASSWORD = 'your_ya_music_password'

client = Client.from_credentials(USER_MAIL, USER_PASSWORD)

tracks = client.users_likes_tracks().tracks

tracks_info = []

for track in tracks:
    full_track = track.track
    title = full_track.title
    artists = []
    albums = []
    for artist in full_track.artists:
        artists.append(artist.name)

    for album in full_track.albums:
        albums.append(album.title)

    dict_track = {'title': title,
                  'artists': artists,
                  'albums': albums}

    tracks_info.append(dict_track)

with open("yamusic_likes.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(tracks_info, indent=True, ensure_ascii=False))


