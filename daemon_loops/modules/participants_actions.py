import datetime as dt
import re

import daemon_loops.settings as s


def insert_posted_tweet(p, conn, m):
    conn.db.insert_posted_tweet([{'campain': s.CAMPAIN_ID,
                                  'url': re.findall(s.TWEET_REGEXP, m.message_str)[0],
                                  'date_received': dt.datetime.now(s.TIMEZONE),
                                  'received_from': p.get_normalised_id()}],
                                trusted=p.is_trusted_participant_for_tweets())
    return p


actions = {
    'stop': {
        'name': 'STOP',
        'test_func': lambda message_str, p: "stop" == re.sub(r'\W', '',
                                                             re.sub(r'\s', '', message_str)).lower(),
        'answer': "Tu as demandé à ne plus reçevoir de messages de moi, alors je me tais ;)\n\nSi tu changes "
                  "d'avis, réponds __**reprendre**__\n\nMerci pour ta participation !",
        'action_func': lambda p, conn, m: conn.db.update_participant_consent(p, False)
    },
    'reprendre': {
        'name': 'REPRENDRE',
        'test_func': lambda message_str, p: "reprendre" == re.sub(r'\W', '',
                                                                  re.sub(r'\s', '', message_str)).lower(),
        'answer': "Tu as demandé à reprendre, merci !\n\nSi tu changes d'avis, réponds __**stop**__ "
                  "\n\nMerci pour ta participation !",
        'action_func': lambda p, conn, m: conn.db.update_participant_consent(p, True)
    },
    'tweet_received': {
        'name': 'SUGGERER UN TWEET',
        'test_func': lambda message_str, p: len(re.findall(s.TWEET_REGEXP, message_str)),
        # !!! supprimer les arguments après le ? dans l'url
        'answer': "Merci pour ton tweet. Il sera suggéré aux autres participants pour qu'iels le retweetent.",
        'action_func': insert_posted_tweet
    },


    'change_frequency': {
        'name': 'CHANGER FREQUENCE DES SUGGESTIONS',
        'test_func': lambda message_str, p: False,
        'answer': "",
        'action_func': lambda p, conn, m: None
    },
    'report_bug': {
        'name': 'SIGNALER UN BUG',
        'test_func': lambda message_str, p: False,
        'answer': "",
        'action_func': lambda p, conn, m: None
    },
    'other_formulation': {
        'name': 'DEMANDER UNE AUTRE FORMULATION POUR CE TWEET',
        'test_func': lambda message_str, p: False,
        'answer': "",
        'action_func': lambda p, conn, m: None
    },
}
