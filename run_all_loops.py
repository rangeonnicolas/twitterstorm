from suggestion_loop import main_suggestion_loop
from listening_loop import main_listening_loop
from daemon_loops.modules.database import DataBase
from daemon_loops.modules.participants_actions import actions, admin_actions
from daemon_loops.modules.telegram import TelegramConnection
from daemon_loops.modules.twitterstorm_utils import get_planned_messages_loop
from daemon_loops.modules.message_analyser import MessageAnalyser
import asyncio
from settings import settings as s
import daemon_loops.modules.logging as logging

# todo_cr : il arrivue que le programme finisse sans rien dire alors que eror/log est rempli. pas cool
# todo_chk : assouplir les regles de filtrage par is_reachable sinon c'est incompréhensible au debuggage,
#  notamment dans _get_participants_from_channel
# todo_es : renommer les noms des fichiers qui st en francais

async def loops(conn, analyser):
    a = asyncio.create_task(main_listening_loop(conn, analyser))
    b = asyncio.create_task(main_suggestion_loop(conn))
    if s.USE_SANDBOX:
        loop_fn = get_planned_messages_loop()
        c = asyncio.create_task(loop_fn(conn))
    await a
    await b
    if s.USE_SANDBOX:
        await c

def run():
    try:
        db = DataBase()
        with TelegramConnection(db) as conn:
            analyser = MessageAnalyser(conn, actions, admin_actions)
            conn.run_with_async_loop(loops(conn, analyser))
    except KeyboardInterrupt as e:
        raise e
    except Exception as e:
        logging.exception("[ARRET DU PROGRAMME] Erreur inconnue au niveau de run_all_loops")

if __name__ == "__main__":
    run()