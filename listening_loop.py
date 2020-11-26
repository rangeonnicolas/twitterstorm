import datetime as dt
from daemon_loops.modules.twitterstorm_utils import wait_for_next_iteration
import settings as s  # todo_es : renommer l'alias
from daemon_loops.modules.database import DataBase
import daemon_loops.modules.logging as logging
from daemon_loops.modules.participants_actions import actions, admin_actions
from daemon_loops.modules.telegram import TelegramConnection
from daemon_loops.modules.twitterstorm_utils import init
from daemon_loops.modules.message_analyser import MessageAnalyser


async def _loop_action(conn, analyser, now, last_new_participants_check, participants_info):

    now = dt.datetime.now(s.TIMEZONE)
    logmsg = "    LISTENING_LOOP - Nouvelle itération de la boucle."
    logging.info(logmsg)

    if now - last_new_participants_check >= dt.timedelta(0, 0, 0, s.CHECK_NEW_PARTICIPANTS_EVERY):
        # todo_chk : la vérification des nouveaux participante.s doit elle bien ête dans cette boucle ?
        participants_info = await conn.check_for_new_participants_in_main_channel(
            known_participants_info=participants_info)
        last_new_participants_check = dt.datetime.now(s.TIMEZONE)

    for j, pi in enumerate(participants_info):

        participant = pi['participant']
        channel = pi['1to1_channel']

        if not conn.is_bot(participant):  # todo_es méthode à mettre plutot dans la classe participant
            msgs, updated_participant = await conn.check_for_new_messages(participant,
                                                                          channel)
            # todo_f : est ce qu'on enregistre tous les mesages dans la BDD? oui ce serait bien
            # todo_f : définir dans la conf un niveau d'enregsitrement (ts les messages ou juste ls infos
            #  necessaires?)

            if await participant.is_scribe():
                for m in msgs:
                    updated_participant = await analyser.analyse_message_from_scribe(m, updated_participant,
                                                                                     channel, participants_info)
            elif await conn.is_admin(participant):  # todo_es méthode à mettre plutot dans la classe participant
                for m in msgs:
                    updated_participant = await analyser.analyse_message_from_admin(m, updated_participant,
                                                                                    channel, participants_info)
            else:
                for m in msgs:
                    updated_participant = \
                        await analyser.analyse_message_from_normal_participant(m,
                                                                               updated_participant,
                                                                               channel)

            participants_info[j]['participant'] = updated_participant

    return now, last_new_participants_check, participants_info


async def main_listening_loop(conn, analyser):

    await init(conn)

    now = dt.datetime.now(s.TIMEZONE)

    last_loop_execution = dt.datetime(1970,1,1, tzinfo=s.TIMEZONE)
    last_new_participants_check = now

    participants_info = await conn.check_for_new_participants_in_main_channel(first_time=True)
    # todo_f: first_time et known_participants sont redondants (y'a pas 1 sans l'autre, enfin presque...)

    while now < s.END_LISTENING_LOOP:
        last_loop_execution = await wait_for_next_iteration(last_loop_execution, s.NEW_LISTENING_LOOP_ITERATION_EVERY)

        try:
            now, last_new_participants_check, participants_info = await _loop_action(conn, analyser, now, last_new_participants_check, participants_info)
        except KeyboardInterrupt as e:
            raise e
        except:
            logging.exception("[ERREUR AU SEIN DE LA BOUCLE] Erreur inconnue dans listening_loop")

    if now >= s.END_LISTENING_LOOP:
        logging.info("Fin de la boucle LISTENING_LOOP car END_LISTENING_LOOP = %s" % s.END_LISTENING_LOOP)

def run():
    try:
        db = DataBase()
        with TelegramConnection(db) as conn:
            analyser = MessageAnalyser(conn, actions, admin_actions)
            conn.run_with_async_loop(main_listening_loop(conn, analyser))
    except KeyboardInterrupt as e:
        raise e
    except Exception as e:
        logging.exception("[ARRET DU PROGRAMME] Erreur inconnue au niveau de listening_loop")

if __name__ == "__main__":
    run()