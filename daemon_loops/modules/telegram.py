import datetime as dt
import json
import re
import sqlite3
import struct
import sys
import dateutil.parser

#from daemon_loops.modules.twitterstorm_utils import init
#from daemon_loops.modules.database import DataBase
#from daemon_loops.modules.participants_actions import actions

from telethon.errors.rpcerrorlist import PhoneCodeInvalidError, AuthKeyUnregisteredError, FloodWaitError, \
    PeerIdInvalidError
from telethon.sync import TelegramClient

import settings as s
import telegram_settings as ts
from daemon_loops.modules.connection import AbstractMessageId, AbstractParticipant, AbstractConnection, \
    AbstractChannel, \
    AbstractParticipantId, AbstractMessage
import daemon_loops.modules.logging as logging
from daemon_loops.modules.twitterstorm_utils import TwitterstormError
from daemon_loops.modules.message_analyser import MessageAnalyser

logging.info(s.INIT_MSG_TO_LOG)

class TelegramChannelId:
    def __init__(self, tg_id):
        if not isinstance(tg_id, int):
            logging.test(20000)
            logging.critical("Un id Télégram est toujours un nombre entier")
        else:  ###
            logging.test(20001)
        self.tg_specific_data = {'tg_id': tg_id}

    def get_normalised_id(self) -> str:
        logging.test(20002)
        return str(s.CAMPAIN_ID) + '_chan_' + str(self.tg_specific_data['tg_id'])

    def get_tg_id(self):
        logging.test(20003)
        return self.tg_specific_data['tg_id']


class TelegramParticipantId(AbstractParticipantId):
    def __init__(self, tg_id):
        if not isinstance(tg_id, int):
            logging.test(20004)
            logging.critical("Un id Télégram est toujours un nombre entier")
        else:  ###
            logging.test(20005)
        self.tg_specific_data = {'tg_id': tg_id}

    def get_normalised_id(self) -> str:
        logging.test(20006)
        return str(s.CAMPAIN_ID) + '_ptcp_' + str(self.tg_specific_data['tg_id'])

    def get_tg_id(self) -> int:
        logging.test(20007)
        return self.tg_specific_data['tg_id']


class TelegramMessageId(AbstractMessageId):
    type_str = '_msg_'

    def __init__(self, tg_id):
        logging.test(20008)
        if not isinstance(tg_id, int):
            logging.test(20009)
            logging.critical("Un id Télégram est toujours un nombre entier")
        else:  ###
            logging.test(20010)
        self.tg_specific_data = {'tg_id': tg_id}

    def get_normalised_id(self) -> str:
        logging.test(20011)
        return str(s.CAMPAIN_ID) + self.type_str + str(self.tg_specific_data['tg_id'])

    def get_tg_id(self) -> int:
        logging.test(20012)
        return self.tg_specific_data['tg_id']

    @staticmethod
    def from_normalised_id_to_tg_id(norm_id):
        logging.test(20013)
        regexp = '%s(\d+)\Z' % re.escape(TelegramMessageId.type_str)
        try:
            logging.test(20014)
            tg_id = re.findall(regexp, norm_id)[0]
        except IndexError:
            logging.test(20015)
            logging.critical("L'argument norm_id est mal formé, il ne correspond pas à la regexp '%s'" % regexp)
        try:
            logging.test(20016)
            tg_id = int(tg_id)
        except ValueError:
            logging.test(20017)
            logging.critical("L'argument norm_id est mal formé, l'id doit être un entier")
        return tg_id


class TelegramChannel(AbstractChannel):
    def __init__(self, tg_channel):
        logging.test(20018)
        self.tg_specific_data = {'tg_channel': tg_channel}

    def get_specific_data(self) -> dict:
        logging.test(20019)
        return self.tg_specific_data

    def get_tg_channel(self):
        logging.test(20020)
        return self.tg_specific_data['tg_channel']


class TelegramMessage(AbstractMessage):
    def __init__(self, tg_message):
        logging.test(20021)
        sender_id = TelegramParticipantId(tg_message.sender_id)
        msg_id = TelegramMessageId(tg_message.id)
        AbstractMessage.__init__(self, msg_id, tg_message.message, tg_message.date, sender_id)

    def _check_id_type(self, id_) -> None:
        if not isinstance(id_, TelegramMessageId):
            logging.test(20022)
            logging.critical(
                "L'argument 'sender_id' doit être de type TelegramMessageId")
        else:  ###
            logging.test(20023)

    def _check_sender_id_type(self, sender_id) -> None:
        if not isinstance(sender_id, TelegramParticipantId):
            logging.test(20024)
            logging.critical(
                "L'argument 'sender_id' doit être de type TelegramParticipantId")
        else:  ###
            logging.test(20025)


