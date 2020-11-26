import os

env = os.environ.get("TS_ENV_TYPE")
if env is None:
    raise Exception("Variable d'environnement TS_ENV_TYPE indéfinie")
elif env.lower() == "dev":
    f = 'settings_tg_dev'
    sets = __import__(f)
elif env.lower() == "prod":
    f = 'settings_tg_prod'
    sets = __import__(f)
else :
    raise Exception("La valeur de la variable d'environnement est erronée : " + env)
INIT_MSG_TO_LOG = "Importé : " + f

RESTRICT_REACHABLE_USERS = sets.RESTRICT_REACHABLE_USERS
REACHABLE_USERS = sets.REACHABLE_USERS
MAIN_CHANNEL_ID = sets.MAIN_CHANNEL_ID




API_ID = "1276127"
API_HASH = "17ee6f423a60838f8f0d7e64d43de5d8"

BOT_PHONE_NUMBER = "+33751212307"

nicolas_acp = 483278428 # todo_es : pas bo

ME = nicolas_acp  # @nicolas_acp # compte servant à tester le programme lorsque SEND_ONLY_TO_ME = True
BOT = 1097550906
TRUSTED_USER_FOR_TWEET_VALIDATION = ME
ADMINS = [nicolas_acp]

SCRIBES_ANIMATORS = [{'tg_id' : 1499986438,
                      'display_name' : "Matthieu GP"}] # matthieu GP
# todo_es : hack pas beau sur le display name !!

SCRIBES_ROBOTS = [1465837192]    # Johanna Klein


NB_MSG_TO_FETCH = 40  # Seulement pour la première itération (au lancement du programme)
