import datetime as dt
import re
from daemon_loops.models import PostedTweet

from settings import settings as s


# todo_chk c'est très chelou qu'on ne douve pas faire passer cette fonction en asynchrone...
def insert_posted_tweet(p, channel, conn, m):
    PostedTweet(campain_id=s.CAMPAIN_ID,
                url=re.findall(s.TWEET_REGEXP, m.message_str)[0],
                date_received=dt.datetime.now(s.TIMEZONE),
                sender_id=p.get_normalised_id(),
                sender_name=p.display_name,
                ).save()

    return p


def format_participant_message(message_str):
    s = re.sub(r'\s', '', message_str)
    s = re.sub(r'\W', '', s)
    s = s.lower()
    return s


def detect_tweet_url(message_str):
    return len(re.findall(s.TWEET_REGEXP, message_str))


def analyse_frequency(message_str):
    format_is_ok = False
    minutes = None
    try:
        nb_str = re.findall(r'\A\s*freq\s*([0-9,\.]+)', message_str.lower())[0]
    except IndexError:
        return False, None
    nb_str = re.sub(",", ".", nb_str)
    nb_str = nb_str[:6]  # avoids too long numbers sent by a participant
    try:
        minutes = float(nb_str)
    except ValueError:
        return False, None
    minutes = max(minutes, s.MIN_SUGGESTION_FREQUENCY)
    return True, minutes



def answer_for_frequency(message_str):
    format_is_ok, minutes = analyse_frequency(message_str)
    if format_is_ok:
        if minutes < 1:
            freq = s.ACTION_FREQ_SECONDS % (int(minutes * 60))
        else:
            freq = s.ACTION_FREQ_MINUTES % minutes
        return s.ACTION_FREQ_UPDATE % freq
    else:
        return s.ACTION_FREQ_ERROR



def update_frequency_for_participant(p, conn, message_str):
    format_is_ok, minutes = analyse_frequency(message_str)
    if format_is_ok:
        return conn.update_suggestions_frequency(p, minutes)
    else:
        return p


async def send_other_suggestion(participant, channel, conn, message ,pi=None):
    if participant.last_text_suggestion_id is not None:
        await conn.send_suggestion(participant, channel, text_id=participant.last_text_suggestion_id, force=True)
    return participant


async def start_suggestions(conn,p):
    if not s.USE_SANDBOX:
        await s.set_conf_var(s.CAMPAIN_ID, 'DEFAULT_SUGGESTIONS', True)
    return p

async def end_suggestions(conn,p):
    if not s.USE_SANDBOX:
        await s.set_conf_var(s.CAMPAIN_ID, 'DEFAULT_SUGGESTIONS', False)  # todo_es : changer le nom de cette variable
    return p

async def open_campain(conn, p, participants_info):
    if not s.USE_SANDBOX:
        await s.set_conf_var(s.CAMPAIN_ID, 'CAMPAIN_IS_OPEN', True)
        # todo_es j'espère que participants_info est bien updaté.
        participants_info = await conn.send_welcome_message_to_all_participants(p, participants_info)
    return p

async def close_campain(conn, p):
    if not s.USE_SANDBOX:
        await s.set_conf_var(s.CAMPAIN_ID, 'CAMPAIN_IS_OPEN', False)
    return p