class TelegramParticipant(AbstractParticipant):

    def __init__(self,
                 campain,
                 tg_id,
                 tg_first_name,
                 tg_last_name,
                 tg_username,
                 is_ok,
                 version,
                 date_fetched,
                 tg_last_checked_msg_id,
                 last_consent_modified,
                 last_arrival_in_channel,
                 suggestions_frequency,
                 last_suggestion_url_or_text,
                 last_text_suggestion_id
                 ):
        logging.test(20026)
        id_ = TelegramParticipantId(tg_id)
        if tg_last_checked_msg_id is not None:
            logging.test(20027)
            last_checked_msg_id = TelegramMessageId(tg_last_checked_msg_id)
        else:
            logging.test(20028)
            last_checked_msg_id = None

        first_name = tg_first_name if tg_first_name is not None else ""
        last_name = tg_last_name if tg_last_name is not None else ""
        username = "@" + tg_username + "" if tg_username is not None else ""
        display_name = "%s %s %s" % (first_name, last_name, username)

        AbstractParticipant.__init__(self,
                                     campain,
                                     id_,
                                     display_name,
                                     is_ok,
                                     version,
                                     date_fetched,
                                     last_checked_msg_id,
                                     last_consent_modified,
                                     last_arrival_in_channel,
                                     suggestions_frequency,
                                     last_suggestion_url_or_text,
                                     last_text_suggestion_id
                                     )

        self.tg_specific_data = {
            'tg_id': tg_id,
            # 'tg_last_checked_msg_id': tg_last_checked_msg_id,
            'tg_first_name': tg_first_name,
            'tg_last_name': tg_last_name,
            'tg_username': tg_username
        }

    @classmethod
    def from_pair(cls, self, p):
        self.__dict__ = p.__dict__.copy()

    def _check_id_type(self, id_) -> None:
        if not isinstance(id_, TelegramParticipantId):
            logging.test(20029)
            logging.critical("L'argument 'id' doit être de type TelegramParticipantId")
        else:  ###
            logging.test(20030)

    def _check_message_id_type(self, last_checked_message_id) -> None:
        if not isinstance(last_checked_message_id, TelegramMessageId):
            logging.test(20031)
            logging.critical("L'argument 'last_checked_message_id' doit être de type TelegramMessageId")
        else:  ###
            logging.test(20032)

    def _set_last_checked_msg(self, last_checked_message_id):
        logging.test(20033)
        self.last_checked_msg_id = last_checked_message_id

    def get_last_checked_msg_tg_id(self):
        logging.test(20034)
        return TelegramMessageId.from_normalised_id_to_tg_id(
            self.last_checked_msg_id.get_normalised_id()) if self.last_checked_msg_id is not None else None
        # todo_chk : j'ai l'impression que c'est dégeu mais j'en suis pas sur

    def is_scribe(self):
        logging.test(20035)
        return self.get_tg_id() in (ts.SCRIBES_ANIMATORS + ts.SCRIBES_ROBOTS)

    def get_specific_data(self) -> dict:
        logging.test(20036)
        return self.tg_specific_data

    def is_trusted_participant_for_tweets(self) -> bool:
        # todo_chk : voir si on veut garder cette feature
        logging.test(20037)
        return True

    def get_tg_id(self) -> int:
        logging.test(20038)
        return self.tg_specific_data['tg_id']

    @staticmethod
    def create_from_db(campain,
                       normalised_id,
                       display_name,
                       is_ok,
                       version,
                       date_fetched,
                       last_checked_msg_id,
                       last_consent_modified,
                       specific_data,
                       last_arrival_in_channel,
                       suggestions_frequency,
                       last_suggestion_url_or_text,
                       last_text_suggestion_id
                       ) -> AbstractParticipant:

        tg_specific_data = json.loads(specific_data)
        try:
            logging.test(20039)
            tg_id = tg_specific_data['tg_id']
            tg_first_name = tg_specific_data['tg_first_name']
            tg_last_name = tg_specific_data['tg_last_name']
            tg_username = tg_specific_data['tg_username']
            # tg_last_checked_msg_id = tg_specific_data['tg_last_checked_msg_id']
        except KeyError:
            logging.test(20040)
            logging.critical("Vous utilisez probablement une ancienne version du schéma de la BDD")

        tg_last_checked_msg_id = TelegramMessageId.from_normalised_id_to_tg_id(
            last_checked_msg_id) if last_checked_msg_id is not None else None

        date_fetched = dateutil.parser.isoparse(date_fetched)
        last_consent_modified = dateutil.parser.isoparse(last_consent_modified)
        last_arrival_in_channel = dateutil.parser.isoparse(last_arrival_in_channel)
        if last_suggestion_url_or_text is not None:
            last_suggestion_url_or_text = dateutil.parser.isoparse(last_suggestion_url_or_text)

        return TelegramParticipant(
            campain,
            tg_id,
            tg_first_name,
            tg_last_name,
            tg_username,
            is_ok,
            version,
            date_fetched,
            tg_last_checked_msg_id,
            last_consent_modified,
            last_arrival_in_channel,
            suggestions_frequency,
            last_suggestion_url_or_text,
            last_text_suggestion_id
        )

