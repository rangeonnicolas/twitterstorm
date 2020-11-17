import datetime as dt
from contextlib import AbstractContextManager

import settings as s
from modules.logger import Logger

logger = Logger()  # todo_f : revoir


class AbstractChannelId:
    pass


class AbstractParticipantId:
    def get_normalised_id(self) -> str:
        logger.test(30000)
        raise NotImplementedError()


class AbstractMessageId:
    def get_normalised_id(self) -> str:
        logger.test(30001)
        raise NotImplementedError()


class AbstractChannel:
    def get_specific_data(self) -> dict:
        logger.test(30002)
        raise NotImplementedError()


class AbstractMessage:
    def __init__(self, id_, message_str, received_at, sender_id):
        logger.test(30003)
        self._check_id_type(id_)
        self._check_sender_id_type(sender_id)

        self.id = id_
        self.message_str = message_str
        self.received_at = received_at
        self.sender_id = sender_id

    def _check_id_type(self, id_) -> bool:
        logger.test(30004)
        raise NotImplementedError()

    def _check_sender_id_type(self, sender_id) -> bool:
        logger.test(30005)
        raise NotImplementedError()

    def get_normalised_sender_id(self) -> str:
        logger.test(30006)
        return self.sender_id.get_normalised_id()

    def get_normalised_id(self) -> str:
        logger.test(30007)
        return self.id.get_normalised_id()


class AbstractParticipant:
    def __init__(self,
                 campain,
                 id_,
                 display_name,
                 is_ok,
                 version,
                 date_fetched,
                 last_checked_msg_id,
                 last_consent_modified,
                 ):
        logger.test(30008)
        self._check_id_type(id_)

        self.campain = campain
        self.id = id_
        self.display_name = display_name
        self.is_ok = is_ok
        self.version = version
        self.date_fetched = date_fetched
        self.last_consent_modified = last_consent_modified

        self.last_checked_msg_id = None
        self.set_last_checked_msg(last_checked_msg_id)

    def get_normalised_id(self) -> str:
        logger.test(30009)
        return self.id.get_normalised_id()

    def get_last_checked_message_id(self) -> str:
        if self.last_checked_msg_id is None:
            logger.test(30010)
            return None
        else:
            logger.test(30011)
            return self.last_checked_msg_id.get_normalised_id()

    def set_last_checked_msg(self, last_checked_message_id):
        if last_checked_message_id is not None:
            logger.test(30012)
            self._check_message_id_type(last_checked_message_id)
        else:  ###
            logger.test(30013)
        self._set_last_checked_msg(last_checked_message_id)

    def _check_id_type(self, id_) -> bool:
        raise NotImplementedError()

    def _check_message_id_type(self, last_checked_message_id) -> bool:
        raise NotImplementedError()

    def is_trusted_participant_for_tweets(self) -> bool:
        raise NotImplementedError()

    def get_specific_data(self) -> dict:
        raise NotImplementedError()

    def _set_last_checked_msg(self, last_checked_message_id):
        raise NotImplementedError()

    def is_scribe(self):
        raise NotImplementedError()

    @staticmethod
    def create_from_db(campain,
                       normalised_id,
                       display_name,
                       is_ok,
                       version,
                       date_fetched,
                       last_checked_msg_id,
                       last_consent_modified,
                       specific_data):
        raise NotImplementedError()


