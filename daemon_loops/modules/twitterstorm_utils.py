import os
import time
import datetime as dt

from asgiref.sync import sync_to_async

import daemon_loops.settings as s
from daemon_loops.modules.logger import logger, create_dirs_if_not_exists
import asyncio

def get_planned_messages_loop():
    return __import__(s.SANDBOX_MODULE_NAME).sandbox_loop

def get_time_before_suggesting():
    return __import__(s.SANDBOX_MODULE_NAME).TIME_BEFORE_SUGGESTING

class TwitterstormError(Exception):  # todo_es : arevoir
    def __init__(self, message, prefix="- ERREUR :  "):
        os.system('cls')  # Windows
        os.system('clear')  # Linux, Mac
        super().__init__(message)
        print("\n\n")
        print(prefix + message)
        print("\n" * 10 + "Aide au debuggage :\n")
        logger.test(10000)


class TwitterstormSettingsError(TwitterstormError):
    def __init__(self, message, file):
        logger.test(10001)
        super().__init__(message, prefix="- ERREUR DANS LE FICHIER DE CONFIGURATION '{}.py':  ".format(file.__name__))


async def wait_for_next_iteration(last_loop_execution, time_between_two_iterations):
    time_between_two_iterations = dt.timedelta(0, 0, 0, time_between_two_iterations)
    current_delta = dt.datetime.now(s.TIMEZONE) - last_loop_execution
    if current_delta < time_between_two_iterations:
        remaining_time = time_between_two_iterations - current_delta
        #time.sleep(remaining_time.total_seconds())
        await asyncio.sleep(remaining_time.total_seconds())
    return dt.datetime.now(s.TIMEZONE)


def init():  # todo_f: affichcer dans les logs un résumé du chargement des données
    # todo_chk: vérifier aussi, en cas de relancement d el'appli après plantage, qu'il n'y a pas d'actions
    #  en attente (ex: le scribe a un message qu'il n'a pas validé)
    logger.test(10002)
    create_dirs_if_not_exists([s.DATA_DIR, s.LOG_DIR, s.SESSION_DIR])