actions = {
    'stop': {
        'name': 'STOP', # doit être compréhensible par un scribe
        'test_func': lambda message_str, p: "stop" == format_participant_message(message_str),
        'answer': s.ROBOT_MSG_SUFFIX + s.ACTION_ANSWER_STOP,
        'action_func': lambda p, c, conn, m: conn.db.update_participant_consent(p, False)
    },
    'reprendre': {   # todo_es : english please (+ ! chercher les références dans message_analyser.py)
        'name': 'REPRENDRE',
        'test_func': lambda message_str, p: "reprendre" == format_participant_message(message_str),
        'answer': s.ROBOT_MSG_SUFFIX + s.ACTION_ANSWER_START,
        'action_func': lambda p, c, conn, m: conn.db.update_participant_consent(p, True)
    },
    'tweet_received': {
        'name': 'SUGGERER UN TWEET',
        'test_func': lambda message_str, p: detect_tweet_url(message_str),
        # !!! supprimer les arguments après le ? dans l'url
        'answer': s.ROBOT_MSG_SUFFIX + s.ACTION_ANSWER_TWEET_RECEIVED,
        'action_func': insert_posted_tweet
    },
    'change_frequency': {
        'name': 'CHANGER FREQUENCE DES SUGGESTIONS',
        'test_func': lambda message_str, p: len(re.findall(r'\A\s*freq\s*[0-9,\.]+', message_str.lower())),
        'answer': lambda p, conn, m: s.ROBOT_MSG_SUFFIX + answer_for_frequency(m.message_str),
        'action_func': lambda p, c, conn, m: update_frequency_for_participant(p, conn, m.message_str)
    },
    'report_bug': {
        'name': 'SIGNALER UN BUG',
        'test_func': lambda message_str, p: "bug" == format_participant_message(message_str)[:3],
        # todo_es : pas très élégant le [:3]
        'answer': s.ROBOT_MSG_SUFFIX + s.ACTION_ANSWER_REPORT_BUG,
        'action_func': lambda p, c, conn, m: p
    },
    'other_formulation': {
        'name': 'DEMANDER UNE AUTRE FORMULATION POUR CE TWEET',
        'test_func': lambda message_str, p: "autre" == format_participant_message(message_str),
        'answer': None,
        'action_func': lambda p, c, conn, m: p,
        'async_action_func': send_other_suggestion
    },
}

async def _raise():  # todo_cr
    raise Exception("Admin raised exception")

admin_actions = {
    'OPEN_CAMPAIN': {
        'name': 'OPEN',
        'test_func': lambda message_str, p: "open" == format_participant_message(message_str),
        'answer': s.ROBOT_MSG_SUFFIX + s.ACTION_ADMIN_OPEN_CAMPAIN if not
        s.USE_SANDBOX else s.ACTION_ADMIN_SANDBOX_ERROR,
        'action_func': lambda p, c, conn, m: p,
        'async_action_func': lambda p, c, conn, m,pi=None: open_campain(conn, p, pi),
    },
    'CLOSE_CAMPAIN': {
        'name': 'CLOSE',
        'test_func': lambda message_str, p: "close" == format_participant_message(message_str),
        'answer': s.ROBOT_MSG_SUFFIX + s.ACTION_ADMIN_CLOSE_CAMPAIN if
        not s.USE_SANDBOX else s.ACTION_ADMIN_SANDBOX_ERROR,
        'action_func': lambda p, c, conn, m: p,
        'async_action_func': lambda p, c, conn, m,pi=None: close_campain(conn, p),
    },
    'START_SUGGESTIONS': {
        'name': 'START SUGGESTIONS',
        'test_func': lambda message_str, p: "startsuggestions" == format_participant_message(message_str),
        'answer': s.ROBOT_MSG_SUFFIX + s.ACTION_ADMIN_START_SUGGESTIONS if not s.USE_SANDBOX else s.ACTION_ADMIN_SANDBOX_ERROR,
        'action_func': lambda p, c, conn, m: p,
        'async_action_func': lambda p, c, conn, m,pi=None: start_suggestions(conn, p),
    },
    'END_SUGGESTIONS': {
        'name': 'END SUGGESTIONS',
        'test_func': lambda message_str, p: "endsuggestions" == format_participant_message(message_str),
        'answer': s.ROBOT_MSG_SUFFIX + s.ACTION_ADMIN_END_SUGGESTIONS if not s.USE_SANDBOX else s.ACTION_ADMIN_SANDBOX_ERROR,
        'action_func': lambda p, c, conn, m: p,
        'async_action_func': lambda p, c, conn, m,pi=None: end_suggestions(conn, p),
    },
    'EXCEPT': {
        'name': '12345ZZZ',
        'test_func': lambda message_str, p: "12345zzz" == format_participant_message(message_str),
        'answer': s.ROBOT_MSG_SUFFIX + s.ACTION_ADMIN_RAISE_EXCEPTION,
        'action_func': lambda p, c, conn, m: p, #_raise(),
        'async_action_func': lambda p, c, conn, m,pi=None: _raise(),
    },
}
