from modules.connection import AbstractMessageId, AbstractParticipant, AbstractConnection, AbstractChannel, \
    AbstractParticipantId, AbstractMessage

import datetime as dt
import json
import re
import sqlite3
import struct
import sys

from telethon.errors.rpcerrorlist import PhoneCodeInvalidError, AuthKeyUnregisteredError, FloodWaitError, \
    PeerIdInvalidError
from telethon.sync import TelegramClient

import settings as s
import telegram_settings as ts
from modules.connection import AbstractMessageId, AbstractParticipant, AbstractConnection, AbstractChannel, \
    AbstractParticipantId, AbstractMessage
from modules.logger import Logger
from modules.twitterstorm import TwitterstormError

logger = Logger()


class TelegramChannelId:
    def __init__(self, tg_id):
        if not isinstance(tg_id, int):
            logger.test(20000)
            raise TwitterstormError("Un id Télégram est toujours un nombre entier")
        else:  ###
            logger.test(20001)
        self.tg_specific_data = {'tg_id': tg_id}

    def get_normalised_id(self) -> str:
        logger.test(20002)
        return str(s.CAMPAIN_NAME) + '_chan_' + str(self.tg_specific_data['tg_id'])

    def get_tg_id(self):
        logger.test(20003)
        return self.tg_specific_data['tg_id']


class TelegramParticipantId(AbstractParticipantId):
    def __init__(self, tg_id):
        if not isinstance(tg_id, int):
            logger.test(20004)
            raise TwitterstormError("Un id Télégram est toujours un nombre entier")
        else:  ###
            logger.test(20005)
        self.tg_specific_data = {'tg_id': tg_id}

    def get_normalised_id(self) -> str:
        logger.test(20006)
        return str(s.CAMPAIN_NAME) + '_ptcp_' + str(self.tg_specific_data['tg_id'])

    def get_tg_id(self) -> int:
        logger.test(20007)
        return self.tg_specific_data['tg_id']


class TelegramMessageId(AbstractMessageId):
    type_str = '_msg_'

    def __init__(self, tg_id):
        logger.test(20008)
        if not isinstance(tg_id, int):
            logger.test(20009)
            raise TwitterstormError("Un id Télégram est toujours un nombre entier")
        else:  ###
            logger.test(20010)
        self.tg_specific_data = {'tg_id': tg_id}

    def get_normalised_id(self) -> str:
        logger.test(20011)
        return str(s.CAMPAIN_NAME) + self.type_str + str(self.tg_specific_data['tg_id'])

    def get_tg_id(self) -> int:
        logger.test(20012)
        return self.tg_specific_data['tg_id']

    @staticmethod
    def from_normalised_id_to_tg_id(norm_id):
        logger.test(20013)
        regexp = '%s(\d+)\Z' % re.escape(TelegramMessageId.type_str)
        try:
            logger.test(20014)
            tg_id = re.findall(regexp, norm_id)[0]
        except IndexError:
            logger.test(20015)
            raise TwitterstormError("L'argument norm_id est mal formé, il ne correspond pas à la regexp '%s'" % regexp)
        try:
            logger.test(20016)
            tg_id = int(tg_id)
        except ValueError:
            logger.test(20017)
            raise TwitterstormError("L'argument norm_id est mal formé, l'id doit être un entier")
        return tg_id


class TelegramChannel(AbstractChannel):
    def __init__(self, tg_channel):
        logger.test(20018)
        self.tg_specific_data = {'tg_channel': tg_channel}

    def get_specific_data(self) -> dict:
        logger.test(20019)
        return self.tg_specific_data

    def get_tg_channel(self):
        logger.test(20020)
        return self.tg_specific_data['tg_channel']


