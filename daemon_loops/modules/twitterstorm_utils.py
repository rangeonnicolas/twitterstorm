import os
import datetime as dt

import settings as s
import asyncio

import daemon_loops.modules.logging as logging

def create_dirs_if_not_exists(dirs_list):
    for dir_ in dirs_list:
        if not os.path.exists(dir_):
            os.makedirs(dir_)



def get_planned_messages_loop():
    return __import__(s.SANDBOX_MODULE_NAME).sandbox_loop

def get_time_before_suggesting():
    return __import__(s.SANDBOX_MODULE_NAME).TIME_BEFORE_SUGGESTING

class TwitterstormError(Exception):  # todo_es : arevoir
    pass

class TwitterstormSettingsError(TwitterstormError):  # todo_es : a exploiter
    def __init__(self, message, file):
        #logging.test(10001)
        #super().__init__(message, prefix="- ERREUR DANS LE FICHIER DE CONFIGURATION '{}.py':  ".format(file.__name__))
        pass


async def wait_for_next_iteration(last_loop_execution, time_between_two_iterations):
    time_between_two_iterations = dt.timedelta(0, 0, 0, time_between_two_iterations)
    current_delta = dt.datetime.now(s.TIMEZONE) - last_loop_execution
    if current_delta < time_between_two_iterations:
        remaining_time = time_between_two_iterations - current_delta
        #time.sleep(remaining_time.total_seconds())
        await asyncio.sleep(remaining_time.total_seconds())
    return dt.datetime.now(s.TIMEZONE)


async def init(conn):  # todo_f: affichcer dans les logs un résumé du chargement des données
    # todo_chk: vérifier aussi, en cas de relancement d el'appli après plantage, qu'il n'y a pas d'actions
    #  en attente (ex: le scribe a un message qu'il n'a pas validé)
    logging.test(10002)
    create_dirs_if_not_exists([s.DATA_DIR, s.LOG_DIR, s.SESSION_DIR])

    await conn.init_conf()
