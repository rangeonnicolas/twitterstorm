import datetime as dt
from settings.advanced_settings import TIMEZONE, LOG_DIR, DATA_DIR, SESSION_LISTENING_LOOP
from settings.advanced_settings import *

###################################################################################################
CAMPAIN_ID = "TwitterStrorm_BF1"

USE_SANDBOX = False

if not USE_SANDBOX:
    DEFAULT_SUGGESTIONS = False                                                  # todo_es : changer le nom de la variable en BDD mais pas ici ;)
    DEFAULT_SUGGESTIONS_FREQUENCY = 1.8                                          # En minutes
else:
    DEFAULT_SUGGESTIONS = True
    DEFAULT_SUGGESTIONS_FREQUENCY = 1.2

END_LISTENING_LOOP = dt.datetime.now(TIMEZONE) + dt.timedelta(0, 60 * 60)        # todo_es a changer

###################################################################################################
import os

env = os.environ.get("TS_ENV_TYPE")
if env is None:
    raise Exception("Variable d'environnement TS_ENV_TYPE indéfinie")
elif env.lower() == "dev":
    ENV_TYPE = "DEV"
    f = 'settings.settings_dev'
    sets = __import__(f).settings_dev
elif env.lower() == "prod":
    ENV_TYPE = "PROD"
    f = 'settings.settings_prod'
    sets = __import__(f).settings_prod
else :
    raise Exception("La valeur de la variable d'environnement est erronée : " + env)
INIT_MSG_TO_LOG = "Importé : " + f

MSG_SUFFIX = sets.MSG_SUFFIX
MIN_TIME_BETWEEN_TWO_ERROR_LOGGINGS = sets.MIN_TIME_BETWEEN_TWO_ERROR_LOGGINGS
###################################################################################################

CLIENT = "Telegram"  # todo_es : variable encore utlisée ?

SANDBOX_MODULE_NAME = 'sandbox_loop'
SEND_ONLY_TO_ME = False

END_SUGGESTION_LOOP = END_LISTENING_LOOP  # todo_es : à merger

NEW_LISTENING_LOOP_ITERATION_EVERY = 2 * 1000  # En milisecondes
CHECK_NEW_PARTICIPANTS_EVERY = 5 * 1000  # En milisecondes
NEW_SUGGESTION_LOOP_ITERATION_EVERY = 4 * 1000  # En milisecondes

TIME_LIMIT_TO_FETCH_PREVIOUS_MSGS = 30 * 60 # En secondes

# todo_es franchement, trouver un autre nom de variable stp
DEFAULT_IS_CAMPAIN_OPEN = False

MIN_SUGGESTION_FREQUENCY = 0.5  # En minutes

DEFAULT_CONSENT = True
DEFAULT_TWEET_VALIDATION = False  # todo_chk useless

# todo_chk réhabiliter ces 2 params?
# Note : en mode SANBOX, ces paramètres ne sont pas pris en compte
# START_SUGGESTIONS = dt.datetime.now(TIMEZONE) # todo_cr mettre à 10h le jour J
# END_SUGGESTIONS = END_LISTENING_LOOP

LOG_DIR = LOG_DIR
DATA_DIR = DATA_DIR
SESSION_LISTENING_LOOP = SESSION_LISTENING_LOOP

###################################################################################################

ROBOT_MSG_SUFFIX = "🤖 : "
ANIMATOR_MSG_SUFFIX = "🗣 : "

# todo_es quite au hack où on ne voulait pas afficher le nom de l'animateurice, merci de remmetre cette ligne :
ANIMATOR_MSG_INTRO = "__**L'un·e des animateurs·ices de la mobilisation vient de t'envoyer un message :**__\n\n"
#ANIMATOR_MSG_INTRO = "__**%s (animateur·ice), vient de t'envoyer un message :**__\n\n" % sender_name !! bien faire attention au sender_name (cf CTRL+F 'intro = s.ANIMATOR_MSG_SUFFIX + s.ANIMATOR_MGS_INTRO % sender_name')


SEND_ONLY_TO_ME_INTRO = "Message initialement destiné à \n{}\n(id={}) :\n\n{}"

