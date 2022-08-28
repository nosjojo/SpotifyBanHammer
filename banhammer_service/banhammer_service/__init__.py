import logging
import pathlib

logger = logging.getLogger("BanHammer")
USER_DIR = pathlib.Path.home()/pathlib.Path("SpotifyBanHammer")
LOG_FILE = USER_DIR/"banhammer.log"
BAN_FILE = USER_DIR/"banned.csv"
BAN_DB = USER_DIR/"banned.db"

if not USER_DIR.exists():
    USER_DIR.mkdir(parents=True, exist_ok=True)