class TelegramMessage(AbstractMessage):
    def __init__(self, tg_message):
        logger.test(20021)
        sender_id = TelegramParticipantId(tg_message.sender_id)
        msg_id = TelegramMessageId(tg_message.id)
        AbstractMessage.__init__(self, msg_id, tg_message.message, tg_message.date, sender_id)

    def _check_id_type(self, id_) -> None:
        if not isinstance(id_, TelegramMessageId):
            logger.test(20022)
            raise TwitterstormError(
                "L'argument 'sender_id' doit être de type TelegramMessageId")
        else:  ###
            logger.test(20023)

    def _check_sender_id_type(self, sender_id) -> None:
        if not isinstance(sender_id, TelegramParticipantId):
            logger.test(20024)
            raise TwitterstormError(
                "L'argument 'sender_id' doit être de type TelegramParticipantId")
        else:  ###
            logger.test(20025)


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
                 ):
        logger.test(20026)
        id_ = TelegramParticipantId(tg_id)
        if tg_last_checked_msg_id is not None:
            logger.test(20027)
            last_checked_msg_id = TelegramMessageId(tg_last_checked_msg_id)
        else:
            logger.test(20028)
            last_checked_msg_id = None

        first_name = tg_first_name if tg_first_name is not None else ""
        last_name = tg_last_name if tg_last_name is not None else ""
        username = "(@" + tg_username + ")" if tg_username is not None else ""
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
                                     )

        self.tg_specific_data = {
            'tg_id': tg_id,
            # 'tg_last_checked_msg_id': tg_last_checked_msg_id,
            'tg_first_name': tg_first_name,
            'tg_last_name': tg_last_name,
            'tg_username': tg_username
        }

    def _check_id_type(self, id_) -> None:
        if not isinstance(id_, TelegramParticipantId):
            logger.test(20029)
            raise TwitterstormError("L'argument 'id' doit être de type TelegramParticipantId")
        else:  ###
            logger.test(20030)

    def _check_message_id_type(self, last_checked_message_id) -> None:
        if not isinstance(last_checked_message_id, TelegramMessageId):
            logger.test(20031)
            raise TwitterstormError("L'argument 'last_checked_message_id' doit être de type TelegramMessageId")
        else:  ###
            logger.test(20032)

    def _set_last_checked_msg(self, last_checked_message_id):
        logger.test(20033)
        self.last_checked_msg_id = last_checked_message_id

    def get_last_checked_msg_tg_id(self):
        logger.test(20034)
        return TelegramMessageId.from_normalised_id_to_tg_id(
            self.last_checked_msg_id.get_normalised_id()) if self.last_checked_msg_id is not None else None
        # todo : j'ai l'impression que c'est dégeu mais j'en suis pas sur

    def is_scribe(self):
        logger.test(20035)
        return self.get_tg_id() in ts.SCRIBES

    def get_specific_data(self) -> dict:
        logger.test(20036)
        return self.tg_specific_data

    def is_trusted_participant_for_tweets(self) -> bool:  # todo : voir si on veut garder cette feature
        logger.test(20037)
        return True

    def get_tg_id(self) -> int:
        logger.test(20038)
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
                       specific_data) -> AbstractParticipant:

        tg_specific_data = json.loads(specific_data)
        try:
            logger.test(20039)
            tg_id = tg_specific_data['tg_id']
            tg_first_name = tg_specific_data['tg_first_name']
            tg_last_name = tg_specific_data['tg_last_name']
            tg_username = tg_specific_data['tg_username']
            # tg_last_checked_msg_id = tg_specific_data['tg_last_checked_msg_id']
        except KeyError:
            logger.test(20040)
            raise TwitterstormError("Vous utilisez probablement une ancienne version du schéma de la BDD")

        tg_last_checked_msg_id = TelegramMessageId.from_normalised_id_to_tg_id(
            last_checked_msg_id) if last_checked_msg_id is not None else None

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
            last_consent_modified
        )


