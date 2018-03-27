import os
import sys

from Billboard import Billboard
from Spotipy import Spotipy


def main():
    os.environ['SPOTIPY_CLIENT_ID'] = 'fa7711b32c9047849df65cfd7ce8c634'
    os.environ['SPOTIPY_CLIENT_SECRET'] = '6c45a93d8d3e496181d1f37cb6b3d98d'
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888'

    global link, playlist_name

    if sys.argv[2] == "Hip-Hop":
        link = "https://www.billboard.com/charts/r-b-hip-hop-songs"
        playlist_name = "Billboard R&B/Hip-Hop Songs"
    elif sys.argv[2] == "Dance":
        link = "https://www.billboard.com/charts/dance-electronic-songs"
        playlist_name = "Billboard Dance/Electronic Songs"

    scope = 'playlist-modify-private playlist-modify'

    charts = Billboard(link)
    page = charts.get_page(link)
    soup = charts.parse_page(page)
    artists = charts.get_tracks_from_billboard(soup)[0]
    songs = charts.get_tracks_from_billboard(soup)[1]

    spotify = Spotipy(scope)
    user = spotify.authenticate(scope)[0]
    sp = spotify.authenticate(scope)[1]
    spotify.add_to_playlist(sp, user, artists, songs, playlist_name)

    print "Done!"


if __name__ == "__main__":
    main()
