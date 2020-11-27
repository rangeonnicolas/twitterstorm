from settings.settings import END_LISTENING_LOOP
import datetime as dt

DEBUT = 1.5 * 60  # en secondes

NEW_SANDBOX_LOOP_ITERATION_EVERY = 20 * 1000

END_SANDBOX_LOOP = END_LISTENING_LOOP

MESSAGE_EXPIRATION = 2 * 60  # En secondes. Définit le délai au dlà duquel il esyt trop tard pour envoyer un planned
# message # todo_es linguee expiratipn (expiry?)

TIME_BEFORE_SUGGESTING = dt.timedelta(0, DEBUT + 60)

ANIMATOR_MSG_INTRO = "__**%s (animateur·ice de la mob.), vient de t'envoyer un message :**__\n\n%s"

orig_tweets = ["https://twitter.com/VignonVirginie/status/1329722635572416512",
               "https://twitter.com/fredjoz/status/1329712809307942912",
               "https://twitter.com/alma_dufour/status/1329718727256977408",
               "https://twitter.com/attac_fr/status/1329724618945523713",
               "https://twitter.com/MarseilleAnv/status/1329717239579336734",
               "https://twitter.com/ElodieNace/status/1329726146406215680",
               "https://twitter.com/CharlieFleurene/status/1329477205949353989",
               "https://twitter.com/fredjoz/status/1329712809307942912",
               "https://twitter.com/CruzPcruz62/status/1329714776390447105"]


PLANNED_MESSAGES = {
    "pm_1": {
        'seconds_after_participant_arrival_in_loop': DEBUT,
        'sender': "Matthieu",
        'msg': """🔥🔥 C'EST PARTI !!! 🔥🔥 \

Je viens de lancer le \
[thread du compte Amis de la Terre](https://twitter.com/amisdelaterre/status/1326088376106311682) , \
vont venir aussi des thread sur les comptes \
ANV et Action Climat Paris ! Vous pouvez RT et tweeter !"""},
    "pm_2": {
        'seconds_after_participant_arrival_in_loop': 3 * 60,
        'sender': "Johanna",
        'msg': """3 mots en TT à utiliser massivement pour devenir viral :
👉 Amazon 
👉 #MardiConseil
👉 #TousContreMacronJour43

Amusez-vous ! 😸"""},
    "pm_3": {
        'seconds_after_participant_arrival_in_loop': DEBUT + 20,
        'sender': "Matthieu",
        'msg': """Voici le tweet acp : https://twitter.com/actionclimat75/status/1326090258438643712, 
à relayer massivement !"""},
    "pm_4": {
        'seconds_after_participant_arrival_in_loop': 6 * 60,
        'sender': "Johanna",
        'msg': """#AmazonMacronComplice en TT : 5ème place !! 
🤩 On assure grave ! 🤩
🔥 On lâche rien ! 🔥"""},
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
mail aux député·e·s de son choix. 

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
