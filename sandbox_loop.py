import datetime as dt
from daemon_loops.modules.twitterstorm_utils import wait_for_next_iteration
from daemon_loops.modules.database import DataBase
from daemon_loops.modules.logger import logger
from daemon_loops.modules.telegram import TelegramConnection
import daemon_loops.modules.sandbox as s
from daemon_loops.modules.twitterstorm_utils import init


async def sandbox_loop(conn):

    now = dt.datetime.now(s.TIMEZONE)

    last_loop_execution = dt.datetime(1970,1,1, tzinfo=s.TIMEZONE)

    while now < s.END_SANDBOX_LOOP :
        last_loop_execution = await wait_for_next_iteration(last_loop_execution, s.NEW_SANDBOX_LOOP_ITERATION_EVERY)

        now = dt.datetime.now(s.TIMEZONE)
        logmsg = "\tNouvelle itération de la boucle SANDBOX ({})".format(now)
        logger.write(logmsg)

        participants_info = await conn.fetch_all_participants(consent=True)

        for j, pi in enumerate(participants_info):

            participant = s.SandboxParticipant(pi['participant'])
            channel = pi['1to1_channel']

            if not conn.is_bot(participant) and not participant.is_scribe():
                planned_msgs = await participant.check_for_planned_message(now, s.PLANNED_MESSAGES)
                for m in planned_msgs:
                    await conn.send(participant, channel, m['message'])
                    await participant.record_planned_message(m)

    if now >= s.END_SANDBOX_LOOP:
        print(
            "La date de fin spécifiée est antérieure à la date actuelle.")  # todo_es : difféencier les différentes
        # boucles dans le message

def run():
    init()
    db = DataBase()
    with TelegramConnection(db) as conn:
        conn.run_with_async_loop(sandbox_loop(conn))

if __name__ == "__main__":
    run()
