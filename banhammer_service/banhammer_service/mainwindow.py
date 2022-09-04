import typing
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtCore import QThreadPool, QThread, pyqtSlot, pyqtSignal
from PyQt5 import QtCore

from banhammer_service.threads import QWorker
from banhammer_service.ui.ui_mainwindow import Ui_SpotifyBanHammer
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pynput.keyboard import KeyCode, Listener, GlobalHotKeys, HotKey
from banhammer_service import LOG_FILE, BAN_FILE, BAN_DB
from banhammer_service.keyboard import *
from banhammer_service.banhammer import BanHammer
import sqlite3
import sys
pls_stop=False
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
    stop_kb_listener = pyqtSignal()
    def __init__(self, parent: typing.Optional[QWidget] = None, flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType] = QtCore.Qt.WindowFlags()) -> None:
        super().__init__(parent, flags)
        self.setupUi(self)
        self.establish_connections()
        self.kb_listener = None
        self.session = None
        self.hotkeys_listener_thread = QThread()
        

    def establish_connections(self):
        self.start_hotkeys_btn.toggled.connect(self.toggle_hotkeys_listener)
        self.stop_kb_listener.connect(self.stop_keyboard_listener)
        self.get_session_btn.pressed.connect(self.acquire_auth)
        
    def stop_keyboard_listener(self):
        if self.kb_listener:
            self.kb_listener.stop()
            self.kb_listener=None

    def acquire_auth(self):
        self.session = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))

    def start_hotkey_thread(self):
        self.hotkey_worker = QWorker(self.keyboard_listener)
        self.hotkey_worker.moveToThread(self.hotkeys_listener_thread)
        self.hotkeys_listener_thread.started.connect(self.hotkey_worker.run)
        self.hotkey_worker.finished.connect(self.hotkeys_listener_thread.quit)
        self.hotkey_worker.finished.connect(self.print_finished)
        self.hotkey_worker.finished.connect(self.hotkey_worker.deleteLater)
        self.hotkeys_listener_thread.start()
        
    
    def print_finished(self):
        print("finished")

    def toggle_hotkeys_listener(self, new_state):
        if new_state == True:
            self.start_hotkeys_btn.setText("Stop Hotkeys")
            self.start_hotkey_thread()
        else:
            self.start_hotkeys_btn.setText("Start Hotkeys")
            self.stop_kb_listener.emit()

    def keyboard_listener(self):
        the_hammer = BanHammer(session=self.session, ban_file=BAN_FILE, ban_database=ban_db)
        kb = KeyBindings()
        
        self.kb_listener = GlobalHotKeys({
                '<ctrl>+<shift>+<46>': the_hammer.ban_current_artist,
                '<ctrl>+<shift>+<8>': the_hammer.ban_current_song})
        
        self.kb_listener.start()
              