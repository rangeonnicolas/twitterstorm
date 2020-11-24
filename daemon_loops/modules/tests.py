import _asyncio
import telethon

from daemon_loops.modules.telegram import TelegramClientWrapper
from listening_loop import main_listening_loop
import datetime as dt
import json
from daemon_loops.modules.logger import create_dirs_if_not_exists
import os
import pickle
from dateutil.parser import parse

from daemon_loops.modules.twitterstorm_utils import TwitterstormError


SAVE_EVERY = 5


def f1(args):
    return json.dumps(args)
def f2(data):
    return json.loads(data)


class TelegramClientTester(TelegramClientWrapper):
        def __init__(self, session, api_id, api_hash, recorder, mode):
            TelegramClientWrapper.__init__(self, session, api_id, api_hash)
            self.recorder = recorder
            self.rec_mode = mode

        async def get_messages(self, *args, **kwargs):
            class FakeTgMessage:
                @classmethod
                def from_tgmsg(cls, tg_message):
                    self = cls()
                    self.sender_id = tg_message.sender_id
                    self.id = tg_message.id
                    self.message = tg_message.message
                    self.date = tg_message.date.isoformat()
                    return self
                @classmethod
                def from_dict(cls, dict_):
                    self = cls()
                    for key in dict_:
                        setattr(self, key, dict_[key])
                    self.date = parse(self.date)
                    return self

            result = await TelegramClientWrapper.get_messages(self, *args, **kwargs)
            def f1(data):
                result = [FakeTgMessage.from_tgmsg(m).__dict__ for m in data]
                return json.dumps(result)
            def f2(data):
                # class A(telethon.tl.patched.Message):
                #     def __init__(self, initial_data):
                #         for key in initial_data:
                #             setattr(self, key, initial_data[key])
                l = json.loads(data)
                return [FakeTgMessage.from_dict(e) for e in l]

            res = self.recorder.record_or_serve(self.rec_mode, "tg_client.get_messages", result, f1, f2)
            return res

        async def get_input_entity(self, *args):

            #def f1(id_):
            #    return json.dumps({"user_id":id_})

            #def f2(data, self):
            #    d = json.loads(data)
            #    return d['user_id']

            args = self.recorder.record_or_serve(self.rec_mode, "tg_client.get_input_entity", args, f1, f2)
            return await TelegramClientWrapper.get_input_entity(self, *args)

        async def get_entity(self, *args):
            args = self.recorder.record_or_serve(self.rec_mode, "tg_client.get_entity", args, f1, f2)
            return await TelegramClientWrapper.get_entity(self, *args)

        def iter_participants(self, *args, **kwargs):
            class AIter:
                def __init__(self, l, recorder, rec_mode):
                    self.l = l
                    self.recorded = []
                    self.recorder = recorder
                    self.rec_mode = rec_mode
                def __aiter__(self):
                    return self
                async def __anext__(self):
                    try:
                        new_element = await self.l.__anext__()
                    except StopAsyncIteration:
                        data_to_record = json.dumps([str(pickle.dumps(e)) for e in self.recorded])
                        self.recorder.record_or_serve(self.rec_mode, "tg_client.iter_participants", data_to_record, f1, f2)
                        raise StopAsyncIteration
                    self.recorded += [new_element]
                    return new_element
            result_orig = TelegramClientWrapper.iter_participants(self, *args, **kwargs)
            return AIter(result_orig, self.recorder, self.rec_mode)

        async def send_message(self, *args, **kwargs):
            return await TelegramClientWrapper.send_message(self, *args, **kwargs)

        async def get_dialogs(self, *args, **kwargs):
            return await TelegramClientWrapper.get_dialogs(self, *args, **kwargs)

        @property
        def loop(self):
            return super().loop

        def connect(self):
            return TelegramClientWrapper.connect(self)

        def disconnect(self):
            return TelegramClientWrapper.disconnect(self)

        async def send_code_request(self, *args, **kwargs):
            return await TelegramClientWrapper.send_code_request(self, *args, **kwargs)

        async def is_user_authorized(self):
            return await TelegramClientWrapper.is_user_authorized(self)

        async def sign_in(self, *args, **kwargs):
            return await TelegramClientWrapper.sign_in(self, *args, **kwargs)


class Recorder:
    def __init__(self):
        self.started_at = dt.datetime.now()
        self.id = str(self.started_at.isoformat())
        self.recorded_data = {}
        self.last_file_save = self.started_at

    def record_or_serve(self, mode, data_id, data, f1, f2, f1args=[], f2args=[]):
        data = f1(data, *f1args)
        to_serve = f2(data, *f2args)

        if data_id not in self.recorded_data.keys():
            self.recorded_data[data_id] = {}
        if type(data) != str and type(data) != bytes:
            raise TwitterstormError("L'argument 'data' doit être de type 'str' or 'bytes'")
        timestamp_key = (dt.datetime.now() - self.started_at).microseconds
        self.recorded_data[data_id][timestamp_key] = data

        now = dt.datetime.now()
        if now - self.last_file_save >= dt.timedelta(0, SAVE_EVERY):
            self.last_file_save = now
            dir_ = "data/test_data"
            create_dirs_if_not_exists([dir_])
            with open(os.path.join(dir_, "data_" + self.id + ".csv"), "w+") as f:
                f.write("%s\t%s\t%s\n" % ("data_id", "datetime", "data"))
                for data_id, value in self.recorded_data.items():
                    for datetime, data in value.items():
                        f.write("%s\t%s\t%s\n" % (data_id, datetime, data))
            print("\n\n\n\n\nSAAAAAVED!!!! youhouhplaboum\n")

        return to_serve

def run():
    # todo_
    from daemon_loops.modules.database import DataBase
    from daemon_loops.modules.logger import logger
    from daemon_loops.modules.participants_actions import actions
    from daemon_loops.modules.telegram import TelegramConnection
    from daemon_loops.modules.twitterstorm_utils import init
    import daemon_loops.modules.settings as s
    import daemon_loops.modules.telegram_settings as ts
    from daemon_loops.modules.message_analyser import MessageAnalyser

    init()
    db = DataBase()
    recorder = Recorder()
    tg_client = TelegramClientTester(s.SESSION_LISTENING_LOOP, ts.API_ID, ts.API_HASH, recorder, "record")

    with TelegramConnection(db, tg_client) as conn:
        analyser = MessageAnalyser(conn, actions)
        conn.tg_client.loop.run_until_complete(main_listening_loop(conn, analyser))


