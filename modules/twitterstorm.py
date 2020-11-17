import os

import settings as s
from modules.logger import Logger

logger = Logger()


class TwitterstormError(Exception):  # todo : arevoir
    def __init__(self, message, prefix="- ERREUR :  "):
        os.system('cls')  # Windows
        os.system('clear')  # Linux, Mac
        super().__init__(message)
        print("\n\n")  # todo
        print(prefix + message)
        print("\n" * 10 + "Aide au debuggage :\n")
        logger.test(10000)


class TwitterstormSettingsError(TwitterstormError):  # todo: a exploiter
    def __init__(self, message, file):
        logger.test(10001)
        super().__init__(message, prefix="- ERREUR DANS LE FICHIER DE CONFIGURATION '{}.py':  ".format(file.__name__))


def init():  # todo: affiahcer tout le chargement des données
    # todo: envoyer une message au scribe pour lui dire de pas faire de la merde
    # todo: vérifier aussi, en cas de relancement d el'appli après plantage, qu'il n'y a pas d'actions
    # en attente (ex: le scribe a un message qu'il n'a pas validé)
    for dir_ in [s.DATA_DIR, s.LOG_DIR, s.SESSION_DIR]:
        if not os.path.exists(dir_):
            os.makedirs(dir_)
            logger.test(10002)


class MessageAnalyser:
    def __init__(self, conn, actions):
        self.actions = actions
        self.conn = conn
        logger.test(10003)

    @staticmethod
    def participant_has_requested_an_action(action_conf, m, participant):
        fn = action_conf['test_func']
        logger.test(10004)
        return fn(m.message_str, participant.get_normalised_id())

    async def analyse_message_from_normal_participant(self, message, participant, channel):
        message_is_understood = False
        for action_name, action_conf in self.actions.items():
            if self.participant_has_requested_an_action(action_conf, message, participant):
                logger.test(10005)
                message_is_understood = True
                answer = action_conf['answer']
                action_fn = action_conf['action_func']

                logmsg = "ACTION : " + participant.get_normalised_id() + "\t" + message.message_str + "\t" + \
                         action_name  #
                # todo: ce message n'est pas très compréhensible
                logger.debug(logmsg)

                await self.conn.send(participant, channel, answer)
                self.conn.save_request_from_participant(message, action_name,
                                                        participant)  # todo: il y a peut-être plus d'arguments à
                # todo : enregistrer en BDD que ça

                participant = action_fn(participant, self.conn, message)
            else:  ###
                logger.test(10006)

        if not message_is_understood:
            logger.test(10007)
            # todo  : désolé, je n'ai pas compris votre message !
        else:  ###
            logger.test(10008)

        return participant

    async def analyse_message_from_scribe(self, message, participant, scribe_channel, participants_info):
        for action_name, action_conf in self.actions.items():
            if action_name not in ["tweet_received"]:  # todo : c'est bof beau..
                if self.participant_has_requested_an_action(action_conf, message,
                                                            participant):  # todo: méthode statique, ça marche avec
                    logger.test(10011)
                    # todo : self ou pas? Si oui tut corriger
                    answer = "Attention, vous êtes scribe. L'action '%s' n'est donc pas disponible pour vous." \
                             % action_name  # todo : faire attention à ce que action_name soit compréhensible par le
                    # scribe... :s
                    await self.conn.send(participant, scribe_channel, answer)
                    return participant
                else:  ###
                    logger.test(10009)
            else:  ###
                logger.test(10010)
        logger.test(10011)
        nb_participants = self.conn.send_message_to_all_participants(message, participant, participants_info)
        answer = "Comme vous êtes enregistré.e comme scribe, votre message a été transféré à %i participants" \
                 % nb_participants
        await self.conn.send(participant, scribe_channel, answer)
        # todo : on ne emanderait pas une validation par hasard? Avec un système de message en attente et 2 min pour
        # confirmer avec le mot clé "#banlancelasauce"
        # Si 2 messages ont été soumis en moins de 2 minutes, bien préciser à la recetion
        # du 2nd message que le précédent est annulé ;)

        return participant  # todo : utile ? participant est il updaté à un moment?
