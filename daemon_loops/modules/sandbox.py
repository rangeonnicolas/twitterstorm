from asgiref.sync import sync_to_async

from daemon_loops.models import SentPlannedMessage, PostedTweet
from daemon_loops.modules.telegram import TelegramParticipant
from settings.settings import CAMPAIN_ID
import datetime as dt
from settings import settings as s
from settings.sandbox_settings import MESSAGE_EXPIRATION, orig_tweets, ANIMATOR_MSG_INTRO

import re

TIMEZONE = s.TIMEZONE


@sync_to_async
def wesh(t):  # todo_es : pas bo
    PostedTweet(campain_id=CAMPAIN_ID,
                url=t,
                date_received=dt.datetime.now(TIMEZONE),
                sender_id="une personne",
                sender_name=re.findall(r"twitter\.com/([^/]+)/", t)[0],
                ).save()


async def populate():
    for t in orig_tweets:
        await wesh(t)


class SandboxParticipant(TelegramParticipant):
    def __init__(self, p):
        TelegramParticipant.from_pair(self, p)

    async def check_for_planned_message(self, now, msgs):
        to_send = []

        for message_id, message_data in msgs.items():

            delta = dt.timedelta(0, message_data['seconds_after_participant_arrival_in_loop'])
            sender = message_data['sender']
            message_txt = message_data['msg']

            when_to_send_the_message = self.last_arrival_in_channel + delta
            it_is_a_bit_too_late_to_send_it = when_to_send_the_message + dt.timedelta(0, MESSAGE_EXPIRATION)

            if when_to_send_the_message < now and now < it_is_a_bit_too_late_to_send_it:
                if not await self._check_if_already_sent(message_id):
                    message = s.ANIMATOR_MSG_SUFFIX + ANIMATOR_MSG_INTRO % (sender, message_txt)

                    to_send.append({
                        'msg_id': message_id,
                        'message': message,
                    })

        return to_send

    @sync_to_async
    def _check_if_already_sent(self, message_id):
        objs = SentPlannedMessage.objects.filter(
            campain_id=CAMPAIN_ID,
            receiver_id=self.get_normalised_id(),
            planned_message_id=message_id,
            sent_at__gte=self.last_arrival_in_channel
        )
        return len(objs) >= 1

    @sync_to_async
    def record_planned_message(self,
                               m):  # todo_es : cette méthode devrait plutot etre dans la classe sandbox_connection (
        #                               les autres aussi?)
        SentPlannedMessage(
            campain_id=CAMPAIN_ID,
            planned_message_id=m['msg_id'],
            sent_at=dt.datetime.now(TIMEZONE),
            receiver_id=self.get_normalised_id(),  # todo_es : a transformer en foreign key quand on pourra
            sent_text=m['message']
        ).save()
