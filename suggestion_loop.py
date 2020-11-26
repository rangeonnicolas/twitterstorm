import datetime as dt
import random

from daemon_loops.modules.twitterstorm_utils import wait_for_next_iteration
from settings import settings as s
from daemon_loops.modules.database import DataBase
import daemon_loops.modules.logging as logging
from daemon_loops.modules.telegram import TelegramConnection
from daemon_loops.modules.twitterstorm_utils import init

# todo_es : il n'est pas dit que d'autres applis (ex whatsapp) necessite le 1to1channel pour envoyer
#  un message. ainsi, la forme participant_info = {'participant': , '1to1_channel': } doit être inconnue du fichier
#  connection.py et encapsulée par le fichier telegram.py, ou bien le 1to1 channel peut même être un attribut de la
#  classe TelegramParticipant.


async def _loop_action(conn, now, last_new_participants_check):

    now = dt.datetime.now(s.TIMEZONE)
    logmsg = "  SUGGESTION_LOOP - Nouvelle itération de la boucle."
    logging.info(logmsg)

    if s.USE_SANDBOX or await conn.right_time_for_suggestions():
        # todo_f : faire en sorte que ce soit
        #  dynmique le start et end (genre c'est le scribe qui envoie des signaux)

        participants_info = await conn.fetch_all_participants()

        for j, pi in enumerate(participants_info):

            participant = pi['participant']
            channel = pi['1to1_channel']

            if not conn.is_bot(participant) and not await participant.is_scribe() and not await conn.is_admin(participant):

                now = dt.datetime.now(s.TIMEZONE)

                if (not s.USE_SANDBOX) or participant.right_time_to_suggest_if_sandbox(now):

                    delta = dt.timedelta(0, 60 * participant.suggestions_frequency)
                    if participant.last_suggestion_url_or_text is None or (
                            participant.last_suggestion_url_or_text + delta <= now):
                        if random.choice([0, 1]):
                            updated_participant, is_sent = await conn.send_a_tweet_url(participant, channel)
                            if not is_sent:
                                updated_participant, is_sent = await conn.send_suggestion(participant, channel)
                        else:
                            updated_participant, is_sent = await conn.send_suggestion(participant, channel)
                            if not is_sent:
                                updated_participant, is_sent = await conn.send_a_tweet_url(participant, channel)
                        participants_info[j]['participant'] = updated_participant

    return now, last_new_participants_check


async def main_suggestion_loop(conn):

    await init(conn)

    now = dt.datetime.now(s.TIMEZONE)

    last_loop_execution = dt.datetime(1970, 1, 1, tzinfo=s.TIMEZONE)
    last_new_participants_check = now

    # participants_info = await conn.check_for_new_participants_in_main_channel(first_time=True)

    while now < s.END_SUGGESTION_LOOP:
        last_loop_execution = await wait_for_next_iteration(last_loop_execution, s.NEW_SUGGESTION_LOOP_ITERATION_EVERY)

        try:
            # todo_es dans les 3 boucles, now n'est pas forcement modifié par _loop_action (en cas de levée d'erreur).
            #  sortir donc le now de _llop_action
            now, last_new_participants_check = await _loop_action(conn, now, last_new_participants_check)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            logging.exception("[ERREUR AU SEIN DE LA BOUCLE] Erreur inconnue dans suggestion_loop")


    if now >= s.END_SUGGESTION_LOOP:
        logging.info("Fin de la boucle SUGGESTION_LOOP car END_SUGGESTION_LOOP = %s" % s.END_SUGGESTION_LOOP)

def run():
    try:
        db = DataBase()
        with TelegramConnection(db) as conn:
            conn.run_with_async_loop(main_suggestion_loop(conn))
    except KeyboardInterrupt as e:
        raise e
    except Exception as e:
        logging.exception("[ARRET DU PROGRAMME] Erreur inconnue au niveau de suggestion_loop")

if __name__ == "__main__":
    run()