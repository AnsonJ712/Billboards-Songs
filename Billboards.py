import requests
import sys
import re
import pprint
from bs4 import BeautifulSoup
from collections import OrderedDict

import spotipy
import spotipy.util as util


link = "http://www.billboard.com/charts/dance-electronic-songs/2017-09-09"
page = requests.get(link)
soup = BeautifulSoup(page.content, 'html.parser')

scope = 'playlist-modify-private playlist-modify'
playlist_name = "Billboards Dance/Electronic Songs"


def authenticate():
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


def get_tracks_from_billboard():
    """
    Collects top dance/electronic song titles from billboards.com
    """
    artists = soup.find_all(class_='chart-row__artist')
    songs = soup.find_all(class_='chart-row__song')

    tracks = OrderedDict();
    for song in range(len(songs)):
        artist = artists[song].get_text().strip()
        artist = re.sub("([&]|(Featuring)|\s[x]|\s$|\sAnd.*|\sWith.*).*", '', artist)
        song = songs[song].get_text().strip()
        tracks[song] = artist
    print "Getting songs from billboards.com"
    # pprint.pprint(tracks)
    return tracks


def get_playlists():
    """
    Searches for playlist named "Billboards Dance/Electronic Songs"
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
    return get_playlists()


def add_songs_to_playlists(playlist_id, songs):
    """
    Searches for song titles and adds them to the playlist
    """
    track_id = []
    added_to_playlist = False
    print "Adding songs to playlist"
    for song, artist in songs.iteritems():
        artist = re.sub("\s$|(\b\sAnd.*\b)", "", artist)
        results = sp.search(q=song + " " + artist)
        for track_name in results['tracks']['items']:
            for artist_name in track_name['album']['artists']:
                if (re.match(artist+'.*', artist_name['name']) or re.match(artist+'.*', "Italo Brothers")) is not None:
                    track_id.append(track_name['uri'])
                    added_to_playlist = True
                    break
            if added_to_playlist:
                added_to_playlist = False
                break
    sp.user_playlist_replace_tracks(user, playlist_id, track_id)


if __name__ == "__main__":
    user = authenticate()[0]
    sp = authenticate()[1]
    tracks = get_tracks_from_billboard()
    playlist_id = get_playlists()
    add_songs_to_playlists(playlist_id, tracks)
    print "Songs added"