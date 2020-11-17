import os

import pytz

DATA_DIR = 'data'
LOG_DIR = os.path.join(DATA_DIR, "log")
SESSION_DIR = os.path.join(DATA_DIR, "sessions")

SESSION_LISTENING_LOOP = os.path.join(SESSION_DIR, "listening_loop")

TIMEZONE = pytz.timezone('Europe/Paris')

ALLOWED_CLIENTS = ["Telegram", "Riendotr"]

STR_UNKNOWN_CLIENT = "Le client spécifié dans la variable CLIENT doit être l'un de ceux-ci : '{}' .".format(
    "', '".join(ALLOWED_CLIENTS))

STR_TG_ENTER_CODE = "Entrez le code envoyé sur le compte Télégram du robot ({}) : "
STR_TG_INVALID_CODE = "Le code envoyé sur le compte Télégram de {} ne correspond pas à celui que vous avez saisi."
STR_TG_AUTH_OK = "Authentification réussie !"
STR_TG_TOO_MANY_INVALID = "Vous avez fait trop d'erreurs en saisissant le code. Il faut maintenant attendre {} " \
                          "secondes avant de relancer le programme, ou utiliser un autre compte Télegram comme robot," \
                          " à spécifier dans la variable BOT_PHONE_NUMBER du fichier de configuration '{}.py'"

TWEET_REGEXP = "https?://[a-zA-Z.]*?twitter.com/.*?/status/[0-9]*"
