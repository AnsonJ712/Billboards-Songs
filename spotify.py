import re
import sys

import spotipy
import spotipy.util as util


class Spotify:
    def __init__(self, scope):
        self.scope = scope

    def authenticate(self, scope, username):
        """
        Grants permission for user to use Spotify's API
        """
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
            artist = artists[song].get_text().strip().replace("'", "")
            artist = re.sub(r"([,*]|\s([X&+x]|(Featuring)|"
                "(With)|(And))).*",
                '',
                artist)
            song = songs[song].get_text().strip()
            if self.get_track_uri(sp, song, artist) is not None:
                track_id.append(self.get_track_uri(sp, song, artist))
                print("Added " + song + " by " + artist)
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
                print("Playlist found")
                return playlist_id

        print("Playlist does not exist, creating a new playlist")
        sp.user_playlist_create(user, playlist_name)
        return self.get_playlist(sp, user, playlist_name)

    def get_track_uri(self, sp, song, artist):
        """
        Searches for song titles and adds them to the playlist
        """
        results = sp.search(q=song.lower() + " " + artist)
        for track_name in results['tracks']['items']:
            if all(x in track_name['name'].lower()
                   for x in list(song.lower())) is not None:
                return track_name['uri']
