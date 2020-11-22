from suggestion_loop import main_suggestion_loop
from listening_loop import main_listening_loop
from daemon_loops.modules.database import DataBase
from sandbox_loop import sandbox_loop
from daemon_loops.modules.participants_actions import actions
from daemon_loops.modules.telegram import TelegramConnection
from daemon_loops.modules.twitterstorm_utils import MessageAnalyser
import asyncio

async def loops(conn, analyser):
    a = asyncio.create_task(main_listening_loop(conn, analyser))
    print(21993,"\nOui euh bon faudra réactuver la boucl de suggestion\n")
    #b = asyncio.create_task(main_suggestion_loop(conn))
    c = asyncio.create_task(sandbox_loop(conn))  # todo_critical : enlever sandbox
    await a
    await c

def run():
    db = DataBase()
    with TelegramConnection(db) as conn:
        analyser = MessageAnalyser(conn, actions)
        conn.run_with_async_loop(loops(conn, analyser))

if __name__ == "__main__":
    run()