URL_SUGGESTION_MSG_STR = ROBOT_MSG_SUFFIX + """Voici un tweet posté par un·e autre activiste (__**{}**__).
[Clique ici]({}) pour l'ouvrir, et si ce tweet te plaît, alors [Like-le]({}) et [Retweete-le]({}) 💪🏼 ! Et si tu est vraiment \
déterminé·e, tu peux même y [répondre][{}] !

Si tu veux que je me taise, envoies-moi '__**STOP**__' 😊 . 
"""

TEXT_SUGGESTION_MSG_STR = ROBOT_MSG_SUFFIX + """Voici un message que tu peux poster en [cliquant ici]({}).

Pour générer à nouveau ce message, mais en ciblant un·e autre député·e, réponds-moi __**AUTRE**__, ou __**STOP**__ \
pour me faire taire 😊.

Pour optimiser nos chances vis-à-vis de l'algorithme de Twitter, l'idéal serait de le poster entre {} et {}.
"""
# todo_es : " mais en ciblant un·e autre député·e" trop spécifique



ACTION_FREQ_MINUTES = "%.2f minutes"
ACTION_FREQ_SECONDS = "%i secondes"
ACTION_FREQ_UPDATE = "Je t'enverrai des suggestions toutes les %s.\n\n__**(Note : Ceci ne vaut que pour les\
 suggestions que je t'envoie automatiquement, par pour les messages des animateur·ice·s 🗣)**__"
ACTION_FREQ_ERROR = "Je n'ai pas compris la fréquence à laquelle je dois t'envoyer les suggestions\nPar exemple : " \
                    "__**FREQ 3**__, " \
                    "ou __**FREQ 0.5**__"

ACTION_ANSWER_STOP = "Tu as demandé à ne plus reçevoir de messages, alors je me tais ;)\n\nSi tu changes " + \
                     "d'avis, réponds __**REPRENDRE**__\n\n(__**Note**__ : Je ne te transfèrerai plus non plus les " + \
                     "messages des animateur·ice·s 🗣)\n\nMerci pour ta participation !"
ACTION_ANSWER_START = "Tu as demandé à reprendre, merci !\n\nSi tu changes d'avis, réponds __**STOP**__ " + \
                      "\n\nMerci pour ta participation !"
ACTION_ANSWER_TWEET_RECEIVED = "Merci pour ton tweet. Il sera suggéré aux autres activistes pour qu'iels le retweetent."
ACTION_ANSWER_REPORT_BUG = "Merci pour ce signalement de bug.\nJe le transmet de ce pas !"
ACTION_ADMIN_OPEN_CAMPAIN = "Tu viens de lancer la campagne ! Les participant·e·s viennent donc de reçevoir le message d'accueil. Pour clôturer la campagne, réponds 'CLOSE'"
ACTION_ADMIN_SANDBOX_ERROR = "[fonction incompatible avec le mode SANDBOX]"
ACTION_ADMIN_CLOSE_CAMPAIN = "Tu viens de clôturer la campagne. Les nouveaux et nouvelles participant·e·s arrivant sur la boucle ne reçevront plus le message d'accueil. Pour réouvrir la campagne, réponds 'OPEN'. Dans ce cas, les participant·e·s ayant déjà reçu le message d'accueil ne le reçevront pas une seconde fois."
ACTION_ADMIN_START_SUGGESTIONS = "Tu viens de lancer les suggestions. Pour les arrêter, réponds 'END SUGGESTIONS'"
ACTION_ADMIN_END_SUGGESTIONS = "Tu viens de stopper les suggestions. Pour les relancer, réponds 'START SUGGESTIONS'"
ACTION_ADMIN_RAISE_EXCEPTION = "Tu viens de lever une exception dans le programme. Attention c'est dangereux !"


if not USE_SANDBOX:
    # todo_es : pas à la bonne place
    invite_link = "https://t.me/joinchat/I-xqAEUulztdUOz-RTsOdQ"
    animateurices = ""
    boucle = '🛒 surprod - comm Interpellation'
    debut_str = '__**Vendredi 27 nov à 10h**__'
