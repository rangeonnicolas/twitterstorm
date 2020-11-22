from asgiref.sync import sync_to_async

from daemon_loops.modules.telegram import TelegramParticipant
from daemon_loops.settings import END_LISTENING_LOOP, TIMEZONE, CAMPAIN_ID
import datetime as dt

NEW_SANDBOX_LOOP_ITERATION_EVERY = 20 * 1000
END_SANDBOX_LOOP = END_LISTENING_LOOP
MESSAGE_EXPIRATION = 2 * 60  # En secondes. Définit le délai au dlà duquel il esyt trop tard pour envoyer un planned message

PLANNED_MESSAGES = {
    "pm_1": {
        'seconds_after_participant_arrival_in_loop': 2, # todo : remetre à 2*60
        'sender': "Matthieu",
        'msg': """J'ai lancé le [thread du compte Amis de la Terre](https://twitter.com/amisdelaterre/status/1326088376106311682) , vont venir aussi des thread sur les comptes \
ANV et ACtion Climat Paris ! Vous pouvez RT et tweeter !"""},
    "pm_2": {
        'seconds_after_participant_arrival_in_loop': 3 * 60,
        'sender': "Johanna",
        'msg': """3 mots en TT à utiliser massivement pour devenir viral :
👉 Amazon 
👉 #MardiConseil
👉 #TousContreMacronJour43

Amusez-vous ! 😸"""},
    "pm_3": {
        'seconds_after_participant_arrival_in_loop': 4 * 60,
        'sender': "Matthieu",
        'msg': """Voici le tweet acp : https://twitter.com/actionclimat75/status/1326090258438643712, 
à relayer massivement !"""},
    "pm_4": {
        'seconds_after_participant_arrival_in_loop': 6 * 60,
        'sender': "Johanna",
        'msg': """#AmazonMacronComplice en TT : 5ème place !! 

On assure grave ! 

On lâche rien !"""},
    "pm_5": {
        'seconds_after_participant_arrival_in_loop': 9 * 60,
        'sender': "Johanna",
        'msg': """Pour celles et ceux qui ont encore le temps, on continue ! Le #AmazonMacronComplice est toujours 
en trending topics !"""},
    "pm_6": {
        'seconds_after_participant_arrival_in_loop': 12 * 60,
        'sender': "Johanna",
        'msg': """Déjà 1359 tweets avec le #AmazonMacronComplice, toujours en TT sur Twitter, bravo🙌👏 ! Encore 
plein de député·es (https://docs.google.com/spreadsheets/d/14hlESe13pL_AoF0_DSyIWo9-OebnG28i1FODEiaH310/edit#gid=0) 
n'ont pas eu leur petit tweet. Il ne faut pas les lâcher et les mettre devant leurs responsabilités 
!"""},
    "pm_7": {
        'seconds_after_participant_arrival_in_loop': 17 * 60,
        'sender': "Johanna",
        'msg': """Un grand MERCI à toutes et tous pour votre détermination ce matin ! 🔥🔥On a encore fait pas mal de 
bruit et vos punchlines nous ont fait rêver 🤩 

Pour celles et ceux qui ont loupé le train ce matin, il est toujours possible de continuer ce midi avec #StopAmazon 
et #AmazonMacronComplice ! N'hésitez pas à utiliser au max les ressources à votre dispositions : chiffres clés, 
memes, visuels ...

La journée n'est pas finie : à partir de 14h nous allons lancer cet outil d'interpellation qui permet d'envoyer un 
mail aux député.e.s de son choix. 

À relayer sur vos RS respectifs. 

Pour participer, il faut 
- cliquer sur ce lien : 
https://www.stop-amazon.fr/StopAmazon-interpellez-un-e-depute-e
- sélectionner un ou des députés en choisissant un département puis quel(s) député on veut contacter. (on peut bien 
sûr renouveler avec un autre département)
- renseigner son nom, prénom, mail
- cocher les cases et envoyer
- pour finaliser votre envoi il faudra ensuite confirmer votre action en ouvrant votre boîte mail.

N'hésitez pas s'il y a des choses pas claires"""}
}




from django.db import models

class SentPlannedMessage(models.Model):
    campain_id = models.CharField(max_length=50)
    planned_message_id = models.CharField(max_length=50)
    sent_at = models.DateTimeField()
    receiver_id = models.CharField(max_length=50)  # todo : a transformer en foreign key quand on pourra
    sent_text = models.TextField()


class SandboxParticipant(TelegramParticipant):
    def __init__(self, p):
        TelegramParticipant.from_pair(self, p)

    async def check_for_planned_message(self, now, msgs):
        to_send = []

        for message_id, message_data in msgs.items():

            delta = dt.timedelta(0,message_data['seconds_after_participant_arrival_in_loop'])
            sender = message_data['sender']
            message_txt = message_data['msg']

            when_to_send_the_message = self.last_arrival_in_channel + delta
            it_is_a_bit_too_late_to_send_it = when_to_send_the_message + dt.timedelta(0, MESSAGE_EXPIRATION)

            if when_to_send_the_message < now and now < it_is_a_bit_too_late_to_send_it:
                if not await self._check_if_already_sent(message_id):  # todo : attention à bien checker qu'il a déjà été envoyé APRES le last_arrival, car il a peut etre été envoyé avant, puis il est parti de la boucle puis revenu :)
                    message = "__**%s (animateur·ice de la mobilisation), vient de t'envoyer un message :**__\n\n%s" % (sender, message_txt)
                    to_send.append({
                        'msg_id' : message_id,
                        'message' : message,
                    })

        return to_send

    @sync_to_async
    def _check_if_already_sent(self, message_id):
        print(22)
        objs = SentPlannedMessage.objects.filter(
            campain_id = CAMPAIN_ID,
            receiver_id=self.get_normalised_id(),
            planned_message_id=message_id,
            sent_at__gte=self.last_arrival_in_channel
        )
        print(objs)
        return len(objs) >= 1

    @sync_to_async
    def record_planned_message(self, m):  # todo : cette méthode devrait plutot etre dans la classe sandbox_connection (les autres aussi?)
        SentPlannedMessage(
            campain_id = CAMPAIN_ID,
            planned_message_id = m['msg_id'],
            sent_at = dt.datetime.now(TIMEZONE),
            receiver_id = self.get_normalised_id(),  # todo : a transformer en foreign key quand on pourra
            sent_text = m['message']
        ).save()