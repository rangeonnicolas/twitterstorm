import datetime as dt
import json
import re
import sqlite3
import struct
import sys

import dateutil.parser

from daemon_loops.modules.twitterstorm_utils import TwitterstormError
from daemon_loops.modules.database import DataBase

from telethon.errors.rpcerrorlist import PhoneCodeInvalidError, FloodWaitError, PeerIdInvalidError
from telethon.sync import TelegramClient

from settings import settings as s, telegram_settings as ts
from daemon_loops.modules.connection import AbstractMessageId, AbstractParticipant, AbstractConnection, \
    AbstractChannel, AbstractPersonnalChannel, AbstractParticipantId, AbstractMessage
import daemon_loops.modules.logging as logging

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
        regexp = r'%s(\d+)\Z' % re.escape(TelegramMessageId.type_str)
        tg_id = None
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
    def __init__(self, dict):
        self.__dict__ = dict

    @classmethod
    def from_telethon_object(cls, tg_channel):
        logging.test(20018)
        self = cls({})
        AbstractChannel.__init__(self, tg_channel.title, {'tg_channel': tg_channel})
        return self

    def get_tg_channel(self):
        logging.test(20020)
        return self.specific_data['tg_channel']

    def is_empty(self):
        return self.specific_data['tg_channel'] is None

class TelegramPersonnalChannel(AbstractPersonnalChannel):
    def __init__(self, dict):
        self.__dict__ = dict

    @classmethod
    def from_telethon_object(cls, tg_channel):
        self = cls({})
        AbstractPersonnalChannel.__init__(self, {'tg_channel': tg_channel})
        return self

    def get_tg_channel(self):
        return self.specific_data['tg_channel']

    def is_empty(self):
        return self.specific_data['tg_channel'] is None


class TelegramMessage(AbstractMessage):
    def __init__(self, dict):
        self.__dict__ = dict

    @classmethod
    def from_telethon_object(cls, tg_message):
        logging.test(20021)
        sender_id = TelegramParticipantId(tg_message.sender_id)
        msg_id = TelegramMessageId(tg_message.id)
        self = cls({})
        AbstractMessage.__init__(self, msg_id, tg_message.message, tg_message.date, sender_id)
        return self

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
    def __init__(self, dict):
        self.__dict__ = dict

    @classmethod
    def from_args(cls,
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
                 last_text_suggestion_id,
                 last_welcome_msg_received
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

        specific_data = {
            'tg_id': tg_id,
            'tg_first_name': tg_first_name,
            'tg_last_name': tg_last_name,
            'tg_username': tg_username
        }

        self = cls({})
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
                                     last_text_suggestion_id,
                                     last_welcome_msg_received,
                                     specific_data
                                     )

        return self

    @classmethod
    async def from_telethon_object(cls, tg_participant, now, suggestions_frequency, first_time):
        participant = cls.from_args(
            s.CAMPAIN_ID,
            tg_participant.id,
            tg_participant.first_name,
            tg_participant.last_name,
            tg_participant.username,
            s.DEFAULT_CONSENT_FORMER_MEMBERS if first_time else s.DEFAULT_CONSENT_NEWCOMERS,
            None,
            now,
            None,
            None,
            now,
            max(suggestions_frequency, s.MIN_SUGGESTION_FREQUENCY),
            None,
            None,
            None,
        )
        if await participant.has_special_role():
            participant.is_ok = True

        return participant

    @classmethod
    def from_pair(cls, p1, p2):
        p1.__dict__ = p2.__dict__.copy()

    @classmethod
    def from_db(cls, campain,
                normalised_id,  # todo_es innutile
                display_name,  # todo_es innutile
                is_ok,
                version,
                date_fetched,
                last_checked_msg_id,
                last_consent_modified,
                specific_data,
                last_arrival_in_channel,
                suggestions_frequency,
                last_suggestion_url_or_text,
                last_text_suggestion_id,
                last_welcome_msg_received
                ) -> AbstractParticipant:

        tg_specific_data = json.loads(specific_data)

        logging.test(20039)
        tg_id = tg_specific_data['tg_id']
        tg_first_name = tg_specific_data['tg_first_name']
        tg_last_name = tg_specific_data['tg_last_name']
        tg_username = tg_specific_data['tg_username']

        tg_last_checked_msg_id = TelegramMessageId.from_normalised_id_to_tg_id(
            last_checked_msg_id) if last_checked_msg_id is not None else None

        date_fetched = dateutil.parser.isoparse(date_fetched)
        last_consent_modified = dateutil.parser.isoparse(last_consent_modified)
        last_arrival_in_channel = dateutil.parser.isoparse(last_arrival_in_channel)
        if last_welcome_msg_received is not None:
            last_welcome_msg_received = dateutil.parser.isoparse(last_welcome_msg_received)
        if last_suggestion_url_or_text is not None:
            last_suggestion_url_or_text = dateutil.parser.isoparse(last_suggestion_url_or_text)

        return cls.from_args(
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
            last_text_suggestion_id,
            last_welcome_msg_received
        )

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

    async def is_scribe(self):
        logging.test(20035)
        scribes_info = await s.getAllScribesInConf(
            s.CAMPAIN_ID)
        # todo_op : prendre tous les scribes ? ne pas faire l'appel une fois avant
        #  de prendre en revue tous les participants?
        scribes_ids = scribes_info.keys()
        return self.get_normalised_id() in scribes_ids


    def is_bot(self):
        """
        Vérifie si le/la participant·e est le robot
        """
        logging.test(20053)
        return self.get_normalised_id() == TelegramParticipantId(ts.BOT).get_normalised_id()

    # todo_es a mettre ds a classe parente
    async def is_admin(self):
        admins = await s.get_all_admins_ids(s.CAMPAIN_ID)
        return self.get_normalised_id() in admins

    async def has_special_role(self) -> bool:
        return await self.is_admin() or await self.is_scribe()

    def is_trusted_participant_for_tweets(self) -> bool:
        # todo_chk : voir si on veut garder cette feature
        logging.test(20037)
        return True

    def get_tg_id(self) -> int:
        logging.test(20038)
        return self.specific_data['tg_id']


