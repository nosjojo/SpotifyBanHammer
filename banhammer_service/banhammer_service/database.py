import functools
import sqlite3
from typing import List, Tuple
from objects import Artist, Track
import logging
logger = logging.getLogger("BanHammer")


class SpotifyDB:
    CMD_SQL_BAN_ARTIST = "INSERT INTO banned_artists VALUES(?, ?)"
    CMD_SQL_BAN_TRACK = "INSERT INTO banned_tracks VALUES(?, ?)"
    CMD_SQL_CHECK_ARTIST_TABLE = "SELECT name FROM sqlite_master WHERE type='table' AND name='banned_artists'"
    CMD_SQL_CHECK_TRACK_TABLE = "SELECT name FROM sqlite_master WHERE type='table' AND name='banned_tracks'"
    CMD_SQL_CREATE_ARTIST_TABLE = "CREATE TABLE banned_artists(name, id)"
    CMD_SQL_CREATE_TRACK_TABLE = "CREATE TABLE banned_tracks(name, id)"
    CMD_SQL_FIND_BANNED_TRACKS = "SELECT id, name FROM banned_tracks WHERE id IN ({})"
    CMD_SQL_FIND_BANNED_ARTISTS = "SELECT id, name FROM banned_artists WHERE id IN ({})"

    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
        self.connection = connection
        self.cursor = cursor

    def requires_artist_table(func):
        @functools.wraps(func)
        def wrapper_check_and_create_artist_table(self, artist):
            if not self.check_artist_table():
                self.create_artist_table()
            return func(self, artist)
        return wrapper_check_and_create_artist_table

    def requires_track_table(func):
        @functools.wraps(func)
        def wrapper_check_and_create_track_table(self, track):
            if not self.check_track_table():
                self.create_track_table()
            return func(self, track)
        return wrapper_check_and_create_track_table

    @requires_artist_table
    def ban_artist(self, artist: Artist):
        self.cursor.execute(self.CMD_SQL_BAN_ARTIST, (artist.name, artist.id))
        logger.info(f"banning {artist.name}, {artist.id}")
        self.connection.commit()

    @requires_track_table
    def ban_track(self, track: Track):
        self.cursor.execute(self.CMD_SQL_BAN_TRACK, (track.name, track.id))
        logger.info(f"banning {track.name}, {track.id}")
        self.connection.commit()

    def check_artist_table(self) -> bool:
        result = self.cursor.execute(self.CMD_SQL_CHECK_ARTIST_TABLE)
        logger.debug("Checking if banned_artist table exists.")
        if result.fetchone() is None:
            logger.debug("banned_artist table not found.")
            return False
        return True

    def check_track_table(self) -> bool:
        result = self.cursor.execute(self.CMD_SQL_CHECK_TRACK_TABLE)
        logger.debug("Checking if banned_track table exists.")
        if result.fetchone() is None:
            logger.debug("banned_track table not found.")
            return False
        return True

    def create_artist_table(self) -> None:
        self.cursor.execute(self.CMD_SQL_CREATE_ARTIST_TABLE)
        logger.debug("Creating banned_artist table.")
        if self.check_artist_table() is False:
            raise Exception("Artist table was not created.")

    def create_track_table(self) -> None:
        self.cursor.execute(self.CMD_SQL_CREATE_TRACK_TABLE)
        logger.debug("Creating banned_track table.")
        if self.check_track_table() is False:
            raise Exception("Track table was not created.")

    @requires_artist_table
    def check_for_banned_artists(self, ids: List[str]) -> List[Tuple[str, str]]:
        CMD = self.CMD_SQL_FIND_BANNED_ARTISTS.format(','.join('?'*len(ids)))
        logging.debug(f"Checking banned_artists table for {len(ids)} keys")
        res = self.cursor.execute(CMD, ids)
        banned_entries = res.fetchall()
        logging.debug(f"Found {len(banned_entries)} banned artists in table.")
        return banned_entries

    @requires_track_table
    def check_for_banned_tracks(self, ids: List[str]) -> List[Tuple[str, str]]:
        CMD = self.CMD_SQL_FIND_BANNED_TRACKS.format(','.join('?'*len(ids)))
        logging.debug(f"Checking banned_tracks table for {len(ids)} keys")
        res = self.cursor.execute(CMD, ids)
        banned_entries = res.fetchall()
        logging.debug(f"Found {len(banned_entries)} banned tracks in table.")
        return banned_entries
