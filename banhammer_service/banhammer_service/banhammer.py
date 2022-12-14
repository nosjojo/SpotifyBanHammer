import logging
from collections import deque
import sqlite3
from banhammer_service.database import SpotifyDB
import spotify
import threading
from banhammer_service.threads import Worker

class BanHammer:
    def __init__(self, session, ban_file, ban_database:sqlite3.Connection):
        self.session = session
        self.logger = logging.getLogger("BanHammer")
        self.ban_file = ban_file
        self.ban_db = ban_database
        self.cur = self.ban_db.cursor()
        self.spotify_db = SpotifyDB(connection=self.ban_db, cursor=self.cur)
        self.fifo = deque()
        self.thread_lock = threading.Lock()

    def ban_current_artist(self):
        self.add_to_queue(spotify.ban_current_playing_artist)

    def ban_current_song(self):
        self.add_to_queue(spotify.ban_current_playing_song)

    def add_to_queue(self, function):
        args=[function, self.session, self.spotify_db]
        self.fifo.append(args)
        Worker(self.fifo, self.thread_lock).start()
        
