import datetime as dt
import os
import traceback
import settings as s
from telethon.errors.rpcerrorlist import FloodWaitError


_d = s.LOG_DIR

if not os.path.exists(_d):
    os.makedirs(_d)

now = dt.datetime.now(s.TIMEZONE).isoformat()

_former_log = os.path.join(_d, "former_log_" + now)
_current_log = os.path.join(_d, "log")
_former_error_log = os.path.join(_d, "former_error_log_" + now)
_current_error_log = os.path.join(_d, "error_log")

open(_former_log, 'w+')
open(_current_log, 'w+')
open(_former_error_log, 'w+')
open(_current_error_log, 'w+')

def _write_log_files(msg):
    with open(_former_log, 'a+') as f:
        f.write(msg + "\n")
    with open(_current_log, 'a+') as f:
        f.write(msg + "\n")

def _write_error_log_files(msg, traceback = None):
    if traceback is not None:
        msg = "%s\n%s\n\n%s\n%s" % ('-'*30, msg, traceback, '-'*30)
    with open(_former_error_log, 'a+') as f:
        f.write(msg + "\n")
    with open(_current_error_log, 'a+') as f:
        f.write(msg + "\n")

def _write_in_files(level, msg, traceback = None):
    if level in ['INFO', 'WARNING', 'ERROR', 'CRITICAL', 'EXCEPTION']:
        _write_log_files(msg)
    if level in ['ERROR', 'CRITICAL', 'EXCEPTION']:
        _write_error_log_files(msg, traceback = traceback)

def _format_msg(msg, level):
    #date = dt.datetime.now(s.TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")
    date = dt.datetime.now(s.TIMEZONE).isoformat()
    return "[%s][%s] %s" % (date, level, msg)

class Logger:
    def __init__(self):
        self.last_exception = dt.datetime.now(s.TIMEZONE)
        self.exception_counter = 0

    def log(self, level, msg,  traceback = None):
        if level not in ['ERROR', 'CRITICAL', 'EXCEPTION']:
            self._log(level, msg, traceback=traceback)
        else:
            delta = dt.datetime.now(s.TIMEZONE) - self.last_exception
            if delta < dt.timedelta(0,s.MIN_TIME_BETWEEN_TWO_ERROR_LOGGINGS):
                self.exception_counter += 1
            else:
                if self.exception_counter > 0:
                    self._log("ERROR", "%i erreur(s) passées sous silence" % self.exception_counter) # todo_es revoir wording (plus précis)
                self._log(level, msg,  traceback = traceback)

                self.last_exception = dt.datetime.now(s.TIMEZONE)
                self.exception_counter = 0

    def _log(self, level, msg,  traceback = None):
        print(92783, "accès log")
        msg = _format_msg(msg, level)
        if s.ENV_TYPE == "DEV":
            print(msg)
            if traceback is not None:
                print()
                print(traceback if traceback is not None else "")
        _write_in_files(level, msg,  traceback = traceback)


logger = Logger()

def debug(msg, *args):
    logger.log("DEBUG", msg)

def info(msg, *args):
    logger.log("INFO", msg)

def warning(msg, *args):
    logger.log("MSG", msg)

# a utiliser si on peut se permettre de continuer le code qui suit l'appel à exception() [donc si l'erreur n'est pas si critique que ça]
def error(msg, *args):
    from daemon_loops.modules.twitterstorm_utils import TwitterstormError
    #logger.log("ERROR", msg)
    exception(TwitterstormError(msg), level = "ERROR")

# a utiliser quand le code qui suit l'appel à critical ne doit pas être exécuté (en effet critical() lève une erreur)
def critical(msg, *args):
    from daemon_loops.modules.twitterstorm_utils import TwitterstormError
    logger.log("CRITICAL", msg)
    raise TwitterstormError(msg)

# a utiliser si on peut se permettre de continuer le code qui suit l'appel à exception() [donc si l'erreur n'est pas si critique que ça]
def exception(e, exc_info=None, level = None):
    # todo_es : rapatrier à dans TgClientWrapper, une fois que l'on y aura rappartié la gestion des excaptions de get_entity et get_input_entity
    #if isinstance(e, FloodWaitError):

    stack = traceback.format_exc()
    msg = "\n" + str(e)
    if exc_info:
        stack += "\nErreur initiale:\n%s" % exc_info

    level = level if level is not None else "EXCEPTION"
    logger.log(level ,msg, traceback= stack)












def test(nb):
        pass


def _generate_ints(self):
        a = [i for i in range(10000, 1 + 10011)]
        b = [i for i in range(20000, 1 + 20100)]
        c = [i for i in range(30000, 1 + 30036)]
        l = a + b + c
        with open("data/TEST_INTS.csv", "w+") as f:
            f.write("id\tutile\n")
            for i in l:
                f.write("%i\t1\n" % i)
        return None
