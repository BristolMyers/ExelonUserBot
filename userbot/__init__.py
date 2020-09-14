import os
import sys
from telethon.sessions import StringSession
from telethon import TelegramClient
from var import Var
from pylast import LastFMNetwork, md5
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb
from dotenv import load_dotenv
from requests import get
import time
from pySmartDL import SmartDL
from .helpers import fonts as fonts, functions as exelondef
from .helpers import memeshelper as memes
from .helpers import tempmemes, process as process

StartTime = time.time()
exelonversion = "2.7.2"

if Var.STRING_SESSION:
    session_name = str(Var.STRING_SESSION)
    if session_name.endswith("="):
        bot = TelegramClient(
            StringSession(session_name),
            Var.APP_ID,
            Var.API_HASH)
    else:
        bot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=Var.APP_ID,
            api_hash=Var.API_HASH).start(
            bot_token=Var.STRING_SESSION)
else:
    session_name = "startup"
    bot = TelegramClient(session_name, Var.APP_ID, Var.API_HASH)

# Paper Plane Genişletilmiş Destek Çubukları
ENV = os.environ.get("ENV", False)

EXELON_ID = ["1012994299"]

# Bot Günlükleri kurulumu:
if bool(ENV):
    CONSOLE_LOGGER_VERBOSE = sb(
        os.environ.get(
            "CONSOLE_LOGGER_VERBOSE",
            "False"))
    if CONSOLE_LOGGER_VERBOSE:
        basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=DEBUG,
        )
    else:
        basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=INFO)
    LOGS = getLogger(__name__)

    # Yapılandırmanın zaten kullanılan değişken kullanılarak düzenlenip düzenlenmediğini kontrol edin.
    # Temel olarak, yapılandırma dosyası için 'bekaret kontrolü';)
    CONFIG_CHECK = os.environ.get(
        "___________PLOX_______REMOVE_____THIS_____LINE__________", None)
    if CONFIG_CHECK:
        LOGS.info(
            "Lütfen ilk hashtag'de belirtilen satırı config.env dosyasından kaldırın"
        )
        quit(1)
    BOTLOG_CHATID = int(os.environ.get("PRIVATE_GROUP_BOT_API_ID", "-100"))
    BOTLOG = sb(os.environ.get("BOTLOG", "True"))
    CONSOLE_LOGGER_VERBOSE = sb(
        os.environ.get(
            "CONSOLE_LOGGER_VERBOSE",
            "False"))
    # Chrome Sürücüsü ve Başsız Google Chrome Binaries
    CHROME_DRIVER = os.environ.get("CHROME_DRIVER", "/usr/bin/chromedriver")
    GOOGLE_CHROME_BIN = os.environ.get(
        "GOOGLE_CHROME_BIN", "/usr/bin/google-chrome")
    # OpenWeatherMap API Key
    OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
    # Youtube API key
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)
    # Default .alive name
    ALIVE_NAME = os.environ.get("ALIVE_NAME", None)
    AUTONAME = os.environ.get("AUTONAME", None)
    UPSTREAM_REPO_URL = os.environ.get(
        "UPSTREAM_REPO_URL",
        "https://github.com/BristolMyers/ExelonUserBot.git")
    # Last.fm Module
    BIO_PREFIX = os.environ.get("BIO_PREFIX", None)
    DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)
    LASTFM_API = os.environ.get("LASTFM_API", None)
    LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
    LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
    LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
    # Google Drive Module
    G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
    G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
    G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA", None)
    GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY",
                                             "./downloads")
    # time.py
    COUNTRY = str(os.environ.get("COUNTRY", ""))
    TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))
else:
    # Yerel barındırma kullanıyorsanız, ppe değişkenlerinizi buraya koyun
    PLACEHOLDER = None

# CloudMail.ru ve MEGA.nz ayıklayıcı ikili dosyalarını kurma,
if not os.path.exists('bin'):
    os.mkdir('bin')
binaries = {
    "https://raw.githubusercontent.com/adekmaulana/megadown/master/megadown":
    "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py":
    "bin/cmrudl",
    "https://raw.githubusercontent.com/adekmaulana/python-scripts/master/shell/megadirect":
    "bin/megadirect"
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)

# Global Variables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
ISAFK = False
AFKREASON = None
CMD_LIST = {}
SUDO_LIST = {}
# for later purposes
INT_PLUG = ""
LOAD_PLUG = {}
