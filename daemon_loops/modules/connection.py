import datetime as dt
import random
from contextlib import AbstractContextManager

from asgiref.sync import sync_to_async

import daemon_loops.settings as s
from daemon_loops.models import PostedTweet, SentTweetUrl, SentTextSuggestion
from daemon_loops.modules.logger import logger
from daemon_loops.modules.message_generator import MessageGenerator
from daemon_loops.modules.twitterstorm_utils import TwitterstormError, get_time_before_suggesting


@sync_to_async
def quickfix3(**kwargs):
    SentTweetUrl(  # todo_es : a déplacer dans la classe BDD
        **kwargs
    ).save()


@sync_to_async
def quixkfix(**kwargs):
    SentTextSuggestion(**kwargs).save()


@sync_to_async
def quifix(**kwargs):
    return [a for a in SentTweetUrl.objects.filter(**kwargs)]


@sync_to_async
def quifix2(already_suggested_urls, campain_id=None, sender_id=None):
    return [a for a in PostedTweet.objects.filter(campain_id=campain_id).exclude(sender_id=sender_id). \
        exclude(url__in=already_suggested_urls)]  # query à tester


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
                 last_arrival_in_channel,
                 suggestions_frequency,
                 last_suggestion_url_or_text,
                 last_text_suggestion_id
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
        self.last_arrival_in_channel = last_arrival_in_channel
        self.suggestions_frequency = suggestions_frequency
        self.last_suggestion_url_or_text = last_suggestion_url_or_text
        self.last_text_suggestion_id = last_text_suggestion_id

        self.last_checked_msg_id = None
        self.set_last_checked_msg(last_checked_msg_id)

        self.time_before_suggesting_if_sandbox = get_time_before_suggesting()

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

    def right_time_to_suggest_if_sandbox(self, now, time_before_suggesting):
        if s.USE_SANDBOX :
            time_before_suggesting = self.time_before_suggesting_if_sandbox
        else :
            raise TwitterstormError("On ne doit pas appeler cette méthode si USE_SANBOX = False")
        return (self.last_arrival_in_channel + time_before_suggesting) < now

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
                       specific_data,
                       last_arrival_in_channel,
                       suggestions_frequency,
                       last_suggestion_url_or_text,
                       last_text_suggestion_id
                       ):
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

    async def _format_participants_info(self, participants_list):
        return [{'participant': p,
                '1to1_channel': await self._get_1to1_channel(p)}
                    for p in participants_list]

    async def fetch_all_participants(self, consent=None):
        """

        """
        participants = await self._format_participants_info(self._get_db_participants(consent=consent))
        return participants

    async def check_for_new_participants_in_main_channel(self, first_time=False, known_participants_info=[]):
        """

        """

        known_participants = [pi['participant'] for pi in known_participants_info]

        new_participants, participants_still_here, participants_who_left, me = await self._get_new_participants_from_main_channel(
            first_time=first_time, known_participants=known_participants)

        new_participants_info = await self._format_participants_info(new_participants)
        participants_who_left_info = await self._format_participants_info(participants_who_left)

        await self._check_me(me)

        self._add_and_update_participants(new_participants, participants_still_here)

        await self._welcome_and_say_goodbye(new_participants_info, participants_who_left_info)

        future = new_participants_info + known_participants_info

        return await self._format_participants_info(self._get_db_participants())
        # todo_op: en vrai on peut optimiser un peu en n'allant pas tout rechercher dans la BDD hein
        # todo_chk : si on enleve cette ligne, plus jamais on ne va fetcher les participants
        # dans la BDD, sauf à l'ilitialisation du prog, enfin si tu le programme un jour... :s


    async def _check_me(self, me):
        if self.me is None:
            logger.test(30017)
            if me is not None:
                logger.test(30018)
                self.me = me
                self.my_channel = await self._get_1to1_channel(me)
            else:
                logger.test(30019)
                if s.SEND_ONLY_TO_ME:
                    # todo_chk : vérifier l'utilité d'avoir un utilisateur ME si send_only_to_me = False.
                    # todo_chk : Si pas utile, décaler le if s.SEND_ONLY_TO_ME avant l'appel de la méthode _check_me
                    raise Exception("Attention, le compte de test ME doit être présent dans le channel dédié à la " +
                                    "twitterstorm si SEND_ONLY_TO_ME = True")
        else:  ###
            logger.test(30020)

    async def _welcome_and_say_goodbye(self, new_participants_info, participants_who_left_info):

        for pi in new_participants_info:
            participant = pi['participant']
            channel = pi['1to1_channel']

            if not self.is_bot(participant):

                if participant.is_scribe():
                    for m in s.WELCOME_SCRIBE_MSGS:
                        await self.send(participant, channel, m)
                else:
                    for m in s.WELCOME_NEW_PARTICIPANT_MSGS:
                        await self.send(participant, channel, m)

        for pi in participants_who_left_info:
            participant = pi['participant']
            channel = pi['1to1_channel']

            if not self.is_bot(participant):

                if participant.is_scribe():
                    for m in s.GOODBYE_SCRIBE_MSGS:
                        await self.send(participant, channel, m)
                else:
                    for m in s.GOODBYE_PARTICIPANT_MSGS:
                        await self.send(participant, channel, m)


    def _add_and_update_participants(self, new_participants, participants_still_here):
        version = dt.datetime.now(s.TIMEZONE)
        if len(new_participants):
            logger.test(30021)
            self._insert_participants(new_participants, version)
        else:  ###
            logger.test(30022)
        if len(participants_still_here):
            logger.test(30023)
            self._update_version_of_known_participants(participants_still_here, version)
        else:  ###
            logger.test(30024)

    def save_request_from_participant(self, message, action, participant):
        logger.test(30037)
        self.db.insert_messages_to_bot([{'campain': s.CAMPAIN_ID,
                                         'participant_id': participant.get_normalised_id(),
                                         'msg': message.message_str,
                                         'received_at': message.received_at,
                                         'processed_at': dt.datetime.now(s.TIMEZONE),
                                         'detected': None,  # todo_chk : c'est quoi ça ?
                                         "action_token": action}])

    def _get_db_participants(self, consent=None):
        """

        @rtype: list(AbstractParticipant)
        """
        logger.test(30025)
        return [p for p in self.db.get_participants(self._get_participant_class(), consent=consent) if
                self._is_reachable(p)]

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
            [{"campain": s.CAMPAIN_ID, "participant_id": participant.get_normalised_id(), "msg": msg,
              "sent_at": dt.datetime.now(s.TIMEZONE)}])

    async def _send_and_record_message(self, participant, channel, msg):
        """

        @rtype: None
        """
        logger.test(30028)
        suffix = s.MSG_SUFFIX if s.MSG_SUFFIX is not None else ""
        await self._send_message(channel, suffix + msg)
        self._record_sent_message(participant, suffix + msg)

    async def send(self, participant, channel, msg, force=False, debug=False):
        """

        @rtype: None
        """

        if not s.SEND_ONLY_TO_ME:
            logger.test(30029)
            if not self.is_bot(participant):
                logger.test(30032)
                logger.test(30033)
                logger.test(30034)
                if participant.is_ok or force:
                    await self._send_and_record_message(participant, channel, msg)
                else:
                    logger.warning(
                        "Il est bizarre que l'on tente d'envoyer un message à quelqu'un.e qui ne le souhaite pas." \
                        "(participant=%s (id=%s), '%s')" % (
                        participant.display_name, participant.get_normalised_id(), msg))

            else:  ###
                logger.test(30033)
        else:
            logger.test(30030)
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
        # todo_op : ici on fait 1 appel à la bdd
        #  pour chaque participant, pourquoi ne pas tout faire en meme temps?
        msgs = self._filter_messages_from_participant_to_bot(msgs, updated_participant)
        return msgs, updated_participant

    def _update_version_of_known_participants(self, participants, now):
        logger.test(30036)
        self.db.update_version_of_participants(participants, now)

    def update_suggestions_frequency(self, participant, minutes):
        self.db.update_participant_frequency(participant, minutes)
        participant.suggestions_frequency = minutes
        return participant

    def _update_last_suggestion(self, participant, datetime):
        self.db.update_last_suggestion(participant, dt.datetime.now(s.TIMEZONE))
        participant.last_suggestion_url_or_text = datetime
        return participant

    def _update_last_suggested_text(self, participant, text_id, datetime):
        participant = self._update_last_suggestion(participant, datetime)
        self.db.update_last_suggested_text(participant, text_id)
        participant.last_text_suggestion_id = text_id
        return participant

    async def send_suggestion(self, participant, channel, text_id=None, force=False):

        if text_id is None:
            random.seed(dt.datetime.now(s.TIMEZONE).microsecond)
            if not len(s.TWEET_TEXTS.keys()):
                return participant, False
            text_ids = list(s.TWEET_TEXTS.keys())
            text_id = random.choice(text_ids)

        text = MessageGenerator.generate_one_message([s.TWEET_TEXTS[text_id]])

        messages = self._format_text_suggestion_mesage(text)
        for to_send in messages:
            await self.send(participant, channel, to_send, force=force)

        participant = self._update_last_suggested_text(participant, text_id, dt.datetime.now(s.TIMEZONE))
        await quixkfix(campain_id=s.CAMPAIN_ID,
                       text_id=text_id,
                       sent_at=dt.datetime.now(s.TIMEZONE),
                       receiver_id=participant.get_normalised_id(),
                       sent_text=text)  # todo_es : pas bo

        return participant, True

    async def send_a_tweet_url(self, participant, channel):
        st = await quifix(campain_id=s.CAMPAIN_ID, receiver_id=participant.get_normalised_id())
        already_suggested_urls = [t.url for t in st]
        pt = await quifix2(already_suggested_urls, campain_id=s.CAMPAIN_ID, sender_id=participant.get_normalised_id())

        if len(pt):
            random.seed(dt.datetime.now(s.TIMEZONE).microsecond)
            chosen_one = random.choice(pt)
            to_send = self._format_url_suggestion_mesage(chosen_one)
            await self.send(participant, channel, to_send)

            participant = self._update_last_suggestion(participant, dt.datetime.now(s.TIMEZONE))
            await quickfix3(
                campain_id=s.CAMPAIN_ID,
                url=chosen_one.url,
                date_sent=dt.datetime.now(s.TIMEZONE),
                receiver_id=participant.get_normalised_id())

            return participant, True
        else:
            return participant, False

    def _format_url_suggestion_mesage(self, posted_tweet):
        name = posted_tweet.sender_name
        url = posted_tweet.url
        msg = s.URL_SUGGESTION_MSG_STR.format(name, url)
        return msg

    def _format_text_suggestion_mesage(self, text):
        # Le message 'text' doit être dans un message bien distinct, afin de pouvoir facilement le copier-coller
        return [s.TEXT_SUGGESTION_MSG_STR, text]

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
