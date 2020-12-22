import datetime as dt
import json
import os
import pickle
import re
import sqlite3
from shutil import copyfile
import daemon_loops.modules.logging as logging

from settings import settings as s


class DataBase:
    def __init__(self, dir=s.DATA_DIR):
        # if not os.path.exists(dir):
        #    os.makedirs(dir)
        self.db_file = os.path.join(dir, 'tweet_database.db')
        self.last_dump = dt.datetime.now(s.TIMEZONE)
        try:
            open(self.db_file, 'r')
            exists = True
        except FileNotFoundError:
            open(self.db_file, 'w+')
            exists = False
        if not exists:
            self.create_schema()
        self._get_and_set_conf()

    def _execute(self, queries, except_func=None):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        res = None
        for q, args in queries:
            try:
                res = c.execute(q, args)
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    self.create_schema()
                    res = c.execute(q, args)
                else:
                    if except_func is not None:
                        except_func(e)
                    else:
                        logging.error(e)
            except Exception as e:
                if except_func is not None:
                    except_func(e)
                else:
                    logging.error(e)
        if res is None:
            result = None
        else:
            result = [e for e in res]
        conn.commit()
        conn.close()
        return result

    def _select(self, query, args):
        for row in self._execute([(query, args)]):
            yield row  # yield innutile

    def create_schema(self):
        queries = self._get_and_set_conf()
        self._execute(queries)

    def _get_and_set_conf(self):
        self.PARTICIPANT_FIELDS = ["campain", "normalised_id",
                                   "display_name", "is_ok",
                                   "version", "date_fetched",
                                   "last_checked_msg_id", "last_consent_modified",
                                   "specific_data", "last_arrival_in_channel", "suggestions_frequency",
                                   "last_suggestion_url_or_text", "last_text_suggestion_id", "last_welcome_msg_received"]
        self.POSTEDTWEET_FIELDS = ["campain", "url", "date_received", "received_from", "validated"]
        self.SENDINGTASKS_FIELDS = ["campain", "version", "id_task", "time_to_send_min", "time_to_send_max", "type",
                                    "to_retweet", "fixed_msg", "percent_active_participants", "min_active_participants",
                                    "message_suggestion"]
        self.SENTTASKS_FIELDS = ["campain", "id_task", "version_sent", "sent", "sent_at", "sent_to"]
        self.MTB_FIELDS = ["campain", "id", "participant_id", "msg", "received_at", "processed_at", "detected",
                           "action_token"]
        self.SENT_MESS_FIELDS = ["campain", "participant_id", "msg", "sent_at"]
        queries = [
            ('''                                   
            CREATE TABLE participant (         
                campain text not null,         
                normalised_id text not null,         
                display_name text,                
                is_ok integer,                 
                version date,                  
                date_fetched date,             
                last_checked_msg_id text,      
                last_consent_modified date,
                specific_data text,
                last_arrival_in_channel date,
                suggestions_frequency float, 
                last_suggestion_url_or_text date,  
                last_text_suggestion_id text,
                last_welcome_msg_received date
            )                                  
        ''', []),
            ('''
                CREATE TABLE posted_tweet (
                    campain text not null,
                    url text,
                    date_received date,
                    received_from integer,
                    validated integer
                )
            ''', []),
            ('''
                CREATE TABLE sending_task (
                    campain text not null,
                    version date,
                    id_task text,
                    time_to_send_min date,
                    time_to_send_max date,
                    type text,
                    to_retweet text,
                    fixed_msg text,
                    percent_active_participants integer,
                    min_active_participants integer,
                    message_suggestion text
                )
            ''', []),
            ('''
                CREATE TABLE sent_tasks (
                    campain text not null,
                    id_task text,
                    version_sent date,
                    sent integer,
                    sent_at date,
                    sent_to text
                )
            ''', []),
            ('''
                CREATE TABLE message_to_bot (
                    campain text not null,
                    id text,
                    participant_id integer,
                    msg text,
                    received_at date,
                    processed_at date,
                    detected text,
                    action_token text
                )
            ''', []),
            ('''
                CREATE TABLE sent_message_by_bot (
                    campain text not null,
                    participant_id integer,
                    msg text,
                    sent_at date
                )
            ''', []),
        ]
        return queries

    def get_sent_messages_by_bot(self, lim=None):
        q = "select {} from sent_message_by_bot ".format(",".join(self.SENT_MESS_FIELDS))
        result = []
        if lim:
            q += " order by sent_at desc limit " + str(lim)
        q += " where campain = '{}'".format(s.CAMPAIN_ID)
        for row in self._select(q, []):
            result += [{field: row[i] for i, field in enumerate(self.SENT_MESS_FIELDS)}]
        return result

    def record_sent_message(self, msgs):
        args = []
        for m in msgs:
            args += [[m[field] for field in self.SENT_MESS_FIELDS]]
        self._insert(args, "sent_message_by_bot", self.SENT_MESS_FIELDS)

    def get_sending_tasks(self, all_tasks=False):
        result = []
        q = "select {} from sending_task where ".format(",".join(self.SENDINGTASKS_FIELDS))
        if not all_tasks:
            q += " version = (select max(version) from sending_task where campain = '{}') and".format(s.CAMPAIN_ID)
        q += " campain = '{}'".format(s.CAMPAIN_ID)
        for row in self._select(q, []):
            result += [{field: (row[i] if field != 'message_suggestion' else pickle.loads(row[i])) for i, field in
                        enumerate(self.SENDINGTASKS_FIELDS)}]
        return result

    def insert_sending_task(self, sg_tasks):
        now = dt.datetime.now(s.TIMEZONE)
        args = []
        for t in sg_tasks:
            args += [[s.CAMPAIN_ID, now] + [t[field] for field in
                                            ['id_task', 'time_to_send_min', 'time_to_send_max', 'type', 'to_retweet',
                                               'fixed_msg', 'percent_active_participants',
                                               'min_active_participants']] + [
                         pickle.dumps(t['message_suggestion'])]]
        self._insert(args, "sending_task", self.SENDINGTASKS_FIELDS)

    def get_tweets(self, validated=True):
        result = []
        q = "select {} from posted_tweet where".format(",".join(self.POSTEDTWEET_FIELDS))
        if validated:
            q += " validated != 0 and "
        q += " campain = '{}'".format(s.CAMPAIN_ID)
        for row in self._select(q, []):
            result += [{field: row[i] for i, field in enumerate(self.POSTEDTWEET_FIELDS)}]
        return result

    def validate_tweet(self, url, validate=True):
        q = ('UPDATE posted_tweet SET validated = ? WHERE url = ? and campain = ?', (validate, url, s.CAMPAIN_ID))
        self._execute([q])

    def insert_posted_tweet(self, tweets, trusted=s.DEFAULT_TWEET_VALIDATION):
        args = []
        for t in tweets:
            args += [[t[field] if field != 'validated' else trusted for field in self.POSTEDTWEET_FIELDS]]
        self._insert(args, "posted_tweet", self.POSTEDTWEET_FIELDS)

    def insert_sent_task(self, s_tasks):
        args = []
        for s in s_tasks:
            args += [[s[field] if field != 'sent_to' else str(s[field]) for field in self.SENTTASKS_FIELDS]]
        self._insert(args, "sent_tasks", self.SENTTASKS_FIELDS)

    def insert_messages_to_bot(self, msgs):
        args = []
        for m in msgs:
            mtb_id = str(m['participant_id']) + "_" + str(m['received_at'])
            args += [[m['campain'], mtb_id, m['participant_id'], m['msg'], m['received_at'],
                      m['processed_at'], m['detected'], m['action_token']]]
        self._insert(args, "message_to_bot", self.MTB_FIELDS)

    def _insert(self, args, table_name, fields):
        queries = []
        for a in args:
            q = (
                'INSERT INTO {}({}) VALUES ({})'.format(table_name, ",".join(fields), ",".join(["?"] * len(fields))), a)
            queries += [q]
        self._execute(queries)

    def insert_participants(self, participants, now):

        participant_ids = [p.get_normalised_id() for p in participants]
        returning_users_ids = self.get_ids_of_former_participants(ids = participant_ids)


        queries = []
        returning_users = []

        # all_participants = self.get_participants(participant_class)
        # consentments = {participant_id: is_ok for participant_id, is_ok in [(u.get_id(), u.is_ok) for u in
        # all_participants]}
        # last_check_m = {participant_id: lcm for participant_id, lcm in [(u.get_id(), u.get_last_checked_message_id(
        # )) for u in all_participants]}
        for p in participants:
            pid = p.get_normalised_id()
            if pid not in returning_users_ids:
                args = s.CAMPAIN_ID, p.get_normalised_id(), \
                       p.display_name, p.is_ok, \
                       now, p.date_fetched, \
                       p.get_last_checked_message_id(), now, \
                       json.dumps(p.get_specific_data()), \
                       p.last_arrival_in_channel, \
                       p.suggestions_frequency, p.last_suggestion_url_or_text, \
                       p.last_text_suggestion_id, p.last_welcome_msg_received

                q = ('INSERT INTO participant({}) VALUES ({})'.format(",".join(self.PARTICIPANT_FIELDS),
                                                                      ",".join(["?"] * len(self.PARTICIPANT_FIELDS))), args)
                queries += [q]
            else:
                returning_users.append(p)
        self._execute(queries)
        self.update_last_arrival_in_channel(returning_users, now)

        if dt.datetime.now(s.TIMEZONE) - self.last_dump > dt.timedelta(0, 1*60):
            self.last_dump = dt.datetime.now(s.TIMEZONE)
            self._dump()

    def get_participants(self, participant_class, consent=None):  # , only_ids_all_versions=False, orig_id=False):
        result = []
        q = "select {} from participant where ".format(",".join(self.PARTICIPANT_FIELDS))
        q += "version = (select max(version) from participant where campain = '{}') and".format(s.CAMPAIN_ID)
        if consent is not None:
            cnst = 1 if consent else 0
            q += " is_ok = {} and".format(cnst)
        q += " campain = '{}'".format(s.CAMPAIN_ID)
        for row in self._select(q, []):
            result += [participant_class.from_db(*row)]
        ids = list(set([r.get_normalised_id() for r in result]))  # dedoublonage (innutile si last versio)

        result = [[r for r in result if r.get_normalised_id() == id_][0] for id_ in ids]

        return result


    def get_participant_by_id(self, id, participant_class):
        # todo_es : quand un user revient dans la boucle, il faudrait lui actualiser certains champs comme son nom par exemple
        result = []
        q = "select {} from participant where ".format(",".join(self.PARTICIPANT_FIELDS))
        q += "version = (select max(version) from participant "
        q += "           where campain = '{}' and normalised_id = '{}') ".format(s.CAMPAIN_ID, id)
        q += "and campain = '{}' ".format(s.CAMPAIN_ID)
        q += "and normalised_id = '{}' ".format(id)
        for row in self._select(q, []):
            result += [participant_class.from_db(*row)]

        #print(928789, "\n\nRETURNING USER!!!!!!!!! ", result[0].display_name)

        if len(result) > 1:
            logging.critical("Plusieurs participants trouvés pour une même version")
        elif len(result) == 1:
            return result[0]
        else :
            return None

    # todo_es cette méthode est appelé 2 fois à peu près au même moment, et je mettrais ma main à couper que c'est redondant :p
    def get_ids_of_former_participants(self, ids=None):

        if ids is None or len(ids):

            q = "select distinct normalised_id from participant       " + \
                "where campain = '{}'                                 ".format(s.CAMPAIN_ID)
            if ids is not None:
                q += " and normalised_id in ('{}')                    ".format("','".join(ids))

            result = [row[0] for row in self._select(q, [])]

            return result
        else:
            return []

    def update_last_arrival_in_channel(self, participants, now):

        queries = []
        for p in participants:
            q = (
            'UPDATE participant SET version = ? , last_arrival_in_channel = ? WHERE normalised_id = ? and campain = ?',
            #  +" version = (select max(version) from participant where campain = ?)",
            (str(now), now, p.get_normalised_id(), s.CAMPAIN_ID))
            queries += [q]
        self._execute(queries)

    def update_participant_frequency(self, participant, minutes):
        q = (
            'UPDATE participant SET suggestions_frequency = ?  WHERE normalised_id = ? and campain = ?',
            (minutes, participant.get_normalised_id(), s.CAMPAIN_ID))
        self._execute([q])

    def update_version_of_participants(self, participants, now):
        queries = []
        for p in participants:
            q = ('UPDATE participant SET version = ? WHERE normalised_id = ? and campain = ?',
                 #  +" version = (select max(version) from participant where campain = ?)",
                 (now, p.get_normalised_id(), s.CAMPAIN_ID))
            queries += [q]
        self._execute(queries)

    def update_participant_consent(self, p, is_ok):
        p.is_ok = is_ok  # todo_chk : ouais c'est un peu chelou de modifier p dans la classe DATABASE...
        # todo_chk : je pense qqu'on a pas besoin de last_consent_modified
        now = dt.datetime.now(s.TIMEZONE)
        q = ('UPDATE participant SET is_ok = ?, last_consent_modified = ?  WHERE normalised_id = ? and campain = ?',
             (is_ok, now, p.get_normalised_id(), s.CAMPAIN_ID))
        self._execute([q])
        return p

    def update_last_suggestion(self, participant, datetime):
        q = ('UPDATE participant SET last_suggestion_url_or_text = ?  WHERE normalised_id = ? and campain = ?',
             (datetime,
              participant.get_normalised_id(), s.CAMPAIN_ID))
        self._execute([q])

    def update_last_suggested_text(self, participant, text_id):
        q = ('UPDATE participant SET last_text_suggestion_id = ?  WHERE normalised_id = ? and campain = ?',
             (text_id,
              participant.get_normalised_id(), s.CAMPAIN_ID))
        self._execute([q])

    def update_last_checked_msg(self, participant):
        q = ('UPDATE participant SET last_checked_msg_id = ?  WHERE normalised_id = ? and campain = ?',
             (participant.get_last_checked_message_id(),
              participant.get_normalised_id(), s.CAMPAIN_ID))
        self._execute([q])

    def update_last_welcome_msg_received(self, participant):
        q = ('UPDATE participant SET last_welcome_msg_received = ?  WHERE normalised_id = ? and campain = ?',
             (participant.last_welcome_msg_received,
              participant.get_normalised_id(), s.CAMPAIN_ID))
        self._execute([q])

    def _dump(self):
        copyfile(self.db_file,
                 re.sub('.db$', '', self.db_file) + str(dt.datetime.now(s.TIMEZONE)) + '.db')  # todo_chk
