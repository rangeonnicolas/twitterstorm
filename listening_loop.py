import datetime as dt
from daemon_loops.modules.twitterstorm_utils import wait_for_next_iteration
import daemon_loops.settings as s  # todo_es : renommer l'alias
from daemon_loops.modules.database import DataBase
from daemon_loops.modules.logger import logger
from daemon_loops.modules.participants_actions import actions
from daemon_loops.modules.telegram import TelegramConnection
from daemon_loops.modules.twitterstorm_utils import init
from daemon_loops.modules.message_analyser import MessageAnalyser
import asyncio

async def main_listening_loop(conn, analyser):

    now = dt.datetime.now(s.TIMEZONE)

    last_loop_execution = dt.datetime(1970,1,1, tzinfo=s.TIMEZONE)
    last_new_participants_check = now

    participants_info = await conn.check_for_new_participants_in_main_channel(first_time=True)
    # todo_f: first_time et known_participants sont redondants (y'a pas 1 sans l'autre, enfin presque...)

    while now < s.END_LISTENING_LOOP:
        last_loop_execution = await wait_for_next_iteration(last_loop_execution, s.NEW_LISTENING_LOOP_ITERATION_EVERY)

        now = dt.datetime.now(s.TIMEZONE)
        logmsg = "\tNouvelle itération de la boucle d'écoute ({})".format(now)
        logger.write(logmsg)

        if now - last_new_participants_check >= dt.timedelta(0,0,0,s.CHECK_NEW_PARTICIPANTS_EVERY):
            # todo_chk : la vérification des nouveaux participante.s doit elle bien ête dans cette boucle ?
            participants_info = await conn.check_for_new_participants_in_main_channel(
                known_participants_info=participants_info)
            last_new_participants_check = dt.datetime.now(s.TIMEZONE)

        for j, pi in enumerate(participants_info):

            participant = pi['participant']
            channel = pi['1to1_channel']

            if not conn.is_bot(participant):
                msgs, updated_participant = await conn.check_for_new_messages(participant,
                                                                              channel)
                # todo_f : est ce qu'on enregistre tous les mesages dans la BDD? oui ce serait bien
                # todo_f : définir dans la conf un niveau d'enregsitrement (ts les messages ou juste ls infos
                #  necessaires?)

                if participant.is_scribe():
                    for m in msgs:
                        # todo_cr : !!! que se passe t'il si ME est à la fois scribe et que
                        #  SEND_ONLY_TO_ME est activé? Plus généralement, s'assure t'on que les messages envoyés aux
                        #  scribes ne reviennent pas ?
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
    init()
    db = DataBase()
    with TelegramConnection(db) as conn:
        analyser = MessageAnalyser(conn, actions)
        conn.run_with_async_loop(main_listening_loop(conn, analyser))

if __name__ == "__main__":
    run()