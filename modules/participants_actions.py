import datetime as dt
import re

import settings as s


def insert_posted_tweet(p, conn, m):
    conn.db.insert_posted_tweet([{'campain': s.CAMPAIN_NAME,
                                  'url': re.findall(s.TWEET_REGEXP, m.message_str)[0],
                                  'date_received': dt.datetime.now(s.TIMEZONE),
                                  'received_from': p.get_normalised_id()}],
                                trusted=p.is_trusted_participant_for_tweets())
    return p


actions = {
    'stop': {
        'test_func': lambda message_str, p: "stop" == re.sub(r'\W', '',
                                                             re.sub(r'\s', '', message_str)).lower(),
        'answer': "Vous avez demandé à ne plus reçevoir de messages de moi, je me tais donc ;)\n\nSi vous changez "
                  "d'avis, répondez 'reprendre' (uniquement)\n\nMerci pour votre participation !",
        'action_func': lambda p, conn, m: conn.db.update_participant_consent(p, False)
    },
    'reprendre': {
        'test_func': lambda message_str, p: "reprendre" == re.sub(r'\W', '',
                                                                  re.sub(r'\s', '', message_str)).lower(),
        'answer': "Vous avez demandé à reprendre, merci !\n\nSi vous changez d'avis, répondez 'stop' ("
                  "uniquement)\n\nMerci pour votre participation !",
        'action_func': lambda p, conn, m: conn.db.update_participant_consent(p, True)
    },
    'tweet_received': {
        'test_func': lambda message_str, p: len(re.findall(s.TWEET_REGEXP, message_str)),
        # !!! supprimer les arguments après le ? dans l'url
        'answer': "Merci pour votre tweet. Il sera suggéré aux autres participants pour qu'iels le retweetent.",
        'action_func': insert_posted_tweet
    },

}
