# CDC site web #

------------------------------------------------------------
todo long run
- dump iteam.org
- tests
- use pk not id
- no style in html template -> css
- <img> : alt
- button radius
- flake8 compliant (pep8 + other stuff)
- `git tag -a v1.4 -m 'my version 1.4'` + `git push origin --tags`
- migrations
    * ./manage.py schemamigration app_name --initial
    * ./manage.py schemamigration app_name --auto 

#########################################################
#                                                       #
# << Premature optimization is the root of all evil. >> #
#                                                       #
#########################################################

to do now
- https://docs.djangoproject.com/en/dev/ref/contrib/sitemaps/
- syndication (rss + atom) : https://docs.djangoproject.com/en/dev/ref/contrib/syndication/
- media sociaux (syncro fb, twitter, google) -> https://github.com/foxmask/django-th
- news / tuto / articles : export pdf (pandoc)

to do maybe
- noscript : menu, (logout ok)
- calendar : list (prochain, passés, ...)
- publications : tags, multi-page
- better member (mail, citation, bio, ... osef ?)

to do later
- ancien iteam.org a lire / parser
- compte Flickr
- nas de Marine Mathieu (là en 2007)
- forum.iteam.org


------------------------------------------------------------
## News ##

**Description**
cette partie permet aux utilisateurs de consulter les news du site web, posté par les administrateurs/modérateurs.

**Contient**

* index
* detail
* create
* edit

-> markdown

1 page accessible à tout le monde affichant les dernières news de la plus récente à la plus vieille. Laissez au choix l'utilisateur de pouvoir avoir 5,10 ou 20 news par page. Accessibilité des news antérieurs en allant sur les pages suivantes (un peu comme tout système de blog, exemple : l'utilisateur a choisi 5 articles par page, donc la page affiche les 5 plus récents, la page 2 les 5 suivants etc)
1 page pour les administrateur permettant de créer/éditer/supprimer des news. Le contenu d'une news n'est pas du simple texte, un minimum de formatage CSS doit être possible, ainsi qu'ajouter des images. Le JavaScript et le PHP cependant doivent être bloqués pour des questions de sécurité. 


------------------------------------------------------------
## Tutos ##

** Description **
une section contenant tous les tutos de l'iTeam et autres tutos sur le libre (qui n'ont pas leur place sur le CRI).

** Contient **
1 page mettant toutes les tutos, 1 page affichant le tuto. Une page pour créer des tutos, le créateur du tuto peut choisir de faire son tuto sur plusieurs pages (pour éviter des pages trop longues) donc faut penser à ajouter cette possibilité. Cette page doit afficher tous les tutos créés par l'utilisateur avec la possibilité d'éditer/supprimer ses tutos et le bouton pour ajouter un tuto. Il serait aussi bien d'accepter le HTML dans les tutos et peut être aussi le JavaScript, ce qui implique donc quelques problèmes de sécurité à considérer. Il faut aussi une page administrateur permettant d'afficher tous les tutos et de pouvoir les éditer supprimer.


------------------------------------------------------------
## Calendrier ##

**Description**
un calendrier tout ce qu'il y a de plus standard (et joli si possible) pour obtenir les derniers événements iTeam. Ce calendrier doit comporter une vue dite mensuel, qui affiche le mois entier, avec les événements correspondant à chaque jour, dans un ordre chronologique, mais sans espacement quelconque pour indiquer qu'il y a 3 heures entre deux événements (c'est pas super clair, donc demandez moi si vous avez pas compris). Une vue semaine détaillant précisément le horaires (un peu comme sur google agenda ou EDT ECE (sic) ). L'utilisateur soit pouvoir cliquer les  événements correspondants qui le ramèneront vers la page décrivant l'événement.

**Contient**
1 page représentant le calendrier. 1 page d'administration pour ajouter/éditer/supprimer une entrée sur le calendrier.


------------------------------------------------------------
## Événement ##

**Description**
dans cette partie on trouve tous les événements (bar, conf, resto etc) de l'iTeam que l'on peut rechercher avec des critères, suivre l'événement sur Facebook, répondre présent ou non etc.

**Contient**
1 page avec un champ de recherche et listant les événements. Une page réservée aux administrateurs pour créer éditer et supprimer les événements.


------------------------------------------------------------
## Formation ##

**Description**
cette partie offre aux utilisateurs une interface pour obtenir des informations sur les formations aussi bien passées que futures.

**Contient**
1 page listant toutes les formations, avec une distinction entre les formations passées et les formations à venir. 1 page décrivant une formation plus en détail, l'affichage doit être différent si la formation est déjà passée ou non. Dans tous les cas une formation est décrite par un formateur, la description de la formation, ainsi que des liens vers des fichiers/liens utiles pour la formation. Si la formation n'est pas encore passée, elle contient en plus une date et un lieu, ainsi que la possibilité de s'inscrire (pour peut être à terme avoir une notification par mail par exemple, pour rappel ou autre). Si la formation est passée, celle contient un lien vers la vidéo de la formation.

Ces deux pages (la liste des formations et leur détail individuel) peut être aussi assimilé à une seule et même page (avec une variable PHP globale GET pour différencier, l'affichage général de l'affichage détaillé).

1 page permettant aux administrateur de créer/éditer/supprimer des news. 1 page permettant au formateur de poster des fichiers pour sa formation ou d'éditer la description (ATTENTION : le formateur ne doit pouvoir modifier que cela)


------------------------------------------------------------
## Synchronisation avec médias sociaux ##

**Description**
un script (par site google + facebook + twitter) qui permet de poster sur nos différentes pages d'asso.

**Contient**
autant de scripts que nécessaire.

- https://developers.facebook.com/docs/graph-api/reference/v2.0/user/feed
- ifttt
- https://github.com/foxmask/django-th

----------------
## Users tests

* Walk me through how you might checkout and pay on our site.
* Where on this site would you go to find the company's contact information?
* What do you think a "project" means within the context of this application?
* Let's say you're shopping for a gift. How would you use this to shop for someone else?
* Which visual elements interest you most on this home page?


