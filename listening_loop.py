import datetime as dt
from daemon_loops.modules.twitterstorm_utils import wait_for_next_iteration
import daemon_loops.settings as s  # todo : renommer l'alias
from daemon_loops.modules.database import DataBase
from daemon_loops.modules.logger import logger
from daemon_loops.modules.participants_actions import actions
from daemon_loops.modules.telegram import TelegramConnection
from daemon_loops.modules.twitterstorm_utils import init, MessageAnalyser
import asyncio

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
# todo : renommer les noms des fichiers qui st en francais


async def main_listening_loop(conn, analyser):

    init()

    now = dt.datetime.now(s.TIMEZONE)

    last_loop_execution = dt.datetime(1970,1,1, tzinfo=s.TIMEZONE)
    last_new_participants_check = now

    participants_info = await conn.check_for_new_participants_in_main_channel(first_time=True)
    # todo: first_time et known_participants sont redondants (y'a pas 1 sans l'autre, enfin presque...)

    while now < s.END_LISTENING_LOOP:
        last_loop_execution = await wait_for_next_iteration(last_loop_execution, s.NEW_LISTENING_LOOP_ITERATION_EVERY)

        now = dt.datetime.now(s.TIMEZONE)
        logmsg = "\tNouvelle itération de la boucle d'écoute ({})".format(now)
        logger.write(logmsg)

        if now - last_new_participants_check >= dt.timedelta(0,0,0,s.CHECK_NEW_PARTICIPANTS_EVERY):
            # todo : la vérification des nouveaux participante.s doit elle bien ête dans cette boucle ?
            participants_info = await conn.check_for_new_participants_in_main_channel(
                known_participants_info=participants_info)
            last_new_participants_check = dt.datetime.now(s.TIMEZONE)

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

def run():
    db = DataBase()
    with TelegramConnection(db) as conn:
        analyser = MessageAnalyser(conn, actions)
        conn.run_with_async_loop(main_listening_loop(conn, analyser))

if __name__ == "__main__":
    run()