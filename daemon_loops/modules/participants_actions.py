import datetime as dt
import re
from daemon_loops.models import PostedTweet

import daemon_loops.settings as s


def insert_posted_tweet(p, channel, conn, m):
    PostedTweet(campain_id=s.CAMPAIN_ID,
                url=re.findall(s.TWEET_REGEXP, m.message_str)[0],
                date_received=dt.datetime.now(s.TIMEZONE),
                sender_id=p.get_normalised_id(),
                sender_name=p.display_name,
                ).save()  # todo : faire un dédoublonnage? et une normalisation d'url (enlever les arguments GET)

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
            freq = "%i secondes" % (int(minutes * 60))
        else:
            freq = "%.2f minutes" % minutes
        return "Je t'enverrai des suggestions toutes les %s.\n\n__**(Note : Ceci ne vaut que pour les\
 suggestions que je t'envoie automatiquement, par pour les messages des animateur·ice·s 🗣)**__" % freq
    else:
        "Je n'ai pas compris la fréquence à laquelle je dois t'envoyer les suggestions\nPar exemple : __**FREQ 3**__, " \
        "ou __**FREQ 0.5**__"


def update_frequency_for_participant(p, conn, message_str):
    format_is_ok, minutes = analyse_frequency(message_str)
    if format_is_ok:
        return conn.update_suggestions_frequency(p, minutes)
    else:
        return p


async def send_other_suggestion(participant, channel, conn, message):
    if participant.last_text_suggestion_id is not None:
        await conn.send_suggestion(participant, channel, text_id=participant.last_text_suggestion_id, force=True)
    return participant


actions = {
    'stop': {
        'name': 'STOP',
        'test_func': lambda message_str, p: "stop" == format_participant_message(message_str),
        'answer': "🤖 Tu as demandé à ne plus reçevoir de messages, alors je me tais ;)\n\nSi tu changes "
                  "d'avis, réponds __**REPRENDRE**__\n\n(__**Note**__ : Je ne te transfèrerai plus non plus les "
                  "messages des animateur·ice·s 🗣)\n\nMerci pour ta participation !",
        'action_func': lambda p, c, conn, m: conn.db.update_participant_consent(p, False)
    },
    'reprendre': {
        'name': 'REPRENDRE',
        'test_func': lambda message_str, p: "reprendre" == format_participant_message(message_str),
        'answer': "🤖 Tu as demandé à reprendre, merci !\n\nSi tu changes d'avis, réponds __**STOP**__ "
                  "\n\nMerci pour ta participation !",
        'action_func': lambda p, c, conn, m: conn.db.update_participant_consent(p, True)
    },
    'tweet_received': {
        'name': 'SUGGERER UN TWEET',
        'test_func': lambda message_str, p: detect_tweet_url(message_str),
        # !!! supprimer les arguments après le ? dans l'url
        'answer': "🤖 Merci pour ton tweet. Il sera suggéré aux autres activistes pour qu'iels le retweetent.",
        'action_func': insert_posted_tweet
    },


    'change_frequency': {
        'name': 'CHANGER FREQUENCE DES SUGGESTIONS',
        'test_func': lambda message_str, p: len(re.findall(r'\A\s*freq\s*[0-9,\.]+', message_str.lower())),
        'answer': lambda p, conn, m: "🤖 " + answer_for_frequency(m.message_str),
        'action_func': lambda p, c, conn, m: update_frequency_for_participant(p, conn, m.message_str)
    },
    'report_bug': {
        'name': 'SIGNALER UN BUG',
        'test_func': lambda message_str, p: "bug" == format_participant_message(message_str)[:3],
        # todo : pas très élégant
        'answer': "🤖 Merci pour ce signalement de bug.\nJe le transmet de ce pas !",
        'action_func': lambda p, c, conn, m: p  # todo à faire
    },
    'other_formulation': {
        'name': 'DEMANDER UNE AUTRE FORMULATION POUR CE TWEET',
        'test_func': lambda message_str, p: "autre" == format_participant_message(message_str),
        'answer': None,
        'action_func': lambda p, c, conn, m: p,
        'async_action_func': send_other_suggestion
    },
}
