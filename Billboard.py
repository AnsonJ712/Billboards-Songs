import requests
import sys
import re
from bs4 import BeautifulSoup

import spotipy
import spotipy.util as util


class Billboard():
    def __init__(self, link):
        self.link = link

    def get_page(self, link):
        return requests.get(link)

    def parse_page(self, page):
        return BeautifulSoup(page.content, 'html.parser')

    def get_tracks_from_billboard(self, soup):
        """
        Collects song titles from billboards.com
        """
        artists = soup.find_all(class_='chart-row__artist')
        songs = soup.find_all(class_='chart-row__song')
        return artists, songs


class Spotipy():
    def __init__(self, scope):
        self.scope = scope

    def authenticate(self, scope):
        """
        Grants permission for user to use Spotify's API
        """
        if len(sys.argv) > 1:
            username = sys.argv[1]
        else:
            print("Usage: %s username playlist-name" % (sys.argv[0],))
            sys.exit()

        token = util.prompt_for_user_token(username, scope)

        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
        else:
            print("Can't get token for", username)

        return username, sp

    def add_to_playlist(self, sp, user, artists, songs, playlist_name):
        playlist_id = self.get_playlist(sp, user, playlist_name)
        track_id = []
        for song in range(len(songs)):
            artist = artists[song].get_text().strip()
            artist = re.sub("([,*]|\s([X&+x]|(Featuring)|"
                            "(With)|(And))).*",
                            '',
                            artist).replace("'", "")
            song = songs[song].get_text().strip()
            print "Added " + song + " by " + artist
            if self.get_track_uri(sp, song, artist) is not None:
                track_id.append(self.get_track_uri(sp, song, artist))
        sp.user_playlist_replace_tracks(user, playlist_id, track_id)

    def get_playlist(self, sp, user, playlist_name):
        """
        Searches for playlist,
        Creates new playlist if not found
        """
        playlists = sp.user_playlists(user)

        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                print "Playlist found"
                return playlist_id

        print "Playlist does not exist, creating a new playlist"
        sp.user_playlist_create(user, playlist_name)
        return self.get_playlist()

    def get_track_uri(self, sp, song, artist):
        """
        Searches for song titles and adds them to the playlist
        """
        results = sp.search(q=song + " " + artist)
        for track_name in results['tracks']['items']:
            for artist_name in track_name['album']['artists']:
                if any(x in artist_name['name'].lower()
                       for x in list(artist.lower())) is not None:
                    return track_name['uri']


def main():
    link = "https://www.billboard.com/charts/r-b-hip-hop-songs"
    scope = 'playlist-modify-private playlist-modify'
    playlist_name = "Billboard R&B/Hip-Hop Songs"

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