class TelegramClientWrapper:
        def __init__(self, session, api_id, api_hash):
            self.client = TelegramClient(session, api_id, api_hash)

        def connect(self):
            try:
                res = self.client.connect()
            except Exception as e:
                res = None  # todo_cr : faut bien gérer l'exception ici
                logging.exception(e)
            return res

        def disconnect(self):
            try:
                res = self.client.disconnect()
            except Exception as e:
                logging.exception(e)
            return res

        def get_messages(self, tg_channel, nb_msgs, **kwargs):
            if tg_channel is None:
                logging.error("On essaie d'obtenir les messages d'un channel qui n'a pas été trouvé")
                return []

            try:
                res = self.client.get_messages(tg_channel, nb_msgs, **kwargs)
            except Exception as e:
                logging.exception(e)
                return []
            return res

        def get_input_entity(self, *args, **kwargs):
            return self.client.get_input_entity(*args, **kwargs)

        def get_entity(self, *args, **kwargs):
            return self.client.get_entity(*args, **kwargs)

        def is_user_authorized(self):
            print(555555555555)
            return self.client.is_user_authorized()

        def sign_in(self, *args, **kwargs):
            return self.client.sign_in(*args, **kwargs)

        def send_code_request(self, *args, **kwargs):
            return self.client.send_code_request(*args, **kwargs)

        def get_dialogs(self, *args, **kwargs):
            return self.client.get_dialogs(*args, **kwargs)

        def iter_participants(self, tg_channel, **kwargs):
            if tg_channel is None:
                logging.error("On essaie d'obtenir les participant.e.s d'un channel qui n'a pas été trouvé")
                return iter([])

            try:
                res = self.client.iter_participants(tg_channel, **kwargs)
            except Exception as e:
                logging.exception(e)
                return iter([])

            return res

        def send_message(self, tg_channel, message, **kwargs):
            if tg_channel is None:
                logging.error("On essaie d'envoyer un message vers un channel qui n'a pas été trouvé\nMessage=\n"+str(message))
                return None

            try:
                res = self.client.send_message(tg_channel, message, **kwargs)
            except Exception as e:
                logging.exception(e)
                return None

            return res

        @property
        def loop(self):
            return self.client.loop


