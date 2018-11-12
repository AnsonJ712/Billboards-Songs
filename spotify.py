import re
import sys

import spotipy
import spotipy.util as util


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
            temp = artists[song].get_text().strip()
            artist = temp
            artist = re.sub(r"([,*]|\s([X&+x]|(Featuring)|(With)|(And)|(vs))).*",
                '',
                artist)
            song = songs[song].get_text().strip()

            if self.__get_track_uri(sp, song, artist) is not None:
                track_id.append(self.__get_track_uri(sp, song, artist))
                print("Added " + song + " by " + temp)

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

        if len(results['tracks']['items']) == 0:
            results = sp.search(q='{}'.format(song), type='track')

        for track_name in results['tracks']['items']:
            return track_name['uri']