class TelegramClientWrapper:
    def __init__(self, session, api_id, api_hash):
        self.client = TelegramClient(session, api_id, api_hash)

    def connect(self):
        res = None
        try:
            res = self.client.connect()
        except sqlite3.OperationalError as e:
            try:
                self._manage_sqlite3_errors(e)
            except TwitterstormError as ee:
                logging.critical(ee)
        except Exception as e:
            logging.exception(e)
        return res

    def disconnect(self):
        res = None
        try:
            res = self.client.disconnect()
        except Exception as e:
            logging.critical(e)
        return res

    async def get_messages(self, tg_channel, nb_msgs, **kwargs):
        if tg_channel is None:
            logging.error("On essaie d'obtenir les messages d'un channel qui n'a pas été trouvé")
            return []

        try:
            res = await self.client.get_messages(tg_channel, nb_msgs, **kwargs)
        except Exception as e:
            logging.exception(e)
            return []

        res = [TelegramMessage.from_telethon_object(m) for m in res]
        return res

    async def get_input_entity(self, peer) -> TelegramPersonnalChannel:
        tg_channel = None
        try:
            tg_channel = await self.client.get_input_entity(peer)
        except Exception:
            logging.exception("Channel non trouvé pour l'argument 'peer' = " + str(peer))
            raise KeyboardInterrupt(
                "Si tu tombes là une fois, c'est qu'il est pertinent de laisser la suite du code dans "
                "self._get_1to1_channel. Sinon, non ;)")  # todo_cr à retirer à terme

        return TelegramPersonnalChannel.from_telethon_object(tg_channel)

    async def get_entity(self, entity) -> TelegramChannel:
        unknown_channel_msg = 'L\'identifiant du channel demandé ({}) est inconnu'.format(entity)

        try:
            tg_channel = await self.client.get_entity(entity)
        except struct.error:
            logging.exception(unknown_channel_msg)
            tg_channel = None
        except PeerIdInvalidError:
            logging.exception(unknown_channel_msg + '\nIl est possible que le compte Télégram qu\'utilise le bot' +
                              ' ne soit pas parmi les membres du channel principal. Il n\'est donc pas ' +
                              'autorisé à accéder à ses informations. Merci de l\'y ajouter.')
            tg_channel = None
        except Exception:
            logging.exception("Erreur inconnue")
            tg_channel = None

        return TelegramChannel.from_telethon_object(tg_channel)

    def is_user_authorized(self):
        return self.client.is_user_authorized()

    def sign_in(self, *args, **kwargs):
        return self.client.sign_in(*args, **kwargs)

    def send_code_request(self, *args, **kwargs):
        return self.client.send_code_request(*args, **kwargs)

    async def get_dialogs(self, *args, **kwargs) -> TelegramPersonnalChannel:
        res = []
        try:
            res = self.client.get_dialogs(*args, **kwargs)
        except sqlite3.OperationalError as e:
            try:
                self._manage_sqlite3_errors(e)
            except TwitterstormError as ee:
                logging.exception(ee)
        except Exception:
            logging.exception("Erreur inconnue")

        return [TelegramPersonnalChannel.from_telethon_object(c) for c in res]

    async def iter_participants(self, tg_channel, first_time = False, **kwargs):
        if tg_channel is None:
            logging.error("On essaie d'obtenir les participant·e·s d'un channel qui n'a pas été trouvé")
            return iter([])

        try:
            tg_participants = self.client.iter_participants(tg_channel, **kwargs)
        except Exception as e:
            logging.exception(e)
            return iter([])

        now = dt.datetime.now(s.TIMEZONE)
        # todo_es : !!!! lors d'une suppression de bdd postgres (ou nouveau campain_id), cette ligne plante au tout premier lancement, pas au 2nd
        default_sug_freq = await s.get_conf_value(s.CAMPAIN_ID, 'DEFAULT_SUGGESTIONS_FREQUENCY')

        res = [await TelegramParticipant.from_telethon_object(p, now, default_sug_freq, first_time)
               async for p in tg_participants]
        # todo_chk peut on utiliser yield ici?

        return iter(res)

    def send_message(self, tg_channel, message, **kwargs):
        if tg_channel is None:
            logging.error(
                "On essaie d'envoyer un message vers un channel qui n'a pas été trouvé\nMessage=\n" + str(message))
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

    @staticmethod
    def _manage_sqlite3_errors(e):
        if isinstance(e, sqlite3.OperationalError) and "database is locked" in str(e):
            raise TwitterstormError(
                ("La connection à Télégram est déjà utilisée. Essayez de supprimer le fichier {}.session\n" +
                 "Voici l'erreur d'origine :\n{}").format(
                    s.SESSION_LISTENING_LOOP, e))
        else:
            raise TwitterstormError(("Erreur inconnue. Essayez de supprimer le fichier {}.session\n" +
                                     "Voici l'erreur d'origine :\n{}").format(
                s.SESSION_LISTENING_LOOP, e))


