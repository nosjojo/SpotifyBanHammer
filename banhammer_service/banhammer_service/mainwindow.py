import typing
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtCore import QThreadPool, QThread
from PyQt5 import QtCore

from banhammer_service.threads import QWorker
from banhammer_service.ui.ui_mainwindow import Ui_SpotifyBanHammer
import logging
import spotipy
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

class MainWindow(QMainWindow, Ui_SpotifyBanHammer):
    def __init__(self, parent: typing.Optional[QWidget] = None, flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType] = QtCore.Qt.WindowFlags()) -> None:
        super().__init__(parent, flags)
        self.setupUi(self)
        self.establish_connections()
        self.hotkeys_listener_thread = QThread()

    def establish_connections(self):
        self.start_hotkeys_btn.toggled.connect(self.toggle_hotkeys_listener)
        self.start_hotkeys_btn.clicked.connect(self.start_hotkeys_btn.toggle)
    
    def acquire_auth(self):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))

    def start_hotkey_thread(self):
        self.hotkey_worker = QWorker(self.keyboard_listener)
        self.hotkey_worker.moveToThread(self.hotkeys_listener_thread)
        self.hotkeys_listener_thread.started.connect(self.hotkey_worker.run)
        self.hotkey_worker.finished.connect(self.hotkeys_listener_thread.quit)
        self.hotkey_worker.finished.connect(self.hotkey_worker.deleteLater)
        #self.hotkeys_listener_thread.finished.connect(self.hotkeys_listener_thread.deleteLater)
        self.hotkeys_listener_thread.start()
    
    def toggle_hotkeys_listener(self, new_state):
        if new_state == True:
            self.start_hotkeys_btn.setText("Stop Hotkeys")
            self.start_hotkey_thread()
        else:
            self.start_hotkeys_btn.setText("Start Hotkeys")
            if self.hotkeys_listener_thread.isRunning():
                self.hotkeys_listener_thread.terminate()
                self.hotkeys_listener_thread.wait()

    def keyboard_listener(self):
        def print_artist():
            print("lololol artist")
        def print_song():
            print("lololol song")
        
        # the_hammer = BanHammer(session=sp, ban_file=BAN_FILE, ban_database=ban_db)
        bindings = {frozenset([KeyCode(vk=160), KeyCode(vk=162), KeyCode(vk=46)]): print_artist,
                    frozenset([KeyCode(vk=160), KeyCode(vk=162), KeyCode(vk=8)]): print_song}

        # bindings = {frozenset([KeyCode(vk=160), KeyCode(vk=162), KeyCode(vk=46)]): the_hammer.ban_current_artist,
                    # frozenset([KeyCode(vk=160), KeyCode(vk=162), KeyCode(vk=8)]): the_hammer.ban_current_song}
        kb = KeyBindings()

        #listener = Listener(on_press=kb.on_press, on_release=kb.on_release, name="keyboard_listener")
        #listener.start()
        with Listener(on_press=kb.on_press, on_release=kb.on_release, name="keyboard_listener") as listener:
             kb.set_hotkeys(bindings)
             listener.join()


    #spotify.sanitize_new_music_friday(sp, BAN_FILE)
        
        