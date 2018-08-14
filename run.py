import os
import sys

from billboard import Billboard
from spotify import Spotify

from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, ACCOUNT

def main():
    os.environ['SPOTIPY_CLIENT_ID'] = CLIENT_ID
    os.environ['SPOTIPY_CLIENT_SECRET'] = CLIENT_SECRET
    os.environ['SPOTIPY_REDIRECT_URI'] = REDIRECT_URI

    global link, playlist_name

    link = sys.argv[1]

    scope = 'playlist-modify-private playlist-modify'

    charts = Billboard(link)
    page = charts.get_page()
    soup = charts.parse_page(page)
    artists = charts.get_tracks_from_billboard(soup)[0]
    songs = charts.get_tracks_from_billboard(soup)[1]
    chart_name = charts.get_tracks_from_billboard(soup)[2]

    playlist_name = "Billboard " + chart_name.get_text().title()

    spotify = Spotify(scope)
    user = spotify.authenticate(ACCOUNT)[0]
    sp = spotify.authenticate(ACCOUNT)[1]
    spotify.add_to_playlist(sp, user, artists, songs, playlist_name)

    print("Done!")


if __name__ == "__main__":
    main()