class TelegramConnection(AbstractConnection):
    def __init__(self, db, telegram_client=None):
        logging.test(20041)
        AbstractConnection.__init__(self, db)
        if telegram_client is not None:
            self.tg_client = telegram_client
        else:
            self.tg_client = TelegramClientWrapper(s.SESSION_LISTENING_LOOP, ts.API_ID, ts.API_HASH)

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

    async def _is_reachable(self, participant):
        """
        Overrides method in AbstractConnection
        """
        logging.test(20042)
        return await self._is_id_reachable(participant.get_normalised_id())

    def connect(self):
        """
        Overrides method in AbstractConnection
        """
        logging.test(20043)
        self.tg_client.connect()
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

        Renvoie pour un·e participant·e donné·e le channel de conversation privée pour communiquer avec lui/elle
        """
        logging.test(20048)

        channel = await self.tg_client.get_input_entity(participant.get_tg_id())
        if channel.is_empty() and participant.tg_specific_data['tg_username'] is not None:
            logging.test(20049)
            logging.test(20050)
            logging.test(20051)
            logging.test(20052)
            channel = await self.tg_client.get_input_entity("@" + participant.tg_username)

        return channel

    def is_bot(self, participant):
        """
        Overrides method in AbstractConnection.
        Vérifie si le/la participant·e est le robot
        """
        logging.test(20053)
        # todo_es cette méthode c'est un peu du rafistolage, et is_admin aussi
        return participant.is_bot()

    async def is_admin(self, participant) -> bool:
        logging.test(20101)
        return await participant.is_admin()

    def _is_me(self, participant):
        """
        Overrides method in AbstractConnection.
        Vérifie si le/la participant·e est le compte ME (compte de test)
        """
        logging.test(20054)
        return participant.get_normalised_id() == TelegramParticipantId(ts.ME).get_normalised_id()

    async def _get_main_channel(self) -> TelegramChannel:
        """
        Overrides method in AbstractConnection.
        Retourne le channel principal sur lequel tous·tes les participant·e·s sont présent·e·s

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
        messages = [m for m in messages if
                    m.received_at > dt.datetime.now(s.TIMEZONE) - dt.timedelta(0, s.TIME_LIMIT_TO_FETCH_PREVIOUS_MSGS)]

        if len(messages):
            logging.test(20058)
            last_message_id = TelegramMessageId(
                max([m.id.get_tg_id() for m in messages]))  # todo_es m.id devrait déjà renvoyer un TelegramMessageId non?
        elif last_checked_message_tg_id is not None:
            logging.test(20059)
            last_message_id = TelegramMessageId(last_checked_message_tg_id)
        else:
            logging.test(20060)
            last_message_id = None

        participant.set_last_checked_msg(last_message_id)
        return messages, participant

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

        return await self.tg_client.get_entity(tg_channel_id.get_tg_id())

    async def _get_new_participants_from_main_channel(self, first_time=False, known_participants=None):
        """
        Overrides method in AbstractConnection.

        Retourne tous·tes les participant·e·s d'un channel à partir du nom de ce dernier,
        ainsi que le compte ME (compte de test) s'il fait partie de ce channel (necessaire
        si SEND_ONLY_TO_ME = True)
        @param known_participants:
        """
        if known_participants is None:
            known_participants = []

        channel = await self._get_main_channel()
        logging.test(20068)
        return await self._get_new_participants_from_channel(channel, first_time=first_time,
                                                             known_participants=known_participants)

    async def _user_authentification(self):
        # Si l'utilisateur n'est pas authentifié, ...
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
        # waiting_time = TelegramConnetion._find_waiting_time(exception)
        logging.error(s.STR_TG_TOO_MANY_INVALID.format(exception.seconds, ts.__name__))
        sys.exit()

    async def _get_all_channels(self):
        """
        Retourne tous les channels auxquels participe le compte du BOT
        """

        return await self.tg_client.get_dialogs()

    async def _get_new_participants_from_channel(self, channel,
                                                 first_time=False,
                                                 known_participants=None):
        """
        Retourne tous·tes les participant·e·s d'un channel
        """

        # todo_op : du coup la méthode db.get_all_participants_origids devient innutile
        #  bon pas ici mais faire en sorte que db.get_participants soit un itérable pour pas
        #  tout charger d'un coup

        if known_participants is None:
            known_participants = []

        if first_time:
            logging.test(20082)
            known_participants = await self._get_db_participants()
        else:  ###
            logging.test(20083)

        known_participants_ids = [p.get_normalised_id() for p in known_participants]

        already_seen_participants_ids = self.db.get_ids_of_former_participants()

        participants_iterable = await self.tg_client.iter_participants(channel.get_tg_channel(), aggressive=True, first_time = first_time)
        # todo_op le fonctionnement avc await est il optimisable ici ?
        all_channel_participants = [{'p_id': p.get_normalised_id(), # todo_es : simplifier cette groooooosse ligne (par exemple on fait plusieurs fois la verif 'in known_paticicpants_ids'
                                     'new_participant':
                                         p if p.get_normalised_id() not in known_participants_ids and p.get_normalised_id() not in already_seen_participants_ids
                                        else (self.db.get_participant_by_id(p.get_normalised_id(), self._get_participant_class()) if p.get_normalised_id() not in known_participants_ids and p.get_normalised_id() in already_seen_participants_ids
                                              else None)}
                                    for p in participants_iterable] # todo_chk y'a un warning ici
        all_channel_participants_ids = [p['p_id'] for p in all_channel_participants]
        tg_new_participants = [p['new_participant'] for p in all_channel_participants if
                               p['new_participant'] is not None]

        # Participants qui ne sont pas sortis du channel
        participants_still_in_the_channel = [p for p in known_participants if
                                             p.get_normalised_id() in all_channel_participants_ids]
        participants_who_left = [p for p in known_participants if
                                 p.get_normalised_id() not in all_channel_participants_ids]

        new_participants = [p for p in tg_new_participants if await self._is_id_reachable(p.get_normalised_id())]

        me = self._search_for_me(new_participants + participants_still_in_the_channel + participants_who_left)

        return new_participants, participants_still_in_the_channel, participants_who_left, me

    @staticmethod
    def _search_for_me(participants_list):
        me = None

        # todo_es : vérifier utilité d'un ME si pas selnd_only_to_me. Sinon, mettre if SEND_ONLY_TO_ME ici
        for p in participants_list:
            if p.get_tg_id() == ts.ME:
                logging.test(20087)
                me = p
            else:  ###
                logging.test(20088)

        return me

    async def _send_message(self, channel, msg):
        """
        Envoie un message via Télégram sur le channel donné
        """
        logging.test(20089)
        await self.tg_client.send_message(channel.get_tg_channel(), msg)

    @staticmethod
    async def _is_id_reachable(participant_id):
        """
        Indique s'il est possible d'interragir avec un participant donné (envoi de messages, etc.).
        """

        # todo_es ext_set = pas tres bo. variable d'environneemnt?
        reachable_participants = await s.get_reachable_participants_ids(s.CAMPAIN_ID)
        reachable_participants.append(TelegramParticipantId(ts.ME).get_normalised_id())
        # self._get_participants_new_from_channel
        # reachable_participants = [TelegramParticipantId(id_).get_normalised_id() for id_ in reachable_participants]
        # reachable_participants = [int(e) if type(e) == str else e for e in reachable_participants]

        if not await s.get_conf_value(s.CAMPAIN_ID, 'RESTRICT_REACHABLE_USERS'):
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
        # todo_chk : Il faut pouvoir se connecter avec un autre compte que le BOT
        # todo_cr : rester cette méthode
        logging.test(20094)
        channels = await self._get_all_channels()
        filtered_channels = [ch for ch in channels if string is None or string.lower() in ch.get_tg_channel().title.lower()]
        print("Liste des channels {}:".format("contenant '{}'".format(string) if string is not None else ""))

        for ch in filtered_channels:
            logging.test(20095)
            tg_channel = ch.get_tg_channel()
            if tg_channel is not None:
                cid = tg_channel.id
            else:
                cid = ""
            title = ch.get_tg_channel().title
            print("- [id= {} ] : '{}'".format(cid, title))

    async def display_participants_of_main_channel(self, search=None):
        logging.test(20096)
        participants, _, _, _ = await self._get_new_participants_from_main_channel()

        main_channel = await self._get_main_channel()
        main_channel = main_channel.get_tg_channel()
        title = main_channel.title if main_channel is not None else "[Channel non trouvé]"
        msg = "\nListe des participants du channel '{}'".format(title)
        msg += " contenant '{}':".format(search) if search is not None else ":"
        if await s.get_conf_value(s.CAMPAIN_ID,
                                  'RESTRICT_REACHABLE_USERS'):
            # todo_chk est ce que la BDD a été initialisée avec la conf avant d'arriver ici?
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


def run():  # todo_es: enlever à terme
    db = DataBase()
    conn = TelegramConnection(db).__enter__()
    # async.run(init(conn))
    # analyser = MessageAnalyser(conn, actions)
    conn.run_with_async_loop(conn.search_channels())


if __name__ == "__main__":  # todo_es: enlever à terme
    run()
