import os
import sys
import re
import requests
import json

import spotipy
import spotipy.util as util

from bs4 import BeautifulSoup


class Spotify:
    def __init__(self, scope):
        self.scope = scope

    def authenticate(self, username):
        """
        Grants permission for user to use Spotify's API
        """
        token = util.prompt_for_user_token(username, self.scope)

        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
        else:
            print("Can't get token for", username)

        return username, sp

    def add_to_playlist(self, sp, user, artists, songs, playlist_name):
        playlist_id = self.__get_playlist(sp, user, playlist_name)
        track_id = []

        for song in range(len(songs)):
            """
            Format songs and artists to search through Spotify API
            """
            artist = artists[song].get_text().strip()
            temp_artist = artist
            temp_artist = re.sub(r"([,*']|\s([X&+x]|(\b(Feat)\w+)|(With)|(And)|(vs)|(Presents))|(The)).*",
                                 '',
                                 temp_artist)

            song = songs[song].get_text().strip()
            temp_song = song
            temp_song = re.sub(r"([()]|(\d{4})).*",
                               '',
                               temp_song)

            uri = self.__get_track_uri(sp, temp_song, temp_artist)

            if uri is not None:
                track_id.append(uri)
            print("Added " + song + " by " + artist)
        sp.user_playlist_replace_tracks(user, playlist_id, track_id)

    def __get_playlist(self, sp, user, playlist_name):
        """
        Searches for playlist,
        Creates new playlist if not found
        """
        playlists = sp.user_playlists(user)

        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                print("Playlist found")
                return playlist_id
        print("Playlist does not exist, creating a new playlist")
        sp.user_playlist_create(user, playlist_name)

        return self.__get_playlist(sp, user, playlist_name)

    def __get_track_uri(self, sp, song, artist):
        """
        Searches for song titles and adds them to the playlist
        """
        results = sp.search(q='{} {}'.format(song, artist), type='track,artist')

        for track_name in results['tracks']['items']:
            """
            Adds non-remix version of song
            """
            # if 'Remix' not in track_name['name'] and 'Remix' not in song and \
            #         song.lower().strip() in track_name['name'].lower().replace('’', '\''):
            for artists in track_name['artists']:
                if artist.lower() in artists['name'].lower():
                    return track_name['uri']
            return track_name['uri']

        song = song.split(' ')[0]
        results = sp.search(q='{} {}'.format(song, artist), type='track,artist')

        if len(results['tracks']['items']) != 0:
            return results['tracks']['items'][0]['uri']


class Billboard:
    def __init__(self, link):
        self.link = link

    def get_page(self):
        return requests.get(self.link)

    def parse_page(self, page):
        return BeautifulSoup(page.content, 'html.parser')

    def get_tracks_from_billboard(self, soup):
        """
        Collects song titles from billboards.com
        """
        chart_name = soup.find(class_='chart-detail-header__chart-name')
        artists = soup.find_all(class_='chart-list-item__artist')
        songs = soup.find_all(class_='chart-list-item__title-text')

        return artists, songs, chart_name


def create_billboard_playlist():
    with open('config.json') as config_file:
        config = json.load(config_file)

    client_id = config['client_id']
    client_secret = config['client_secret']
    redirect_uri = config['redirect_uri']
    account = config['account']

    os.environ['SPOTIPY_CLIENT_ID'] = client_id
    os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
    os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri

    link = sys.argv[1]

    scope = 'playlist-modify-private playlist-modify'

    charts = Billboard(link)
    page = charts.get_page()
    soup = charts.parse_page(page)
    artists = charts.get_tracks_from_billboard(soup)[0]
    songs = charts.get_tracks_from_billboard(soup)[1]
    chart_name = charts.get_tracks_from_billboard(soup)[2]

    playlist_name = "Billboard " + chart_name.get_text().title().strip('\n')

    spotify = Spotify(scope)
    user = spotify.authenticate(account)[0]
    sp = spotify.authenticate(account)[1]
    spotify.add_to_playlist(sp, user, artists, songs, playlist_name)

    print("Done!")


def main():
    create_billboard_playlist()


if __name__ == "__main__":
    main()
