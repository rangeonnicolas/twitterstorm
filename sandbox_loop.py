import datetime as dt
from daemon_loops.modules.twitterstorm_utils import wait_for_next_iteration
from daemon_loops.modules.database import DataBase
import daemon_loops.modules.logging as logging
from daemon_loops.modules.telegram import TelegramConnection
import daemon_loops.modules.sandbox as sb
from daemon_loops.modules.twitterstorm_utils import init
from settings.sandbox_settings import TIME_BEFORE_SUGGESTING, PLANNED_MESSAGES, END_SANDBOX_LOOP, \
    NEW_SANDBOX_LOOP_ITERATION_EVERY

TIME_BEFORE_SUGGESTING = TIME_BEFORE_SUGGESTING  # todo_es cf ctrl+f 'return __import__(
#                                                    s.SANDBOX_MODULE_NAME).TIME_BEFORE_SUGGESTING'


async def _loop_action(conn):
    now = dt.datetime.now(sb.TIMEZONE)
    logmsg = "SANDBOX_LOOP - Nouvelle itération de la boucle."
    logging.info(logmsg)

    participants_info = await conn.fetch_all_participants(consent=True)

    for j, pi in enumerate(participants_info):

        participant = sb.SandboxParticipant(pi['participant'])
        channel = pi['1to1_channel']

        if not conn.is_bot(participant) and not await participant.is_scribe() and not await conn.is_admin(participant):
            planned_msgs = await participant.check_for_planned_message(now, PLANNED_MESSAGES)
            for m in planned_msgs:
                await conn.send(participant, channel, m['message'])
                await participant.record_planned_message(m)

    return now


async def sandbox_loop(conn):
    await init(conn)

    now = dt.datetime.now(sb.TIMEZONE)

    last_loop_execution = dt.datetime(1970, 1, 1, tzinfo=sb.TIMEZONE)

    await sb.populate();
    # todo_es : populate ne doit s'exécuter que si la campagne est nouvelle (ou si effacement BDD)

    while now < END_SANDBOX_LOOP:

        last_loop_execution = await wait_for_next_iteration(last_loop_execution, NEW_SANDBOX_LOOP_ITERATION_EVERY)

        try:
            now = await _loop_action(conn)
        except KeyboardInterrupt as e:
            raise e
        except Exception:
            logging.exception("[ERREUR AU SEIN DE LA BOUCLE] Erreur inconnue dans sandbox_loop")

    if now >= END_SANDBOX_LOOP:
        logging.info("Fin de la boucle SANDBOX_LOOP car END_SANDBOX_LOOP = %s" % END_SANDBOX_LOOP)


def run():
    try:
        db = DataBase()
        with TelegramConnection(db) as conn:
            conn.run_with_async_loop(sandbox_loop(conn))
    except KeyboardInterrupt as e:
        raise e
    except Exception:
        logging.exception("[ARRET DU PROGRAMME] Erreur inconnue au niveau de sandbox_loop")


if __name__ == "__main__":
    run()
