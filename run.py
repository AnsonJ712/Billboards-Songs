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

    if sys.argv[1] == "R&B/Hip-Hop":
        link = "https://www.billboard.com/charts/r-b-hip-hop-songs"
    elif sys.argv[1] == "Dance/Electronic":
        link = "https://www.billboard.com/charts/dance-electronic-songs"
    elif sys.argv[1] == "Country":
        link = "https://www.billboard.com/charts/country-songs"
    elif sys.argv[1] == "Rock":
        link = "https://www.billboard.com/charts/rock-songs"
    elif sys.argv[1] == "Latin":
        link = "https://www.billboard.com/charts/latin-songs"
    elif sys.argv[1] == "Pop":
        link = "https://www.billboard.com/charts/pop-songs"

    playlist_name = "Billboard " + sys.argv[1] + " Songs"

    scope = 'playlist-modify-private playlist-modify'

    charts = Billboard(link)
    page = charts.get_page()
    soup = charts.parse_page(page)
    artists = charts.get_tracks_from_billboard(soup)[0]
    songs = charts.get_tracks_from_billboard(soup)[1]

    spotify = Spotify(scope)
    user = spotify.authenticate(ACCOUNT)[0]
    sp = spotify.authenticate(ACCOUNT)[1]
    spotify.add_to_playlist(sp, user, artists, songs, playlist_name)

    print("Done!")


if __name__ == "__main__":
    main()
