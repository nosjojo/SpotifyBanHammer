import logging
import spotipy
from PyQt5.QtWidgets import QApplication
from banhammer_service.mainwindow import MainWindow
from spotipy.oauth2 import SpotifyOAuth
from pynput.keyboard import KeyCode, Listener
from banhammer_service import LOG_FILE, BAN_FILE, BAN_DB
from banhammer_service.keyboard import *
from banhammer_service.banhammer import BanHammer
import sqlite3
import sys

logger = logging.getLogger("BanHammer")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
logger.addHandler(handler)
logger.info("Log started.")
ban_db = sqlite3.connect(BAN_DB, check_same_thread=False)

#from banhammer_service import spotify

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

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



# NEED TO MAKE THE SCRIPT RECOVERABLE FROM TIMEOUT ERRORS.
