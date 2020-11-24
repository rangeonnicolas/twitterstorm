import datetime as dt
import os
import daemon_loops.modules.advanced_settings as s


# todo_es : a mettre utrepart quand on aura résolu la question du logger (on le met ici à cause de circular imports)
def create_dirs_if_not_exists(dirs_list):
    for dir_ in dirs_list:
        if not os.path.exists(dir_):
            os.makedirs(dir_)

class ErrorLogger:
    def log(self, err, orig_err=None):
        pass

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

    def warning(self, *args):
        return self.write(*args)

    def test(self, nb):
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

logger = Logger()
error_logger = ErrorLogger()

if __name__ == "__main__":  # todo_es : aretirer
    Logger()._generate_ints()