class TelegramConnection(AbstractConnection):
    def __init__(self, db, telegram_client=None):
        logging.test(20041)
        AbstractConnection.__init__(self, db)
        if telegram_client is not None:
            self.tg_client = telegram_client
        else:
            self.tg_client = TelegramClientWrapper(s.SESSION_LISTENING_LOOP, ts.API_ID, ts.API_HASH)
        print('\n\n\n%s\n' % type(self.tg_client))

    async def init_conf(self):

        await AbstractConnection.init_conf(self)

        # todo_chk mettre plutot ça a l'initialisation de la classe DataBAse, quand il y en aura une
        id_cls = TelegramParticipantId
        for id in ts.ADMINS:
            norm_id = id_cls(id).get_normalised_id()
            await s.addParticipantToConf(s.CAMPAIN_ID, norm_id, 'ADMIN')
        for id in ts.REACHABLE_USERS:
            norm_id = id_cls(id).get_normalised_id()
            await s.addParticipantToConf(s.CAMPAIN_ID, norm_id, 'REACHABLE')
        for id in ts.SCRIBES_ROBOTS:
            norm_id = id_cls(id).get_normalised_id()
            await s.addParticipantToConf(s.CAMPAIN_ID, norm_id, 'SCRIBE_ROBOT')
        for p in ts.SCRIBES_ANIMATORS:
            id = p['tg_id']
            name = p['display_name']
            norm_id = id_cls(id).get_normalised_id()
            await s.addParticipantToConf(s.CAMPAIN_ID, norm_id, 'SCRIBE_ANIMATOR', display_name_for_animators=name)
        await s.set_conf_var(s.CAMPAIN_ID, 'RESTRICT_REACHABLE_USERS', ts.RESTRICT_REACHABLE_USERS)


    def _is_reachable(self, participant):
        """
        Overrides method in AbstractConnection
        """
        logging.test(20042)
        return self._is_id_reachable(participant.get_normalised_id())

    def connect(self):
        """
        Overrides method in AbstractConnection
        """
        logging.test(20043)
        try:
            self.tg_client.connect()
        except sqlite3.OperationalError as e:
            logging.test(20100)
            self._manage_sqlite3_errors(e)

        self.tg_client.loop.run_until_complete(self._user_authentification())
        return self

    def disconnect(self, exc_type, exc_value, traceback):
        """
        Overrides method in AbstractConnection
        """
        if exc_type is not None:
            logging.test(20046)
            if isinstance(exc_type, ConnectionError):
                logging.test(20047)
                logging.critical(("La connection à Télégram a expirée. Reconnectez-vous.\n" +
                                         "Le cas échéant, supprimez le fichier {}").format(s.SESSION_LISTENING_LOOP))
            else:  ###
                logging.test(20044)
        else:  ###
            logging.test(20045)
        self.tg_client.disconnect()

    async def _get_1to1_channel(self, participant) -> TelegramChannel:
        """
        Overrides method in AbstractConnection.

        Renvoie pour un.e participant.e donné.e le channel de conversation privée pour communiquer avec lui/elle
        """

        # todo_es : dépalacer toute la gestion d'erreur dans TelegramClientWrapper?
        try:
            logging.test(20048)
            channel = await self.tg_client.get_input_entity(participant.get_tg_id())
        except ValueError:
            if participant.tg_specific_data['tg_username'] is None:
                logging.test(20049)
                return TelegramChannel(None)
            else: ###
                logging.test(20050)
            try:
                logging.test(20051)
                channel = await self.tg_client.get_input_entity("@" + participant.tg_username)
            except ValueError:
                logging.test(20052)
                logging.error("Channel du participant {}({}) non trouvé".format(participant.get_tg_id(), participant.display_name))
                return TelegramChannel(
                    None)  # todo_chk: gérer le cas où channel = None dans les fonctions appelant _get_1to1_channel
        except Exception:
            logging.error(
                "Channel du participant {}({}) non trouvé".format(participant.get_tg_id(), participant.display_name))
            return TelegramChannel(None)
        return TelegramChannel(channel)

    def is_bot(self, participant):
        """
        Overrides method in AbstractConnection.
        Vérifie si le/la participant.e est le robot
        """
        logging.test(20053)
        return participant.get_normalised_id() == TelegramParticipantId(ts.BOT).get_normalised_id()

    def is_admin(self, participant):
        """
        Overrides method in AbstractConnection.
        Vérifie si le/la participant.e est le robot
        """
        logging.test(20101)
        admins = [TelegramParticipantId(a).get_normalised_id() for a in ts.ADMINS]
        return participant.get_normalised_id() in admins


    def _is_me(self, participant):
        """
        Overrides method in AbstractConnection.
        Vérifie si le/la participant.e est le compte ME (compte de test)
        """
        logging.test(20054)
        return participant.get_normalised_id() == TelegramParticipantId(ts.ME).get_normalised_id()

    async def _get_main_channel(self) -> TelegramChannel:
        """
        Overrides method in AbstractConnection.
        Retourne le channel principal sur lequel tous.tes les participant.e.s sont présent.e.s

        """
        logging.test(20055)
        return await self._get_tgchannel_from_id(TelegramChannelId(ts.MAIN_CHANNEL_ID))

    def _get_participant_class(self):
        logging.test(20056)
        return TelegramParticipant  # todo_es : en fait non. créer une méthode dans TelegramConnectin appelée
        #  create_participant, puis dans database.py>get_users, remplacer participant_class par conn.create_participant

    async def _get_messages(self, channel, participant):
        last_checked_message_tg_id = participant.get_last_checked_msg_tg_id()
        kwargs = {
            'min_id': last_checked_message_tg_id} \
            if last_checked_message_tg_id is not None else {}

        messages = await self.tg_client.get_messages(channel.get_tg_channel(), ts.NB_MSG_TO_FETCH, **kwargs)

        if len(messages):
            logging.test(20058)
            last_message_id = TelegramMessageId(max([m.id for m in messages]))
        elif last_checked_message_tg_id is not None:
            logging.test(20059)
            last_message_id = TelegramMessageId(last_checked_message_tg_id)
        else:
            logging.test(20060)
            last_message_id = None

        participant.set_last_checked_msg(last_message_id)
        return [TelegramMessage(m) for m in messages], participant

    @staticmethod
    def _filter_messages_from_participant_to_bot(messages, participant):
        logging.test(20061)
        return [m for m in messages
                if m.get_normalised_sender_id() == participant.get_normalised_id()]

    async def _get_tgchannel_from_id(self, tg_channel_id):
        """
        Retourne un channel Télégramme à partir de son identifiant
        @return: TelegramChannel
        """

        unknown_channel_msg = 'L\'identifiant du channel demandé ({}) est inconnu'.format(tg_channel_id.get_tg_id())
        try:
            logging.test(20063)
            channel = await self.tg_client.get_entity(tg_channel_id.get_tg_id())

        except struct.error as e:
            logging.error(unknown_channel_msg)
            logging.test(20064)
            return TelegramChannel(None)

        except PeerIdInvalidError as e:
            logging.test(20065)
            logging.error(
                unknown_channel_msg + '\nIl est possible que le compte Télégram qu\'utilise le bot' +
                ' ne soit pas parmi les membres du channel principal. Il n\'est donc pas ' +
                'autorisé à accéder à ses informations. Merci de l\'y ajouter.')
            return TelegramChannel(None)

        except AuthKeyUnregisteredError as e:
            logging.exception(e)
            logging.test(20066)
            return TelegramChannel(None)

        except Exception as e:
            print(3333333333333333333333333333333333333333)
            logging.exception(e)
            return TelegramChannel(None)

        logging.test(20067)

        return TelegramChannel(channel)

    async def _get_new_participants_from_main_channel(self, first_time=False, known_participants=[]):
        """
        Overrides method in AbstractConnection.

        Retourne tous.tes les participant.e.s d'un channel à partir du nom de ce dernier,
        ainsi que le compte ME (compte de test) s'il fait partie de ce channel (necessaire
        si SEND_ONLY_TO_ME = True)
        @param known_participants:
        """
        channel = await self._get_main_channel()
        logging.test(20068)
        return await self._get_new_participants_from_channel(channel, first_time=first_time,
                                                             known_participants=known_participants)

    async def _user_authentification(self):
        # Si l'utilisateur n'est pas authentifié, ...
        print(297376872,type(self.tg_client))
        if not await self.tg_client.is_user_authorized():

            # ... on lui envoie le code de validation sur son Télégram.
            try:
                logging.test(20069)
                await self.tg_client.send_code_request(ts.BOT_PHONE_NUMBER)
            except FloodWaitError as e:
                logging.test(20070)
                # Cas où le code a été saisi trop de fois de manière erronée
                self._manage_flood_wait_error(e)

            # L'utilisateur doit ensuite saisir son code ici :
            code_is_valide = False
            while not code_is_valide:
                logging.test(20071)
                code = input(s.STR_TG_ENTER_CODE.format(ts.BOT_PHONE_NUMBER))
                try:
                    logging.test(20072)
                    await self.tg_client.sign_in(ts.BOT_PHONE_NUMBER, code)
                except PhoneCodeInvalidError:
                    logging.test(20073)
                    # Si le code est incorrect
                    code_is_valide = False
                    logging.info(s.STR_TG_INVALID_CODE.format(ts.BOT_PHONE_NUMBER))
                except FloodWaitError as e:
                    logging.test(20074)
                    # Cas où le code a été saisi trop de fois de manière erronée
                    self._manage_flood_wait_error(e)
                else:
                    logging.test(20075)
                    # Si le code est bon
                    code_is_valide = True
                    logging.info(s.STR_TG_AUTH_OK)
        else:  ###
            logging.test(20076)

    @staticmethod
    def _find_waiting_time(exception):
        """
        Retourne le temps restant avant de pouvoir retenter une connection à Télégram.
        """
        try:
            logging.test(20077)
            waiting_time = re.findall("wait of (.*?) seconds", str(exception))[0]
        except IndexError:
            logging.test(20078)
            waiting_time = " ? "
        return waiting_time

    @staticmethod
    def _manage_flood_wait_error(exception):
        """
        Méthode appéles dans le cas où le code a été saisi trop de fois de manière erronée :
        Télégram exige alors un temps d'attente avant de pouvoir retenter sa chance.
        """
        logging.test(20079)
        #waiting_time = TelegramConnetion._find_waiting_time(exception)
        logging.error(s.STR_TG_TOO_MANY_INVALID.format(exception.seconds, ts.__name__))
        sys.exit()

    def _manage_sqlite3_errors(self, e):
        if isinstance(e, sqlite3.OperationalError) and "database is locked" in str(e):
            logging.critical(("La connection à Télégram est déjà utilisée. Essayez de supprimer le fichier {}.session\n" +
                                    "Voici l'erreur d'origine :\n{}").format(
                                        s.SESSION_LISTENING_LOOP, e))
        else:
            logging.critical(("Erreur inconnue. Essayez de supprimer le fichier {}.session\n" +
                                    "Voici l'erreur d'origine :\n{}").format(
                                        s.SESSION_LISTENING_LOOP, e))


    async def _get_all_channels(self):
        """
        Retourne tous les channels auxquels participe le compte du BOT
        """
        try:
            logging.test(20080)
            channels = await self.tg_client.get_dialogs()
        except sqlite3.OperationalError as e:
            logging.test(20081)
            self._manage_sqlite3_errors(e)

        return [{'title': ch.title, 'channel': TelegramChannel(ch)} for ch in channels]

    async def _get_new_participants_from_channel(self, channel,
                                                 first_time=False,
                                                 known_participants=[]):
        """
        Retourne tous.tes les participant.e.s d'un channel
        """

        now = dt.datetime.now(s.TIMEZONE)
        me = None

        # db_participants_id = self.db.get_all_participants_origids(TelegramParticipant)
        # todo_op : du coup la méthode db.get_all_participants_origids devient innutile
        #  bon pas ici mais faire en sorte que db.get_participants soit un itérable pour pas
        #  tout charger d'un coup

        if first_time:
            logging.test(20082)
            known_participants = self._get_db_participants()
        else:  ###
            logging.test(20083)

        known_participants_tg_ids = [p.get_tg_id() for p in known_participants]

        tg_participants_iterable = self.tg_client.iter_participants(channel.get_tg_channel(), aggressive=True)
        tg_all_channel_participants = [{'p_id': p.id,
                                'new_participant': p if p.id not in known_participants_tg_ids else None}
                               async for p in tg_participants_iterable]
        all_channel_participants_tg_ids = [p['p_id'] for p in tg_all_channel_participants]
        tg_new_participants = [p['new_participant'] for p in tg_all_channel_participants if p['new_participant'] is not None]

        # Participants qui ne sont pas sortis du channel
        participants_still_in_the_channel = [p for p in known_participants if p.get_tg_id() in all_channel_participants_tg_ids]
        participants_who_left = [p for p in known_participants if p.get_tg_id() not in all_channel_participants_tg_ids]

        new_participants = []


        for p in tg_new_participants:
            logging.test(20084)
            normalised_id = TelegramParticipantId(p.id).get_normalised_id()
            if self._is_id_reachable(normalised_id):
                logging.test(20085)
                new_participant = TelegramParticipant(
                    s.CAMPAIN_ID,
                    p.id,
                    p.first_name,
                    p.last_name,
                    p.username,
                    s.DEFAULT_CONSENT,
                    None,
                    now,
                    None,
                    None,
                    now,
                    max(s.DEFAULT_SUGGESTIONS_FREQUENCY, s.MIN_SUGGESTION_FREQUENCY),
                    None,
                    None,
                )
                new_participants.append(new_participant)
                # bonne nouvelle : ts.ME n'a plu besoin d'etre readable ;) !!!!!
                # if p.id == ts.ME:
                #    me = new_participant
            else:
                logging.test(20086)

        # todo_es : vérifier utilité d'un ME si pas selnd_only_to_me. Sinon, mettre if SEND_ONLY_TO_ME ici
        for p in new_participants + participants_still_in_the_channel + participants_who_left:
            if p.get_tg_id() == ts.ME:
                logging.test(20087)
                me = p
            else:  ###
                logging.test(20088)

        return new_participants, participants_still_in_the_channel, participants_who_left, me

    async def _send_message(self, channel, msg):
        """
        Envoie un message via Télégram sur le channel donné
        """
        logging.test(20089)
        await self.tg_client.send_message(channel.get_tg_channel(), msg)

    @staticmethod
    def _is_id_reachable(participant_id):
        """
        Indique s'il est possible d'interragir avec un participant donné (envoi de messages, etc.).
        """

        # todo_es ext_set = pas tres bo. variable d'environneemnt?
        reachable_participants = ts.REACHABLE_USERS + [ts.ME]
        # self._get_participants_new_from_channel
        reachable_participants = [TelegramParticipantId(id_).get_normalised_id() for id_ in reachable_participants]
        # reachable_participants = [int(e) if type(e) == str else e for e in reachable_participants]

        if not ts.RESTRICT_REACHABLE_USERS:
            logging.test(20090)
            return True
        else:
            logging.test(20091)
            if participant_id in reachable_participants:
                logging.test(20092)
                return True
            else:  ###
                logging.test(20093)
            return False

    async def search_channels(self, string=None):
        logging.test(20094)
        channels = await self._get_all_channels()
        filtered_channels = [ch for ch in channels if string is None or string.lower() in ch['title'].lower()]
        print("Liste des channels {}:".format("contenant '{}'".format(string) if string is not None else ""))

        for ch in filtered_channels:
            logging.test(20095)
            tg_channel = ch['channel'].get_tg_channel()
            if tg_channel is not None:
                cid = tg_channel.id
            else:
                cid = ""
            title = ch['title']
            print("- [id= {} ] : '{}'".format(cid, title))

    async def display_participants_of_main_channel(self, search=None):
        logging.test(20096)
        participants, _, _, _ = await self._get_new_participants_from_main_channel()

        main_channel = await self._get_main_channel()
        main_channel = main_channel.get_tg_channel()
        title = main_channel.title if main_channel is not None else "[Channel non trouvé]"
        msg = "\nListe des participants du channel '{}'".format(title)
        msg += " contenant '{}':".format(search) if search is not None else ":"
        if ts.RESTRICT_REACHABLE_USERS :
            msg += "\n\n! ATTENTION :\nDans le fichier de configuration, RESTRICT_REACHABLE_USERS " \
            "est à True, ce qui restreint les utilisateurs affichés ici.\n"
        print(msg)

        for p in participants:
            logging.test(20097)
            first_name = p.get_specific_data()['tg_first_name']
            last_name = p.get_specific_data()['tg_last_name']
            username = p.get_specific_data()['tg_username']

            first_name = first_name if first_name is not None else ""
            last_name = last_name if last_name is not None else ""
            username = "@" + username + " " if username is not None else "? "

            for_search = first_name + last_name + username
            if search is None or search.lower() in for_search.lower():
                logging.test(20098)
                pid = p.get_tg_id()
                total_len = len(str(pid) + first_name + last_name)
                space = " " * (30 - total_len)
                print("- [id= {} ]: {} {}{} [username = {}]".format(pid, first_name, last_name, space, username))
            else:
                logging.test(20099)

    def run_with_async_loop(self, call):
        return self.tg_client.loop.run_until_complete(call)

#def run():  # todo_es: enlever à terme
#    init()
#    db = DataBase()
#    conn = TelegramConnection(db).__enter__()
#    analyser = MessageAnalyser(conn, actions)
#    conn.run_with_async_loop(conn.search_channels("prod"))

#if __name__ == "__main__":  # todo_es: enlever à terme
#    run()