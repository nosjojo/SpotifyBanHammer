import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pynput.keyboard import KeyCode, Listener
from banhammer_service import utility
import spotify
from banhammer_service.keyboard import *
from banhammer_service.banhammer import BanHammer
import pathlib
from objects import *

logger = logging.getLogger("BanHammer")

user_dir = pathlib.Path.home()/pathlib.Path("SpotifyBanHammer")
log_file = user_dir/"banhammer.log"
ban_file = user_dir/"banned.csv"
if not user_dir.exists():
    user_dir.mkdir(parents=True, exist_ok=True)

logger.setLevel(logging.INFO)
handler = logging.FileHandler(log_file, encoding='utf-8')
logger.addHandler(handler)
logger.info("Log started.")

if __name__ == "__main__":
    scope = ("ugc-image-upload,"
            "user-modify-playback-state,"
            "user-read-playback-state,"
            "user-read-currently-playing,"
            "user-follow-modify,"
            "user-follow-read,"
            "user-read-recently-played,"
            "user-read-playback-position,"
            "user-top-read,"
            "playlist-read-collaborative,"
            "playlist-modify-public,"
            "playlist-read-private,"
            "playlist-modify-private,"
            "app-remote-control,"
            "streaming,"
            "user-library-modify,"
             "user-library-read")
            
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))
    the_hammer = BanHammer(session=sp, ban_file=ban_file)
    playlist = Playlist(spotify.find_playlist_by_name(sp, "Better New Music Friday"))
    utility.dump_response_to_file(playlist, "example_single_playlist")
    result = spotify.get_playlist_tracks(sp, playlist)
    print("")
    

# NEED TO MAKE THE BAN LIST A DATABASE WITH AN ARTIST TABLE AND A SONG TABLE.
# NEED TO MAKE THE SCRIPT RECOVERABLE FROM TIMEOUT ERRORS.
