# Todo
## Features
### Critique
### Important
- fonction de suppression des trucs innutiles dans la BDD
- enregistrement des clics de postage
- updater en temps rééel le frequences
- clic to tweet
- analyse des perfs : logs à supprimer, BDD

### Intéressant
- tests
- leur proposer d'envoyer un debrioef? ('Bug / Avis')
- enregistrer les bugs ;)
- pinage de 1message récap

## wording
- On essaie de tenir jusque, de manière régulière

## rapide
- gitter les fichiers config
x TwitterWatch fonctionne t'il tjrs ?
- !! detecter les mauvaises urls ! postées par les participants au robot
- CHECK peut on piner un message
- todo : n'accepter qu'un message a la fois (ex : bug https://twitter.com/actionclimat75/status/1326090258438643712 lol)
- TW a 'til des logs chiants ? une grosse BDD?'
- créer des users TG

## Fiabilité
- 3 boucles séparées

## Performance
- Passer la sqlite3 en Django
- vider la BDD + suppression de doublons innutiles
- todo_op
- normalisation des urls des tweets pour éviter les doublons + vérification de doublon avat d'insérer dans la BDD

# Tâches jour J
## H = 0
- LANCER LES SUGGESTIONS ;) (start suggestions / end suggestions)
- remplir rapidement la BDD avec les tweets
- transférer le message de lancement

## En continu
- trnasférer les messages des animateur.ices EN SIGNANT A LA FIN !!!!
- logs des boucles : `tail -f daemon_loops/data/log/log`
- savoir quand descendre la frequence + le notifier

## Data 
- sauvegarder BDD
- supprimer logs
- vider BDD
- espace disque sur le serveur

## Monitoring
- cf monitoring
- exceptions levées / excpetion de flow
- tester l'envoi de message à partir du compte act. LAMBDA

## Sur Twitter
- surveiller les TT
- surveiller les tweets des comptes importants

## Autres
- recherche une nouvelle librairie python de twitterscraping



# Monitoring & stats
## Stats de performance de campagne
- nb de tweets sur twitter

## Monitoring appli
- nb personnes acceptant les suggestions (is_ok)
- histogramme de la fréquence de suggestion de chaque participant.e
- nb messages envoyés / recus en temps réel

## Monitoring technique
### Charge
- temps d'itération de chaque boucle
- nb de lignes dans chaque table de la BDD
- temps de réponse moyen au messages "STOP", etc.

### Audit du vidage de data
- les logs :
    - les logs de twitterwatch
    - les logs de supervisord
    - les logs de l'app
- les dumps de la BDD sqlite3


 
# Futur
## Features
- !! important : quand on cherche les id TG des boucles et personnes, on se connecte avec son compte perso et la session reste enregistrée, et si on fait pas gaffe le programme général tourne avec cette session. #30hdeDebugPourRien
- les suggestions vont aussi aux admins (aussi les msg des scribes mais c'est normal) : c'est bien ou pas?
- !!! retirer les noms du code !!!
- attention, les liens html ne passent pas quand on copie-colle à la main un message en mode animateur (en tout cas avec TG desktop ubuntu)
- attention, avc les frequences par défaut, tout le monde se voit suggérer des tweets au meme moment. mettre un aléatoire dans les freq initiales MAIS aussi quand on augmente (pas augmenter de 20min pile tout le monsde) 
- l'admin doit pouvoir suggérer des tweets (et voir accès aux autres actions possibles?)
- les animateurs doivent pouvoir lancer la campagne et les suggetstions
- conf : mettre des comptes twitter plus importants que d'autres qui ont plus de chances detre retwités
- envoi de (mail/msg Teleg) à 5 amis chacun.e pour leur demander de retweeter
- une conf dynamique modifiable en cours de route
- demander confirmation au scribe dans les 2 min suivant le msg
  - NB : Si 2 messages ont été soumis en moins de 2 minutes, bien préciser à la recetion du 2nd message que le précédent est annulé ;)
- faire une boucle asynchone d'envoie des messages (ainsi les boucles sandbox et suggestions n'auront plus à avoir des fonctions asynchrones)
- interface de monitoring
- gestion des Exceptions (à ennvoyer sur le cpt DEV)
- dans les différentes boucles, il faut parfois recharger les données qui sont en BDD. Exemple boucle suggestion : quand on modifie le is_ok directement dans la BDD, ça ne s'actualise pas dans le programme

## optim
- todo_chk

## Pour un code plus beau
- revoir la classe logger
- les docstrings ;)
- todo_es

## wording
- dire au scribe de ne pas faire de la merde




# Notes en vrac
## Urls
- https://getdaytrends.com/fr/france/

## Spécificités twitter
Pour le poster, vous n'avez qu'à cliquer ici : https://twitter.com/compose/tweet?text=.%40FredericOudea%20va%20mettre%20sur%20pied%20une%20trajectoire%20passant%27probablement%27par%20la%20r%C3%A9duction%20en%20valeur%20absolue%20des%20p%C3%A9trole%20et%20gaz.%20Il%20y%20a%20des%20raisons%20de%20s%27inqui%C3%A9ter%20quand%20vous%20dites%20que%20vous%20voulez%20soutenir%20la%20croissance%20du%20%23schiste%21%20%23VosParisNotreAvenir

- exemples :
 - https://twitter.com/intent/retweet?tweet_id=1263063127538774016
 - https://twitter.com/intent/tweet?in_reply_to=1263063127538774016&related=twitterdev&text=J%20esp%C3%A8re
 - https://twitter.com/intent/like?tweet_id=463440424141459456
- doc :
 - https://developer.twitter.com/en/docs/twitter-for-websites/web-intents/overview
 - https://developer.twitter.com/en/docs/twitter-for-websites/tweet-button/guides/web-intent

## Idées
- Faire un concours pour que les gens s'emparent du TT ?
- Humour (idem, pr que les gens s'en emparent)
- Sondage?

## stats argumentaire utilité de l'appli
- ratio mb msg sour boucle 450/messages animateur.rices
- nb moy de retweet par personne / nb de retweet possibles avec l'appli
- nb de messages de partage de tweets sur la 450 qui auraient pu etre évités
- nb de participant.es vraiemnt actif.ves sur boucle
- nb de participant.es ayant posté au moins 1 tweet