else:
    invite_link = "https://t.me/joinchat/I-xqAEUulztdUOz-RTsOdQ"                  # todo_es : pas vraiment le bon lien
    animateurices = "(__**Johanna et Matthieu**__)"
    boucle = '[DEMO] 🛒 surprod - comm Interpellation'
    debut_str = "dans :\n__**2MINUTES**__"



MESSAGE_NOT_UNDERSTOOD_STR = \
    ROBOT_MSG_SUFFIX + """Désolé, je n'ai pas compris ton message.

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
""".format(boucle)


MESSAGE_NOT_UNDERSTOOD_STR_ADMIN = "Bon sérieux mec, j'ai pas pigé ton message. Voici les actions possibles : {}"

SCRIBE_ACTION_ERROR = "Attention, vous êtes scribe. L'action '%s' n'est donc pas disponible pour vous."
SCRIBE_FORWARDED_MESSAGE = "Comme vous êtes enregistré.e comme scribe, votre message a été transféré à %i participants"









# Pour les messages suivants, mettre une liste vide si pas de message à envoyer
WELCOME_SCRIBE_MSGS = ["Salut Scribe!"]
WELCOME_NEW_PARTICIPANT_MSGS = ["""
[🛒 surprod - comm Interpellation]

Bonjour ! 
Merci de participer à l'action d'interpellation contre Amazon. 😍

Tu reçois ce message car tu es inscrit·e dans la boucle __**'{}'**__.
Cette boucle est destinée aux informations générales de la mobilisation d'interpellation qui commence {}.\

Cependant, cette boucle contient beaucoup d'activisites, et il n'est pas toujours pratique de suivre tous les 
messages qui \
y passent ! 😱
Ainsi, pour que tu puisses te concentrer sur les informations importantes, nous utiliserons en plus de cette grosse \
boucle, une boucle privée.
Cette boucle privée, c'est celle dans laquelle tu es en train de lire ce message. Dans cette boucle, il n'y a que toi \
et moi. 😊

Mais moi, je suis qui au fait ?

Je suis un programme informatique (un robot ! 🤖), et j'ai 3 rôles :
👉🏼 Te transférer les instructions importantes des animateur·ices de la mobilisation {}. 
👉🏼 Te suggérer des textes que tu pourra copier pour les poster sur twitter. 
👉🏼 Te suggérer des tweets postés par d'autres activistes pour que tu les Like et les Retweete.

👉🏼 De ton côté, je t'invite à m'envoyer les URL des tweets que tu as postés, afin que je les propose aux 
autres activistes de la boucle. Je suis spécialement entraîné à reconnaître les URL des tweets (de type 
https://twitter.com/pseudo/status/13297...), je saurai donc les détecter dans les messages que tu m'enverras ici 
😊.

Allez, ensemble on va saturer twitter, et mettre la pression à Amazon !!! 💪🏼""".format(
    boucle, debut_str, animateurices),
    """Ah oui, une dernière chose :

👉🏼 Si tu n'es plus disponible pour cette mob, envoies-moi __**STOP**__, et je me taierai.
👉🏼 Si je suis trop bavard, envoies __**FREQ 1**__, en remplaçant __**1**__ par le nombre de minutes desquelles 
tu veux que j'espace mes messages. Par exemple, avec __**FREQ 60**__, je ne t'enverrai des messages qu'une fois par 
heure.
👉🏼 Si tu détectes un bug de mon fonctionnement, envoies-moi __**BUG**__ suivi de la description du problème, 
ça aidera les informaticien·ne·s qui m'ont donné naissance !"""]
GOODBYE_SCRIBE_MSGS = ["Au revoir Scribe!"]
GOODBYE_PARTICIPANT_MSGS = [
    ROBOT_MSG_SUFFIX + """Tu es sorti·e de la boucle d'interpellation. Je ne t'enverrai donc plus de message. 😊\nSi tu souhaites y  
revenir plus tard, voici le lien : {}""".format(
        invite_link)]

