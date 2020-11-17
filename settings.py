import datetime as dt
from modules.advanced_settings import *  # todo utiliser une autre méthode

CLIENT = "Telegram"

CAMPAIN_NAME = "TwitterStrorm_1"

DEFAULT_CONSENT = False
DEFAULT_TWEET_VALIDATION = False

SEND_ONLY_TO_ME = True

# END_LISTENING_LOOP = dt.datetime(2020,5,24,8,0,0,tzinfo=s.TIMEZONE)
END_LISTENING_LOOP = dt.datetime.now(s.TIMEZONE) + dt.timedelta(0, 60 * 60)  # a changer
