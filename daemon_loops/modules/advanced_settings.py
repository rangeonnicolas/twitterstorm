import os

import pytz
from asgiref.sync import sync_to_async

from daemon_loops.models import ConfigParticicipantlist, ConfigAdmins, ConfigScribes, ConfigRobotScribes, \
    ConfigReachableParticipants, ConfigVars

DATA_DIR = os.path.join('daemon_loops', 'data')
LOG_DIR = os.path.join(DATA_DIR, "log")
SESSION_DIR = os.path.join(DATA_DIR, "sessions")

SESSION_LISTENING_LOOP = os.path.join(SESSION_DIR, "main_session")

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


def get_class_according_to_type(type):
    types = {
        'ADMIN': ConfigAdmins,
        "SCRIBE_ANIMATOR": ConfigScribes,
        "SCRIBE_ROBOT" : ConfigRobotScribes,
        "REACHABLE": ConfigReachableParticipants,
    }
    if type not in types.keys():
        # todo_es : ces fonstions ne doivent pas etre dans ce fichier, surtout qu'elles raisent des exception alors qu'il faudrait utiliser logging.error
        raise Exception("Argument 'type' invalide ({})".format(type))
    return types[type]


async def addParticipantToConf(campain_id, participant_norm_id, type, display_name_for_animators=None):
    participant, cls = await getParticipantInConf(campain_id, participant_norm_id, type)
    kwargs = {
        'campain_id': campain_id,
        'participant_id': participant_norm_id
    }
    if display_name_for_animators:
        kwargs.update({'display_name_for_animators' : display_name_for_animators})
    if participant is None:
        await fixfix(cls, kwargs)
    else:
        for k, v in kwargs.items():
            setattr(participant, k, v)
        await pipou(participant)

@sync_to_async
def pipou(participant):
    participant.save()

@sync_to_async
def fixfix(cls, kwargs):
    cls(**kwargs).save()

@sync_to_async
def getParticipantInConf(campain_id, participant_norm_id, type) -> (ConfigParticicipantlist, type):
    cls = get_class_according_to_type(type)

    objs = cls.objects.filter(
        campain_id=campain_id,
        participant_id=participant_norm_id
    )
    if len(objs) > 1:
        # todo_chk oui c'est pas beau mais init est appelé 3 fois , à chaque début de boucle.
        #  Il ne faudrait qu'un seul init, mais ça implique de sortir le init de la loop async (quoi que...)
        obj = objs[0]
        for o in objs[1:]:
            o.delete()
    elif len(objs) == 1:
        return objs[0], cls
    else:
        return None, cls

@sync_to_async
def getAllScribesInConf(campain_id) -> dict:  # todo_es kamelkase??
    result = {}
    for type in ["SCRIBE_ANIMATOR", "SCRIBE_ROBOT"]:
        cls = get_class_according_to_type(type)
        objs = cls.objects.filter(campain_id=campain_id)
        result.update({o.participant_id:
                           {'scribe_type': type,
                            'name': o.display_name_for_animators}
                        for o in objs})
    return result

@sync_to_async
def get_all_admins_ids(campain_id) -> list:
    objs = ConfigAdmins.objects.filter(campain_id=campain_id)
    return [o.participant_id for o in objs]

@sync_to_async
def get_reachable_participants_ids(campain_id) -> list:
    objs = ConfigReachableParticipants.objects.filter(campain_id=campain_id)
    return [o.participant_id for o in objs]

async def set_conf_var(campain_id, key, value):
    kwargs = {'campain_id': campain_id, 'key': key}
    if isinstance(value, bool):
        kwargs.update({'value_bool': value})
    elif isinstance(value, float) or isinstance(value, int):
        kwargs.update({'value_float': value})
    elif isinstance(value, str):
        kwargs.update({'value_str': value})
    else:
        raise Exception("Type inconnu")

    obj = await _get_conf_var(campain_id, key)

    if obj is not None:
        for k, v in kwargs.items():
            setattr(obj, k, v)
    else:
        obj = ConfigVars(**kwargs)

    await plop(obj)

@sync_to_async
def plop(obj):
    obj.save()

@sync_to_async
def _get_conf_var(campain_id, key):
    objs = ConfigVars.objects.filter(
        campain_id=campain_id,
        key=key
    )
    if len(objs) > 1:
        # todo_chk oui c'est pas beau mais init est appelé 3 fois , à chaque début de boucle.
        #  Il ne faudrait qu'un seul init, mais ça implique de sortir le init de la loop async (quoi que...)
        obj = objs[0]
        for o in objs[1:]:
            o.delete()
    elif len(objs) == 1:
        return objs[0]
    else:
        return None


async def get_conf_value(campain_id, key):
    obj = await _get_conf_var(campain_id, key)
    if obj is None:
        return None
    else:
        for field in ['value_float', 'value_bool', 'value_str']:
            value = getattr(obj, field, None)
            if value is not None:
                return value
    # todo_es : gérer le cas où aucun des 3 n'est ok mieux que ça
    return None
