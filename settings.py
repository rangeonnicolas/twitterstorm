import os

env = os.environ.get("TS_ENV_TYPE")
if env is None:
    raise Exception("Variable d'environnement TS_ENV_TYPE indéfinie")
elif env.lower() == "dev":
    ENV_TYPE = "DEV"
    f = 'settings_dev'
    sets = __import__(f)
elif env.lower() == "prod":
    ENV_TYPE = "PROD"
    f = 'settings_prod'
    sets = __import__(f)
else :
    raise Exception("La valeur de la variable d'environnement est erronée : " + env)
INIT_MSG_TO_LOG = "Importé : " + f

MSG_SUFFIX = sets.MSG_SUFFIX
MIN_TIME_BETWEEN_TWO_ERROR_LOGGINGS = sets.MIN_TIME_BETWEEN_TWO_ERROR_LOGGINGS






import datetime as dt
from daemon_loops.modules.advanced_settings import *  # todo_es utiliser une autre méthode
from daemon_loops.modules.advanced_settings import TIMEZONE

CLIENT = "Telegram"  # todo_es : variable encore utlisée ?

CAMPAIN_ID = "TwitterStrorm_2"

USE_SANDBOX = True  # todo_cr
SANDBOX_MODULE_NAME = 'sandbox_loop'

NEW_LISTENING_LOOP_ITERATION_EVERY = 2 * 1000  # En milisecondes
CHECK_NEW_PARTICIPANTS_EVERY = 5 * 1000  # En milisecondes
NEW_SUGGESTION_LOOP_ITERATION_EVERY = 4 * 1000  # En milisecondes

TIME_LIMIT_TO_FETCH_MSGS = 30 * 60 # En secondes



# todo_es : changer le nom de la variable en BDD mais pas ici ;)
DEFAULT_SUGGESTIONS = False if dt.datetime.now() < dt.datetime(2020,11,27,10,15) else True # détermine s'il faut envoyer les suggestions dès le lancement du programme (sans attendre la 'START' de l'admin
# todo_es franchement, trouver un autre nom de variable stp
DEFAULT_IS_CAMPAIN_OPEN = False

DEFAULT_SUGGESTIONS_FREQUENCY = 1.2  # En minutes
MIN_SUGGESTION_FREQUENCY = 0.5  # En minutes

DEFAULT_CONSENT = True
DEFAULT_TWEET_VALIDATION = False  # todo_chk useless

SEND_ONLY_TO_ME = False

# END_LISTENING_LOOP = dt.datetime(2020,5,24,8,0,0,tzinfo=s.TIMEZONE)
END_LISTENING_LOOP = dt.datetime.now(TIMEZONE) + dt.timedelta(0, 60 * 60)  # todo_cr a changer
END_SUGGESTION_LOOP = END_LISTENING_LOOP  # todo_es : à merger

# todo_chk réhabiliter ces 2 params?
# note : en mode sandbox, ces paramètres ne sont pas pris en compte
#START_SUGGESTIONS = dt.datetime.now(TIMEZONE) # todo_cr mettre à 10h le jour J
#END_SUGGESTIONS = END_LISTENING_LOOP

ROBOT_MSG_SUFFIX = "🤖 : "
ANIMATOR_MSG_SUFFIX = "🗣 : "

URL_SUGGESTION_MSG_STR = ROBOT_MSG_SUFFIX + """Voici un tweet posté par un·e autre activiste (__**{}**__).

[Clique ici]({}) pour l'ouvrir, et si ce tweet te plaît, alors Like-le et Retweete-le 💪🏼 !

Si tu veux que je me taise, envoies-moi '__**STOP**__' 😊 . 
"""

TEXT_SUGGESTION_MSG_STR = ROBOT_MSG_SUFFIX + """Voici un message que tu peux copier-coller dans un tweet.

Pour générer à nouveau ce message, mais en ciblant un·e autre député·e, réponds-moi __**AUTRE**__.
"""

# todo_es : pas à la bonne place
invite_link = "https://t.me/joinchat/I-xqAEUulztdUOz-RTsOdQ"
animateurices = "Johanna et Matthieu"
boucle = '[DEMO] 🛒 surprod - comm Interpellation'

# Pour les messages suivants, mettre une liste vide si pas de message à envoyer
WELCOME_SCRIBE_MSGS = ["Salut Scribe!"]
WELCOME_NEW_PARTICIPANT_MSGS = ["""
[🛒 surprod - comm Interpellation]

Bonjour ! 
Merci de participer à l'action d'interpellation contre Amazon. 😍

Tu reçois ce message car tu es inscrit.e dans la boucle __**'{}'**__.
Cette boucle est destinée aux informations générales de la mobilisation d'interpellation qui commence dans :\n__**2 \
MINUTES**__

Cependant, cette boucle contient beaucoup d'activisites, et il n'est pas toujours pratique de suivre tous les 
messages qui \ 
y passent ! 😱
Ainsi, pour que tu puisses te concentrer sur les informations importantes, nous utiliserons en plus de cette grosse \
boucle, une boucle privée.
Cette boucle privée, c'est celle dans laquelle tu es en train de lire ce message. Dans cette boucle, il n'y a que toi \
et moi. 😊

Mais moi, je suis qui au fait ?

Je suis un programme informatique (un robot ! 🤖), et j'ai 3 rôles :
👉🏼 Te transférer les instructions importantes des animateur.ice.s de la mobilisation (__**{}**__). 
👉🏼 Te suggérer des textes que tu pourra copier pour les poster sur twitter. 
👉🏼 Te suggérer des tweets postés par d'autres activistes pour que tu les Like et les Retweete.

👉🏼 De ton côté, je t'invite à m'envoyer les URL des tweets que tu as postés, afin que je les propose aux 
autres activistes de la boucle. Je suis spécialement entraîné à reconnaître les URL des tweets (de type 
https://twitter.com/pseudo/status/13297...), je saurai donc les détecter dans les messages que tu m'enverras ici 
😊.

Allez, ensemble on va saturer twitter, et mettre la pression à Amazon !!! 💪🏼""".format(
    boucle, animateurices),
    """Ah oui, une dernière chose :

👉🏼 Si tu n'es plus disponible pour cette mob, envoies-moi __**STOP**__, et je me taierai.
👉🏼 Si je suis trop bavard, envoies __**FREQ 1**__, en remplaçant __**1**__ par le nombre de minutes desquelles 
tu veux que j'espace mes messages. Par exemple, avec __**FREQ 60**__, je ne t'enverrai des messages qu'une fois par 
heure.
👉🏼 Si tu détectes un bug de mon fonctionnement, envoies-moi __**BUG**__ suivi de la description du problème, 
ça aidera les informaticien.ne.s qui m'ont donné naissance !"""]
GOODBYE_SCRIBE_MSGS = ["Au revoir Scribe!"]
GOODBYE_PARTICIPANT_MSGS = [
    ROBOT_MSG_SUFFIX + """Tu es sorti.e de la boucle d'interpellation. Je ne t'enverrai donc plus de message. 😊\nSi tu souhaites y  
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