class AbstractConnection(AbstractContextManager):
    def __init__(self, database_connection):
        """
        Méthode __init__
        @rtype: None
        """
        logger.test(30014)
        self.db = database_connection
        self.me = None
        self.my_channel = None

    def __enter__(self):
        """
        Méthode "__enter__" du Context Manager.
        @rtype: AbstractConnection
        """
        logger.test(30015)
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Méthode "__exit__" du Context Manager.
        @rtype: None
        """
        logger.test(30016)
        self.disconnect(exc_type, exc_value, traceback)

    async def check_for_new_participants_in_main_channel(self, first_time=False, known_participants=[]):
        """

        @rtype: None
        """
        new_participants, participants_still_here, me = await self._get_new_participants_from_main_channel(
            first_time=first_time, known_participants=known_participants)

        if self.me is None:
            logger.test(30017)
            if me is not None:
                logger.test(30018)
                self.me = me
                self.my_channel = await self._get_1to1_channel(me)
            else:
                logger.test(30019)
                if s.SEND_ONLY_TO_ME:
                    raise Exception("Attention, le compte de test ME doit être présent dans le channel dédié à la " +
                                    "twitterstorm si SEND_ONLY_TO_ME = True")
        else:  ###
            logger.test(30020)

        self._add_and_update_participants(new_participants, participants_still_here)

        return [{'participant': p, '1to1_channel': await self._get_1to1_channel(p)} for p in
                self._get_db_participants()]
        # todo_f: en vrai on peut optimiser un peu en n'allant pas tout rechercher dans la BDD hein
        # todo_f : si on enleve cette ligne, plus jamais on ne va fetcher les participants
        #  todo_f : dans la BDD, sauf à l'ilitialisation du prog, enfin si tu le programme un jour... :s

    def _add_and_update_participants(self, new_participants, participants_still_here):
        version = dt.datetime.now(s.TIMEZONE)
        if len(new_participants):
            logger.test(30021)
            self._insert_participants(new_participants, version)
        else:  ###
            logger.test(30022)
        if len(participants_still_here):
            logger.test(30023)
            self._update_known_participants(participants_still_here, version)
        else:  ###
            logger.test(30024)

    def save_request_from_participant(self, message, action, participant):
        logger.test(30037)
        self.db.insert_messages_to_bot([{'campain': s.CAMPAIN_NAME,
                                         'participant_id': participant.get_normalised_id(),
                                         'msg': message.message_str,
                                         'received_at': message.received_at,
                                         'processed_at': dt.datetime.now(s.TIMEZONE),
                                         'detected': None,  # todo : c'est quoi ça ?
                                         "action_token": action}])

    def _get_db_participants(self):
        """

        @rtype: list(AbstractParticipant)
        """
        logger.test(30025)
        return [p for p in self.db.get_participants(self._get_participant_class()) if self._is_reachable(p)]

    # def _get_db_participants_ids(self):
    #    """
    #
    #    @rtype: list(int)
    #    """
    #    return self.db.get_all_participants_ids(self._get_participant_class())

    def _insert_participants(self, participants, now):
        """

        @rtype: None
        """
        logger.test(30026)
        self.db.insert_participants(participants, now)

    def _record_sent_message(self, participant, msg):
        """

        @rtype: None
        """
        logger.test(30027)
        self.db.record_sent_message(
            [{"campain": s.CAMPAIN_NAME, "participant_id": participant.get_normalised_id(), "msg": msg,
              "sent_at": dt.datetime.now(s.TIMEZONE)}])

    async def _send_and_record_message(self, participant, channel, msg):
        """

        @rtype: None
        """
        logger.test(30028)
        await self._send_message(channel, msg)
        self._record_sent_message(participant, msg)

    async def send(self, participant, channel, msg, debug=False):
        """

        @rtype: None
        """
        print("Wesh mais gros, où tu vérifie si les gens sont reachable avant de leur envoyer??????????????")
        # todo : à faire!!!!!!!!!!!!!!!
        if not s.SEND_ONLY_TO_ME:
            logger.test(30029)
            if not self.is_bot(participant):
                logger.test(30032)
                logger.test(30033)
                logger.test(30034)
                await self._send_and_record_message(participant, channel, msg)
            else:  ###
                logger.test(30033)
        else:
            logger.test(30030)
            print(self.me, self.my_channel)
            if self.me is None or self.my_channel is None:
                logger.test(30031)
                raise Exception("Il semble que self.me ou self.my_channel n'aient pas été initialisés.")
            else:  ###
                logger.test(30032)
            msg = "Message initialement destiné à \n{}\n(id={}) :\n\n{}".format(participant.display_name,
                                                                                participant.get_normalised_id(), msg)
            await self._send_and_record_message(self.me, self.my_channel, msg)

    def send_message_to_all_participants(self, message, participant, participants_info):
        self._filter_reachable_participants(participants_info)
        logger.test(30033)
        print(
            "Ouais euh... j'ai un peu la flemme de le développer là (à l'origine tu veux envoyer un msg à toute la "
            "boucle)")
        return 2983879287987398792

    def _filter_reachable_participants(self, participants_info):
        logger.test(30034)
        return "La flemme"

    async def check_for_new_messages(self, participant, channel):
        logger.test(30035)
        msgs, updated_participant = await self._get_messages(channel, participant)
        self.db.update_last_checked_msg(updated_participant)
        # todo : ici on fait 1 appel à la bdd
        # todo : pour chaque participant, pourquoi ne pas tout faire en meme temps?
        msgs = self._filter_messages_from_participant_to_bot(msgs, updated_participant)
        return msgs, updated_participant

    def _update_known_participants(self, participants, now):
        logger.test(30036)
        self.db.update_participants(participants, now)

    def connect(self):
        """

        """
        raise NotImplementedError()

    def disconnect(self, exc_type, exc_value, traceback) -> None:
        """

        """
        raise NotImplementedError()

    async def _get_1to1_channel(self, participant) -> AbstractChannel:
        """

        """
        raise NotImplementedError()

    def _is_reachable(self, participant) -> bool:
        """

        """
        raise NotImplementedError()

    def _is_me(self, participant) -> bool:
        """

        """
        raise NotImplementedError()

    def is_bot(self, participant) -> bool:
        """

        """
        raise NotImplementedError()

    def _get_main_channel(self) -> AbstractChannel:
        """
        Retourne le channel principal sur lequel tous.tes les participant.e.s sont présent.e.s
        """
        raise NotImplementedError()

    @staticmethod
    def _filter_messages_from_participant_to_bot(messages, participant):
        raise NotImplementedError()

    def _get_participant_class(self):
        raise NotImplementedError()

    def _get_messages(self, channel, participant):
        raise NotImplementedError()

    def _send_message(self, channel, msg):
        raise NotImplementedError()

    async def _get_new_participants_from_main_channel(self, first_time=False, known_participants=[]):
        raise NotImplementedError()
