import os
import sys

from billboard import Billboard
from spotify import Spotify


def main():
    os.environ['SPOTIPY_CLIENT_ID'] = 'fa7711b32c9047849df65cfd7ce8c634'
    os.environ['SPOTIPY_CLIENT_SECRET'] = '6c45a93d8d3e496181d1f37cb6b3d98d'
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888'

    global link, playlist_name

    if sys.argv[2] == "Hip-Hop":
        link = "https://www.billboard.com/charts/r-b-hip-hop-songs"
    elif sys.argv[2] == "Dance/Electronic":
        link = "https://www.billboard.com/charts/dance-electronic-songs"
    elif sys.argv[2] == "Country":
        link = "https://www.billboard.com/charts/country-songs"
    elif sys.argv[2] == "Rock":
        link = "https://www.billboard.com/charts/rock-songs"
    elif sys.argv[2] == "Latin":
        link = "https://www.billboard.com/charts/latin-songs"
    elif sys.argv[2] == "Pop":
        link = "https://www.billboard.com/charts/pop-songs"

    playlist_name = "Billboard " + sys.argv[2] + " Songs"

    scope = 'playlist-modify-private playlist-modify'

    charts = Billboard(link)
    page = charts.get_page()
    soup = charts.parse_page(page)
    artists = charts.get_tracks_from_billboard(soup)[0]
    songs = charts.get_tracks_from_billboard(soup)[1]

    spotify = Spotify(scope)
    user = spotify.authenticate(sys.argv[1])[0]
    sp = spotify.authenticate(sys.argv[1])[1]
    spotify.add_to_playlist(sp, user, artists, songs, playlist_name)

    print("Done!")


if __name__ == "__main__":
    main()
