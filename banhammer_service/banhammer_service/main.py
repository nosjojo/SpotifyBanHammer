import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pynput.keyboard import KeyCode, Listener
from banhammer_service.keyboard import *
from banhammer_service.banhammer import BanHammer
import pathlib

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
    bindings = {frozenset([KeyCode(vk=160), KeyCode(vk=162), KeyCode(vk=46)]): the_hammer.ban_current_artist,
                frozenset([KeyCode(vk=160), KeyCode(vk=162), KeyCode(vk=8)]): the_hammer.ban_current_song}
    kb = KeyBindings()

    with Listener(on_press=kb.on_press, on_release=kb.on_release) as listener:
        kb.set_hotkeys(bindings)
        listener.join()

# NEED TO MAKE THE BAN LIST A DATABASE WITH AN ARTIST TABLE AND A SONG TABLE.
# NEED TO MAKE THE SCRIPT RECOVERABLE FROM TIMEOUT ERRORS.
