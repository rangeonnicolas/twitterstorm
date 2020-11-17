import datetime as dt
import time

import settings as s  # todo : renommer l'alias
from modules.database import DataBase
from modules.logger import Logger
from modules.participants_actions import actions
from modules.telegram import TelegramConnection
from modules.twitterstorm import init, MessageAnalyser

# todo_f : docstrings
# todo_f : regrouper les chaines de caractères DESTINEES AU PARTICIPANTS !!
# todo_f : avaoir un vrai logger
# todo : la moindre petite exception dans la récupéaration d'un message ou autre fait planter le programme... :s
# todo : assouplir les regles de filtrage par is_reachable sinon c'est incompréhensible au debuggage,
#  notamment dans _get_participants_from_channel
# todo : inclure dans les tests : relancage du programme pour voir si tout repart bien comm'i'fo
# todo : tester le participant_consent! (en ragardant si persistence dan la bdd)
# todo : trouver un moyen de tester quand un participant sort de la boucle... ou jarter cette option...
# todo : un message pour tout nouvel arrivant dans la bdd
# todo : un message pour toutt personne qui part
# todo : tester l'ajout d'une personne à la boucle
# todo : reorganiser les fichiers de conf y faire une classe où on peut appeler s.msgs.SESSION_LISTENING_LOOP
# comment faire pour faire évoluer la conf durant l'exécution du programme (ex : ajout d'un scribe?)

init()
db = DataBase()
logger = Logger()


async def main(conn, analyser):
    deltamin = 2
    check_new_participants_every = 5  # todo: a changer : 30

    now = dt.datetime.now(s.TIMEZONE)
    i = 0

    participants_info = await conn.check_for_new_participants_in_main_channel(first_time=True)
    # todo: first_time et known_participants sont redondants (y'a pas 1 sans l'autre, enfin presque...)

    while now < s.END_LISTENING_LOOP:

        now = dt.datetime.now(s.TIMEZONE)

        i += 1
        time.sleep(deltamin)  # todo : faire plutot le delta avec la précédente itération
        logmsg = "\tNouvelle itération de la boucle d'écoute ({})".format(now)
        logger.write(logmsg)

        if i % check_new_participants_every == 0:
            known_participants = [pi['participant'] for pi in participants_info]
            participants_info = await conn.check_for_new_participants_in_main_channel(
                known_participants=known_participants)
 
        for j, pi in enumerate(participants_info):

            participant = pi['participant']
            channel = pi['1to1_channel']

            if not conn.is_bot(participant):
                msgs, updated_participant = await conn.check_for_new_messages(participant,
                                                                              channel)  # todo : est ce qu'on enregistre
                # tous les mesages dans la BDD? oui ce serait bien

                if participant.is_scribe():
                    for m in msgs:
                        # todo : !!! que se passe t'il si ME est à la fois scribe et que
                        # SEND_ONLY_TO_ME est activé? Plus généralement, s'assure t'on que les messages envoyés aux
                        # scribes ne reviennent pas ?
                        updated_participant = await analyser.analyse_message_from_scribe(m, updated_participant,
                                                                                         channel, participants_info)
                        # todo : ici , n'envoyer que ce qu'il y a d'utile dans l'argument participants_info,
                        #  en effet c'est dangereux car participants_info n'est pas updaté avec le nouveau
                        #  updated_participant
                else:
                    for m in msgs:
                        logger.debug("User '%s'[id='%s'] sent message to bot at %s : '%s'"
                                     % (participant.display_name,
                                        participant.get_normalised_id(),
                                        m.received_at.strftime(
                                            "%d-%m-%y %H:%M:%S"),
                                        m.message_str))

                        updated_participant = \
                            await analyser.analyse_message_from_normal_participant(m,
                                                                                   updated_participant,
                                                                                   channel)

                participants_info[j]['participant'] = updated_participant

    if now >= s.END_LISTENING_LOOP:
        print("La date de fin spécifiée est antérieure à la date actuelle.")


with TelegramConnection(db) as conn:
    analyser = MessageAnalyser(conn, actions)
    conn.tg_client.loop.run_until_complete(main(conn, analyser))
