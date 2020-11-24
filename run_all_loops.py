from suggestion_loop import main_suggestion_loop
from listening_loop import main_listening_loop
from daemon_loops.modules.database import DataBase
from daemon_loops.modules.participants_actions import actions
from daemon_loops.modules.telegram import TelegramConnection
from daemon_loops.modules.twitterstorm_utils import init, get_planned_messages_loop
from daemon_loops.modules.message_analyser import MessageAnalyser
import asyncio
import daemon_loops.settings as s


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
    init()
    db = DataBase()
    with TelegramConnection(db) as conn:
        analyser = MessageAnalyser(conn, actions)
        conn.run_with_async_loop(loops(conn, analyser))

if __name__ == "__main__":
    run()