depute_e_s = ["@S_Trompille",
              "@AudeBono",
              "@MarcDelatte",
              "@B_Peyrol",
              "@CCastaner",
              "@LoicDombreval",
              "@CedricRoussel06",
              "@A_Ardisson",
              "@GBessonMoreau",
              "@PereaAlain",
              "@MRobert_11",
              "@AnneBlanc_12",
              "@S_Mazars",
              "@ThierryMichels",
              "@VincentThiebaut",
              "@saidahamada",
              "@ALouisDeputee13",
              "@MonicaMichel_Of",
              "@al_petel",
              "@ClairePitollat",
              "@RaconCathy",
              "@BertrandBouyx",
              "@LeVigoureuxF",
              "@AlainTourret",
              "@MARSAUDSandra",
              "@MESNIERThomas",
              "@jean_ardouin",
              "@RaphaelGerard17",
              "@FCBDeputeduCher",
              "@LoicKervran18",
              "@KhattabiF",
              "@dmartindijon",
              "@_DidierParis",
              "@HerveBerville",
              "@ebothorel",
              "@Kerlogot22",
              "@moreaujb23",
              "@JeanMarieFIEVET",
              "@ChassaingPh",
              "@MichelDelpon",
              "@Jacqlinedubois",
              "@ericalauzet",
              "@Fred_Barbier",
              "@F_Charvier",
              "@DenisSommer",
              "@CLAPOTMireille",
              "@CdLavergne",
              "@AliceThourot",
              "@StephanieAtger",
              "@fchouat",
              "@mguevenoux",
              "@p_a_raphan",
              "@RixainMP",
              "@Romeiro1L",
              "@severine_gipson",
              "@FGouttefarde",
              "@claireopetit",
              "@BQuestel",
              "@marietamarelle",
              "@guillaumekasba",
              "@RichardFerrand",
              "@SandrineLeFeur",
              "@didierlegac",
              "@AnnaigLeMeur_AN",
              "@GrazieMelchior",
              "@LilianeTanguyAN",
              "@PA_Anglade",
              "@scazebonne",
              "@AGenetet",
              "@alexIholroyd",
              "@Amelia_LKF",
              "@RolandLescure",
              "@anthonycellier",
              "@fdumasdeputee",
              "@jrcazeneuve",
              "@florent_boudie",
              "@BCouillard33",
              "@DominiqueDavid_",
              "@duboschristelle",
              "@cfabreAN",
              "@V_Hammerer",
              "@SoPanonacle",
              "@BenoitSimian",
              "@olivier_serva",
              "@LenaickADAM",
              "@DeputeCabareP",
              "@MoniqueIborra",
              "@SandrineMorch",
              "@MickaelNogal",
              "@jfportarrieu",
              "@etoututpicard",
              "@corinnevignon",
              "@sylv1templier",
              "@B_BessotBallot",
              "@lejeune_ch",
              "@F_Lardet",
              "@marion_lenne",
              "@V_Riotton",
              "@XavierRoseren",
              "@BeaudouinSo",
              "@MarieAngeMagne",
              "@PierreVenteau",
              "@ClaireBouchet05",
              "@pascaleboyer05",
              "@celinecalvez",
              "@Ch_Hennion",
              "@JMaireofficiel",
              "@jmarilossian",
              "@DeputeeBPetelle",
              "@flprovendier",
              "@solere92",
              "@DemoulinEM",
              "@CoDubost",
              "@JFEliaou",
              "@MIRALLESMP",
              "@F_BACHELIER",
              "@ChrisCloarec",
              "@mustapha_laabid",
              "@GaelLeBohec",
              "@LMaillart",
              "@FJolivet36",
              "@Chalumeau_P",
              "@fabiennecolboc",
              "@LabaronneDaniel",
              "@AbadieCaroline",
              "@EmilieCChalas",
              "@JCColasRoy",
              "@GalliardM",
              "@CKamowski3805",
              "@3807Limon",
              "@M_MeynierM",
              "@dbrulebois",
              "@DeputeCausse",
              "@JulienBorowczyk",
              "@V_Faure_Muntian",
              "@AudeAmadou",
              "@ydaniel_depute",
              "@FdeRugy",
              "@audreydufeu",
              "@SophieErrante",
              "@YHaury44",
              "@valerie_oppelt",
              "@CarolineJanvier",
              "@stephanie_rist",
              "@AVFreschi",
              "@lauzzanamichel",
              "@NicoleDubre17",
              "@stelladupont",
              "@denis_Masseglia",
              "@l_saintpaul",
              "@BertrandSorre",
              "@StTRAVERT",
              "@GirardinEric",
              "@RamlatiAli",
              "@CGrandjean54",
              "@XavierPalu2017",
              "@J_M_Jacques",
              "@NicoleLePeih",
              "@HervePellois",
              "@G_ROUILLARD",
              "@christophearend",
              "@b_belhaddad",
              "@RichardLioger",
              "@ludovicMDS",
              "@IsabelleRauch",
              "@NicoleTrisse",
              "@HeleneZannier",
              "@ALCattelot",
              "@DipompeoChrist",
              "@lecocqcharlotte",
              "@brigitte_liso",
              "@FMorlighem",
              "@OssonCatherine",
              "@PascalBoisLaREM",
              "@CaroleBBonnard",
              "@LaetitiaAvia",
              "@BGriveaux",
              "@StanGuerini",
              "@AChristine_Lang",
              "@GillesLeGendre",
              "@SylvainMaillard",
              "@Pierr_Person",
              "@huguesrenson",
              "@PacomeRupin",
              "@mariesilin",
              "@BuonTAN",
              "@JMaquetDeputee",
              "@JeanPierrePont",
              "@Vthomas_63",
              "@SCazenove",
              "@LaurenceGayte",
              "@yves_blein",
              "@BrunoBonnellOff",
              "@AnneBrugnera",
              "@Anissa_Khedher",
              "@trudigoz",
              "@sclaireaux",
              "@BenjaminDirx",
              "@Gauvain_Raphael",
              "@RRebeyrotte",
              "@DamienPichereau",
              "@Typhanie_Degois",
              "@DoStephanie_77",
              "@RKokouendoJ",
              "@MichelePeyron",
              "@damienadam76",
              "@XavierBatut",
              "@SKerbarh",
              "@sirasylla76",
              "@Vidal7602",
              "@Patrice_Anato",
              "@SylvieCharriere",
              "@stephane_teste",
              "@C_Delpirou",
              "@JLeclabart",
              "@philippefolliot",
              "@JeanTerlier",
              "@VerdierJouclas",
              "@DDaSilva95",
              "@NaimaMoutchou",
              "@zivkapark",
              "@Cecile_Rilhac",
              "@g_vuilletet",
              "@jjbridey94260",
              "@fdescrozaille",
              "@JFMBAYE",
              "@LauStmartin",
              "@VGB83",
              "@eguerelLREM",
              "@famatras",
              "@SereineEnMarche",
              "@cecile_muschotti",
              "@brunepoirson",
              "@ZITOUNISouad3",
              "@StephaneBuchou",
              "@HenrietPierre",
              "@LeguilleBalloy",
              "@fballetblu",
              "@SachaHoulie",
              "@dbaichere",
              "@auroreberge",
              "@YaelBRAUNPIVET",
              "@fgranjus",
              "@MarieLebec78",
              "@BeatricePiron",
              "@npouzyreff78"]