class TelegramConnection(AbstractConnection):
    def __init__(self, *args, **kwargs):
        logger.test(20041)
        AbstractConnection.__init__(self, *args, **kwargs)
        self.tg_client = TelegramClient(s.SESSION_LISTENING_LOOP, ts.API_ID, ts.API_HASH)

    def _is_reachable(self, participant):
        """
        Overrides method in AbstractConnection
        """
        logger.test(20042)
        return self._is_id_reachable(participant.get_normalised_id())

    def connect(self):
        """
        Overrides method in AbstractConnection
        """
        logger.test(20043)
        self.tg_client.connect()
        self.tg_client.loop.run_until_complete(self._user_authentification())
        return self  # todo: on peut encore séparer le context manager de toutes les autres méthodes

    def disconnect(self, exc_type, exc_value, traceback):
        """
        Overrides method in AbstractConnection
        """
        if exc_type is not None:
            logger.test(20046)
            if isinstance(exc_type, ConnectionError):
                logger.test(20047)
                raise TwitterstormError(("La connection à Télégram a expirée. Reconnectez-vous.\n" +
                                         "Le cas échéant, supprimez le fichier {}").format(s.SESSION_LISTENING_LOOP))
            else:  ###
                logger.test(20044)
        else:  ###
            logger.test(20045)
        self.tg_client.disconnect()

    async def _get_1to1_channel(self, participant):
        """
        Overrides method in AbstractConnection.

        Renvoie pour un.e participant.e donné.e le channel de conversation privée pour communiquer avec lui/elle
        """
        try:
            logger.test(20048)
            channel = await self.tg_client.get_input_entity(participant.get_tg_id())
        except ValueError:
            if participant.tg_username is None:
                logger.test(20049)
                return None
            else:
                logger.test(20050)
            try:
                logger.test(20051)
                channel = await self.tg_client.get_input_entity("@" + participant.tg_username)
            except ValueError:
                logger.test(20052)
                return None  # todo: gérer le cas où channel = None dans les fonctions appelant _get_1to1_channel
        return TelegramChannel(channel)

    def is_bot(self, participant):
        """
        Overrides method in AbstractConnection.
        Vérifie si le/la participant.e est le robot
        """
        logger.test(20053)
        return participant.get_normalised_id() == TelegramParticipantId(ts.BOT).get_normalised_id()

    def _is_me(self, participant):
        """
        Overrides method in AbstractConnection.
        Vérifie si le/la participant.e est le compte ME (compte de test)
        """
        logger.test(20054)
        return participant.get_normalised_id() == TelegramParticipantId(ts.ME).get_normalised_id()

    async def _get_main_channel(self) -> TelegramChannel:
        """
        Overrides method in AbstractConnection.
        Retourne le channel principal sur lequel tous.tes les participant.e.s sont présent.e.s

        """
        logger.test(20055)
        return await self._get_tgchannel_from_id(TelegramChannelId(ts.MAIN_CHANNEL_ID))

    def _get_participant_class(self):
        logger.test(20056)
        return TelegramParticipant  # todo : en fait non. créer une méthode dans TelegramConnection appelée
        # create_participant, puis dans database.py>get_users, remplacer participant_class par conn.create_participant

    async def _get_messages(self, channel, participant):
        last_checked_message_tg_id = participant.get_last_checked_msg_tg_id()
        kwargs = {
            'min_id': last_checked_message_tg_id} \
            if last_checked_message_tg_id is not None else {}

        messages = await self.tg_client.get_messages(channel.get_tg_channel(), ts.NB_MSG_TO_FETCH, **kwargs)

        if len(messages):
            logger.test(20058)
            last_message_id = TelegramMessageId(max([m.id for m in messages]))
        elif last_checked_message_tg_id is not None:
            logger.test(20059)
            last_message_id = TelegramMessageId(last_checked_message_tg_id)
        else:
            logger.test(20060)
            last_message_id = None

        participant.set_last_checked_msg(last_message_id)
        return [TelegramMessage(m) for m in messages], participant

    @staticmethod
    def _filter_messages_from_participant_to_bot(messages, participant):
        logger.test(20061)
        return [m for m in messages
                if m.get_normalised_sender_id() == participant.get_normalised_id()]

    async def _get_tgchannel_from_id(self, tg_channel_id):
        """
        Retourne un channel Télégramme à partir de son identifiant
        @return: TelegramChannel
        """
        unknown_channel_msg = 'L\'identifiant du channel demandé ({}) est inconnu'.format(tg_channel_id.get_tg_id())
        try:
            logger.test(20063)
            channel = await self.tg_client.get_entity(tg_channel_id.get_tg_id())
        except struct.error:
            logger.test(20064)
            raise TwitterstormError(unknown_channel_msg)
        except PeerIdInvalidError:
            logger.test(20065)
            raise TwitterstormError(
                unknown_channel_msg + '\nIl est possible que le compte Télégram qu\'utilise le bot' +
                ' ne soit pas parmi les membres du channel principal. Il n\'est donc pas ' +
                'autorisé à accéder à ses informations. Merci de l\'y ajouter.')
        except AuthKeyUnregisteredError as e:
            logger.test(20066)
            raise e
        logger.test(20067)
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
        logger.test(20068)
        return await self._get_new_participants_from_channel(channel, first_time=first_time,
                                                             known_participants=known_participants)

    async def _user_authentification(self):
        # Si l'utilisateur n'est pas authentifié, ...
        if not await self.tg_client.is_user_authorized():

            # ... on lui envoie le code de validation sur son Télégram.
            try:
                logger.test(20069)
                await self.tg_client.send_code_request(ts.BOT_PHONE_NUMBER)
            except FloodWaitError as e:
                logger.test(20070)
                # Cas où le code a été saisi trop de fois de manière erronée
                self._manage_flood_wait_error(e)

            # L'utilisateur doit ensuite saisir son code ici :
            code_is_valide = False
            while not code_is_valide:
                logger.test(20071)
                code = input(s.STR_TG_ENTER_CODE.format(ts.BOT_PHONE_NUMBER))
                try:
                    logger.test(20072)
                    await self.tg_client.sign_in(ts.BOT_PHONE_NUMBER, code)
                except PhoneCodeInvalidError:
                    logger.test(20073)
                    # Si le code est incorrect
                    code_is_valide = False
                    logger.write(s.STR_TG_INVALID_CODE.format(ts.BOT_PHONE_NUMBER))
                except FloodWaitError as e:
                    logger.test(20074)
                    # Cas où le code a été saisi trop de fois de manière erronée
                    self._manage_flood_wait_error(e)
                else:
                    logger.test(20075)
                    # Si le code est bon
                    code_is_valide = True
                    logger.write(s.STR_TG_AUTH_OK)
        else:  ###
            logger.test(20076)

    @staticmethod
    def _find_waiting_time(exception):
        """
        Retourne le temps restant avant de pouvoir retenter une connection à Télégram.
        """
        try:
            logger.test(20077)
            waiting_time = re.findall("wait of (.*?) seconds", str(exception))[0]
        except IndexError:
            logger.test(20078)
            waiting_time = " ? "
        return waiting_time

    @staticmethod
    def _manage_flood_wait_error(exception):
        """
        Méthode appéles dans le cas où le code a été saisi trop de fois de manière erronée :
        Télégram exige alors un temps d'attente avant de pouvoir retenter sa chance.
        """
        logger.test(20079)
        waiting_time = TelegramConnection._find_waiting_time(exception)
        logger.error(s.STR_TG_TOO_MANY_INVALID.format(waiting_time, ts.__name__))
        sys.exit()

    async def _get_all_channels(self):
        """
        Retourne tous les channels auxquels participe le compte du BOT
        """
        try:
            logger.test(20080)
            channels = await self.tg_client.get_dialogs()
        except sqlite3.OperationalError as e:
            logger.test(20081)
            raise TwitterstormError("Erreur très chelou. Essayez de supprimer le fichier {}\n" +
                                    "Voici l'erreur d'origine :\n{}".format(
                                        s.SESSION_LISTENING_LOOP, e))

        return [{'title': ch.title, 'channel': TelegramChannel(ch)} for ch in channels]

    async def _get_new_participants_from_channel(self, channel,
                                                 first_time=False,
                                                 known_participants=[]):
        # dans le nom de la méthode
        """
        Retourne tous.tes les participant.e.s d'un channel
        """
        now = dt.datetime.now(s.TIMEZONE)
        me = None

        # db_participants_id = self.db.get_all_participants_origids(TelegramParticipant)
        # todo : du coup la méthode db.get_all_participants_origids devient innutile
        # todo : bon pas ici mais faire en sorte que db.get_participants soit un itérable pour pas
        # todo : tout charger d'un coup

        if first_time:
            logger.test(20082)
            known_participants = self._get_db_participants()
        else:  ###
            logger.test(20083)

        known_participants_tg_ids = [p.get_tg_id() for p in known_participants]

        tg_participants_iterable = self.tg_client.iter_participants(channel.get_tg_channel(), aggressive=True)
        tg_all_participants = [{'p_id': p.id,
                                'new_participant': p if p.id not in known_participants_tg_ids else None}
                               async for p in tg_participants_iterable]
        all_participants_tg_ids = [p['p_id'] for p in tg_all_participants]
        tg_new_participants = [p['new_participant'] for p in tg_all_participants if p['new_participant'] is not None]

        # Participants qui ne sont pas sortis du channel
        participants_still_in_the_channel = [p for p in known_participants if p.get_tg_id() in all_participants_tg_ids]

        new_participants = []

        for p in tg_new_participants:
            logger.test(20084)
            normalised_id = TelegramParticipantId(p.id).get_normalised_id()
            if self._is_id_reachable(normalised_id):
                logger.test(20085)
                new_participant = TelegramParticipant(
                    s.CAMPAIN_NAME,
                    p.id,
                    p.first_name,
                    p.last_name,
                    p.username,
                    s.DEFAULT_CONSENT,
                    None,
                    now,
                    None,
                    None
                )
                new_participants.append(new_participant)
                # bonne nouvelle : ts.ME n'a plu besoin d'etre readable ;) !!!!!
                # if p.id == ts.ME:
                #    me = new_participant
            else:
                logger.test(20086)

        for p in new_participants + participants_still_in_the_channel:
            if p.get_tg_id() == ts.ME:
                logger.test(20087)
                me = p
            else:  ###
                logger.test(20088)

        return new_participants, participants_still_in_the_channel, me

    async def _send_message(self, channel, msg):
        """
        Envoie un message via Télégram sur le channel donné
        """
        logger.test(20089)
        await self.tg_client.send_message(channel.get_tg_channel(), msg)

    @staticmethod
    def _is_id_reachable(participant_id):
        """
        Indique s'il est possible d'interragir avec un participant donné (envoi de messages, etc.).
        """

        reachable_participants = ts.REACHABLE_USERS + [ts.ME]
        # self._get_participants_new_from_channel
        reachable_participants = [TelegramParticipantId(id_).get_normalised_id() for id_ in reachable_participants]
        # reachable_participants = [int(e) if type(e) == str else e for e in reachable_participants]

        if not ts.RESTRICT_REACHABLE_USERS:
            logger.test(20090)
            return True
        else:
            logger.test(20091)
            if participant_id in reachable_participants:
                logger.test(20092)
                return True
            else:  ###
                logger.test(20093)
            return False

    async def search_channels(self, string=None):
        logger.test(20094)
        channels = await self._get_all_channels()
        filtered_channels = [ch for ch in channels if string is None or string.lower() in ch['title'].lower()]
        print("Liste des channels {}:".format("contenant '{}'".format(string) if string is not None else ""))
        # todo: print console, pas dans le logger

        for ch in filtered_channels:
            logger.test(20095)
            tg_channel = ch['channel'].get_tg_channel()
            cid = tg_channel.id
            title = ch['title']
            print("- [id= {} ] : '{}'".format(cid, title))

    async def display_participants_of_main_channel(self, search=None):
        logger.test(20096)
        participants, _, _ = await self._get_new_participants_from_main_channel()

        main_channel = await self._get_main_channel()
        title = main_channel.get_tg_channel().title
        msg = "Liste des participants du channel '{}'".format(title)
        msg += " contenant '{}':".format(search) if search is not None else ":"
        print(msg)  # todo: console, pas dans le logger

        for p in participants:
            logger.test(20097)
            first_name = p.get_specific_data()['tg_first_name']
            last_name = p.get_specific_data()['tg_last_name']
            username = p.get_specific_data()['tg_username']

            first_name = first_name if first_name is not None else ""
            last_name = last_name if last_name is not None else ""
            username = "@" + username + " " if username is not None else "? "

            for_search = first_name + last_name + username
            if search is None or search.lower() in for_search.lower():
                logger.test(20098)
                pid = p.get_tg_id()
                total_len = len(str(pid) + first_name + last_name)
                space = " " * (30 - total_len)
                print("- [id= {} ]: {} {}{} [username = {}]".format(pid, first_name, last_name, space, username))
            else:
                logger.test(20099)
