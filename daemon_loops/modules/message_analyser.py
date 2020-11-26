from asgiref.sync import sync_to_async
import settings as s

from daemon_loops.modules.connection import AbstractParticipant
from daemon_loops.modules.twitterstorm_utils import TwitterstormError
import daemon_loops.modules.logging as logging

MESSAGE_NOT_UNDERSTOOD_STR = \
    s.ROBOT_MSG_SUFFIX + """Désolé, je n'ai pas compris ton message.

👉🏼 Si tu n'es plus disponible pour cette mob, envoies-moi __**STOP**__, et je me taierai.

👉🏼 Si je suis trop (ou pas assez) bavard, envoies __**FREQ 1**__, en remplaçant __**1**__ par le nombre de \
minutes desquelles \
tu veux que j'espace mes messages.

👉🏼 Si tu détectes un bug de mon fonctionnement (ou des fautes d'orthographe), envoies-moi __**BUG**__ suivi de \ 
la description du problème.

👉🏼 De ton côté, je t'invite à m'envoyer les URL des tweets que tu as postés, afin que je les propose aux \
autres activistes de la boucle. Je suis spécialement entraîné à reconnaître les URL des tweets (de type \
https://twitter.com/pseudo/status/13297...), je saurai donc les détecter dans les messages que tu m'enverras ici \ 
😊

👉🏼 Si tu souhaites t'adresser à de vrais humains, tu peux poster un message dans la boucle __**{}**__.
""".format(s.boucle)


MESSAGE_NOT_UNDERSTOOD_STR_ADMIN = "Bon sérieux mec, j'ai pas pigé ton message. Voici les actions possibles : {}"



class MessageAnalyser:
    def __init__(self, conn, actions, admin_actions):
        self.actions = actions
        self.admin_actions = admin_actions
        self.conn = conn
        logging.test(10003)

    @staticmethod
    def participant_has_requested_an_action(action_conf, m, participant):
        fn = action_conf['test_func']
        logging.test(10004)
        return fn(m.message_str, participant.get_normalised_id())

    async def analyse_message_from_normal_participant(self, message, participant, channel):
        return await self._analyse_messages_and_take_actions(self.actions, MESSAGE_NOT_UNDERSTOOD_STR, message, participant, channel)

    async def analyse_message_from_scribe(self, message, participant, scribe_channel, participants_info):
        for action_id, action_conf in self.actions.items():
            if action_id not in ["tweet_received"]:  # todo_es : c'est bof beau..
                if self.participant_has_requested_an_action(action_conf, message, participant):
                    logging.test(10011)
                    answer = "Attention, vous êtes scribe. L'action '%s' n'est donc pas disponible pour vous." \
                             % action_conf['name']
                    await self.conn.send(participant, scribe_channel, answer)
                    return participant
                else:  ###
                    logging.test(10009)
            else:  ###
                logging.test(10010)
        logging.test(10011)

        nb_participants = await self.conn.send_message_to_all_participants(message, participant, participants_info)
        answer = "Comme vous êtes enregistré.e comme scribe, votre message a été transféré à %i participants" \
                 % nb_participants
        await self.conn.send(participant, scribe_channel, answer)

        return participant  # todo_chk : utile ? participant est il updaté à un moment?


    async def analyse_message_from_admin(self, message, participant, channel, participants_info):
        # todo_es : ne pas faire ça, remettre la decription en toutes lettres et détaillée
        error_msg = MESSAGE_NOT_UNDERSTOOD_STR_ADMIN.format(self.admin_actions.keys())
        return await self._analyse_messages_and_take_actions(self.admin_actions, error_msg,  message, participant, channel, participants_info=participants_info)

    async def _analyse_messages_and_take_actions(self, actions, ununderstood_str,  message, participant, channel, participants_info=None):  # todo_es linguee ununderstood
        message_is_understood = False
        for action_name, action_conf in actions.items():
            if self.participant_has_requested_an_action(action_conf, message, participant):
                logging.test(10005)
                message_is_understood = True
                answer = action_conf['answer']
                action_fn = action_conf['action_func']

                logmsg = "ACTION : " + participant.get_normalised_id() + "\t" + message.message_str + "\t" + \
                         action_name  #
                # todo_es: ce message n'est pas très compréhensible
                logging.debug(logmsg)

                if answer is not None:
                    if type(answer) != str:
                        answer = answer(participant, self.conn, message)
                    await self.conn.send(participant, channel, answer, force=True)

                self.conn.save_request_from_participant(message, action_name,
                                                        participant)
                # todo_chk : il y a peut-être plus d'arguments à enregistrer en BDD que ça

                action_fn = sync_to_async(action_fn)
                participant = await action_fn(participant, channel, self.conn, message)

                if 'async_action_func' in action_conf.keys():
                    async_action_fn = action_conf['async_action_func']
                    participant = await async_action_fn(participant, channel, self.conn, message, pi=participants_info)

                if not isinstance(participant, AbstractParticipant):
                    logging.critical(
                        "Attention, dans chaque action de self.actions ou self.admin_actions, la valeur de la clé 'action_func' doit être "
                        "une fonction retournant un participant.")

            else:  ###
                logging.test(10006)

        if not message_is_understood:
            logging.test(10007)
            answer = ununderstood_str
            await self.conn.send(participant, channel, answer, force=True)
        else:  ###
            logging.test(10008)

        return participant
