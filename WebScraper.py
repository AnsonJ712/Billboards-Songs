import pprint
import requests
import sys
import re
from bs4 import BeautifulSoup

import spotipy
import spotipy.util as util


link = "http://www.billboard.com/charts/dance-electronic-songs"
page = requests.get(link)
soup = BeautifulSoup(page.content, 'html.parser')

scope = 'playlist-modify-private playlist-modify'
playlist_name = "Billboards Dance/Electronic Songs"


def authenticate():
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


def get_tracks_from_billboard():
    songs = soup.find_all(class_='chart-row__song')

    tracks = []

    for song in range(len(songs) / 2):
        tracks.append(songs[song].get_text().strip())

    print "Getting songs from billboards.com"
    return tracks


def get_playlists():
    playlists = sp.user_playlists(user)

    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            print "Playlist found"
            return playlist_id

    print "Playlist does not exist, creating a new playlist"
    sp.user_playlist_create(user, playlist_name)
    get_playlists()


def add_songs_to_playlists(songs):
    track_id = []

    for x in range(len(songs)):
        results = sp.search(q=songs[x], type='track')
        track_id.append(results['tracks']['items'][0]['uri'])

    sp.user_playlist_replace_tracks(user, playlist_id, track_id)
    print "Adding songs to playlist"

if __name__ == "__main__":
    user = authenticate()[0]
    sp = authenticate()[1]
    tracks = get_tracks_from_billboard()
    playlist_id = get_playlists()
    add_songs_to_playlists(tracks)