TWEET_TEXTS = {
    "tweet_1": [""".""", depute_e_s,
                """, alors que @EmmanuelMacron contribue à la disparition des petits commerces en laissant carte 
                blanche à Amazon, nous comptons sur vous pour porter le moratoire sur les entrepôts de e-commerce à 
                l'AN lors du projet de loi CCC.\n#AmazonMacronComplice #StopAmazon"""],
    "tweet_2": ["""Bonjour """, depute_e_s, """
, @EmmanuelMacron ne compte pas stopper l'installation d'Amazon en 🇫🇷 qui va détruire pourtant 100 000 emplois. 
Soutiendrez-vous le moratoire sur les entrepôts de e-commerce lors du passage à l'AN de la loi CCC 
?\n#AmazonMacronComplice #StopAmazon"""],
    "tweet_3": [
        """On ne peut pas compter sur @EmmanuelMacron pour arrêter l'expansion d'Amazon en 🇫🇷 qui signe la mort des 
        petits commerces. """,
        depute_e_s, """
 : aurez-vous le courage de vous y opposer? Soutenez le moratoire sur les entrepôts e-commerce dans le PJL 
 CCC\n#AmazonMacronComplice #StopAmazon"""],
    "tweet_4": ["""Bonjour """, depute_e_s, """
 : protéger les petits commerçants demande du courage. @EmmanuelMacron ne l'a pas. Vous devez soutenir le moratoire 
 sur les entrepôts de e-commerce lors du projet de loi CCC.\n#StopAmazon : 1 emploi créé, 4,5 emplois 
 supprimés.\n#AmazonMacronComplice"""],
    "tweet_5": ["""Bonjour  """, depute_e_s, """
 : protégez les petits commerces 🇫🇷 : soutenez le moratoire sur les entrepôts de e-commerce lors du projet de loi 
 CCC. Stop au massacre.\nAmazon c'est 1 emploi créé pour 4,5 emplois détruits.\n#AmazonMacronComplice #StopAmazon"""],
    "tweet_6": [
        """Alors qu'@EmmanuelMacron continue d'accueillir Amazon à bras ouverts, pourtant fossoyeur des petits 
        commerces en 🇫🇷 (100 000 emplois seront détruits en 2021), """,
        depute_e_s, """
_AN soutenez le moratoire sur les entrepôts de e-commerce !\n#AmazonMacronComplice #StopAmazon"""],
    "tweet_7": ["""Bonjour """, depute_e_s, """
. Je m'inquiète pour l'économie 🇫🇷 car @EmmanuelMacron ne freine pas l'implantation d'Amazon qui détruit les petits 
commerces (1 emploi créé pour 4,5 supprimés). Vous devez soutenir le moratoire sur les entrepôts de 
e-commerce\n#AmazonMacronComplice #StopAmazon"""],
    "tweet_8": [""".""", depute_e_s, """
, @EmmanuelMacron donne carte blanche à l'implantation d'@Amazon en France alors qu'il sait que cela va engendrer 
près de 100 000 destructions d'emplois. Serez-vous complice de cette catastrophe ? #AmazonMacronComplice 
#StopAmazon"""],
    "tweet_9": ["""Bonjour """, depute_e_s, """
, vous soutenez les commerçant·es de proximité ? Si oui, ayez le courage de dire #StopAmazon face à l'entêtement 
d'@EmmanuelMacron\n#AmazonMacronComplice"""],
    "tweet_10": ["""Bonjour """, depute_e_s, """
, votre majorité @LaREM_AN mène les commerçant·es vers des faillites en cascade en autorisant l'implantation massive 
d'#Amazon en 🇫🇷, qui va détruire 100 000 emplois. Si vous ne voulez pas être responsable de cette catastrophe, 
dites #StopAmazon"""],
    "tweet_11": ["""Bonjour """, depute_e_s, """
 , dire oui à l'implantation d'#Amazon aujourd'hui en 🇫🇷, c'est signer la mort des commerces de proximité et la 
 destruction de 100 000 emplois\nVous assumez cette politique pro #JeffBezos en pleine crise économique 
 ?\n#AmazonMacronComplice #StopAmazon"""],
    "tweet_12": ["""Bonjour """, depute_e_s, """
, visiblement @EmmanuelMacron préfère #Amazon aux petits commerçant·es puisqu'il soutient l'implantation massive de 
la multinationale en 🇫🇷. Et vous, êtes-vous ok pour sacrifier 100 000 emplois pour plaire à Jeff Bezos ? 
#StopAmazon"""],
    "tweet_13": ["""Bonjour """, depute_e_s, """
, les petits commerçants ont besoin de vous. Déjà à terre à cause du #coronavirus, ils ne se relèveront pas si vous ne vous opposez pas à l'implantation d'#Amazon en France. Ayez le courage de les défendre !\n#AmazonMacronComplice #StopAmazon"""],
}
