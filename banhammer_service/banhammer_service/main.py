import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pynput.keyboard import KeyCode, Listener
from banhammer_service import LOG_FILE, BAN_FILE, BAN_DB
from banhammer_service.keyboard import *
from banhammer_service.banhammer import BanHammer
import sqlite3


logger = logging.getLogger("BanHammer")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
logger.addHandler(handler)
logger.info("Log started.")
ban_db = sqlite3.connect(BAN_DB)


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
    the_hammer = BanHammer(session=sp, ban_file=BAN_FILE, ban_database=ban_db)
    bindings = {frozenset([KeyCode(vk=160), KeyCode(vk=162), KeyCode(vk=46)]): the_hammer.ban_current_artist,
                frozenset([KeyCode(vk=160), KeyCode(vk=162), KeyCode(vk=8)]): the_hammer.ban_current_song}
    kb = KeyBindings()

    with Listener(on_press=kb.on_press, on_release=kb.on_release) as listener:
        kb.set_hotkeys(bindings)
        listener.join()

# NEED TO MAKE THE BAN LIST A DATABASE WITH AN ARTIST TABLE AND A SONG TABLE.
# NEED TO MAKE THE SCRIPT RECOVERABLE FROM TIMEOUT ERRORS.
