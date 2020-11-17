import datetime as dt
import os
import modules.advanced_settings as s


# todo : a mettre utrepart quand on aura résolu la question du logger (on le met ici à cause de circular imports)
def create_dirs_if_not_exists(dirs_list):
    for dir_ in dirs_list:
        if not os.path.exists(dir_):
            os.makedirs(dir_)


class Logger:
    def __init__(self, d=s.LOG_DIR):
        filename1 = os.path.join(d, "log_" + dt.datetime.now(s.TIMEZONE).isoformat())
        filename2 = os.path.join(d, "log")
        create_dirs_if_not_exists([s.LOG_DIR])
        open(filename1, 'w+')
        open(filename2, 'w+')
        self.filename1 = filename1
        self.filename2 = filename2

    def write(self, msg):
        print(msg)
        print()
        with open(self.filename1, 'a+') as f:
            f.write(msg + "\n")
        with open(self.filename2, 'a+') as f:
            f.write(msg + "\n")

    def debug(self, msg):
        self.write(msg)

    def error(self, *args):
        return self.write(*args)

    def test(self, nb):
        pass
