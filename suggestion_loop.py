import datetime as dt
from daemon_loops.modules.twitterstorm_utils import wait_for_next_iteration
import daemon_loops.settings as s
from daemon_loops.modules.database import DataBase
from daemon_loops.modules.logger import logger
from daemon_loops.modules.telegram import TelegramConnection

# todo : todo_refactoring : il n'est pas dit que d'autres applis (ex whatsapp) necessite le 1to1channel pour envoyer un message.
# todo : ... ainsi, la forme participant_info = {'participant': , '1to1_channel': } doit être inconnue du fichier connection.py et encapsulée par le fichier telegram.py, ou bien le 1to1 channel peut même être un attribut de la classe TelegramParticipant.

async def main_suggestion_loop(conn):

    now = dt.datetime.now(s.TIMEZONE)

    last_loop_execution = dt.datetime(1970,1,1, tzinfo=s.TIMEZONE)
    last_new_participants_check = now

    #participants_info = await conn.check_for_new_participants_in_main_channel(first_time=True)

    while now < s.END_SUGGESTION_LOOP:
        last_loop_execution = await wait_for_next_iteration(last_loop_execution, s.NEW_SUGGESTION_LOOP_ITERATION_EVERY)

        now = dt.datetime.now(s.TIMEZONE)
        logmsg = "\tNouvelle itération de la boucle de suggestions ({})".format(now)
        logger.write(logmsg)

        participants_info = await conn.fetch_all_participants()

        for j, pi in enumerate(participants_info):

            participant = pi['participant']
            channel = pi['1to1_channel']

            if not conn.is_bot(participant) and not participant.is_scribe():
                if participant._last_suggestion_is_far_enough():


                    # :
                    # else:
                    # participants_info[j]['participant'] = updated_participant
                    pass

    if now >= s.END_SUGGESTION_LOOP:
        print("La date de fin spécifiée est antérieure à la date actuelle.")  # todo : difféencier les différentes boucles dans le message

def run():
    init()
    db = DataBase()
    with TelegramConnection(db) as conn:
        conn.run_with_async_loop(main_suggestion_loop(conn))

if __name__ == "__main__":
    run()