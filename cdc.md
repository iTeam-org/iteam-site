python manage.py dumpdata --format=json myapp > data.json
https://docs.djangoproject.com/en/1.6/topics/security/

# CDC site web #

------------------------------------------------------------
todo :
-> dump iteam.org

- clean templates (crispy form, ...) + tests
- news / tuto : draft boolean + better error / keep data
- better member (mail, citation, bio, ...) + member:settings_view

- calendrier (http://uggedal.com/journal/creating-a-flexible-monthly-calendar-in-django/ + https://github.com/llazzaro/django-scheduler)
- event + formation : formation, jpo, bar, ...

- a propos / l'iteam
- bitbucket / github


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

.........................
POST graph.facebook.com
  /{user-id}/feed?
    message={message}&
    access_token={access-token}
.........................
 https://developers.facebook.com/docs/graph-api/reference/v2.0/user/feed
.........................
POST /me/feed HTTP/1.1
Host: graph.facebook.com

message=This+is+a+test+message



.........................
 DJANGO IMAGES
.........................


In your settings file, you’ll need to define MEDIA_ROOT as the full path to a directory where you’d like Django to store uploaded files. (For performance, these files are not stored in the database.) Define MEDIA_URL as the base public URL of that directory. Make sure that this directory is writable by the Web server’s user account.
Add the FileField or ImageField to your model, defining the upload_to option to specify a subdirectory of MEDIA_ROOT to use for uploaded files.
All that will be stored in your database is a path to the file (relative to MEDIA_ROOT). You’ll most likely want to use the convenience url attribute provided by Django. For example, if your ImageField is called mug_shot, you can get the absolute path to your image in a template with {{ object.mug_shot.url }}.



image = models.ImageField(
        upload_to=image_path,
        blank=True, null=True,
        default=None
    )


def image_path(instance, filename):
    """Get path to a tutorial image.

    Returns:
        string

    """
    ext = filename.split('.')[-1]
    filename = u'original.{}'.format(string.lower(ext))
    return os.path.join('tutorials', str(instance.pk), filename)


def thumbnail_path(instance, filename):
    """Get path to a tutorial thumbnail.

    Returns:
        string

    """
    ext = filename.split('.')[-1]
    filename = u'thumb.{}'.format(string.lower(ext))
    return os.path.join('tutorials', str(instance.pk), filename)

    

image = Image.open(self.image)

            if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')

            image.thumbnail(thumb_size, Image.ANTIALIAS)

            # save the thumbnail to memory
            temp_handle = StringIO()
            image.save(temp_handle, 'png')
            temp_handle.seek(0)  # rewind the file

            # save to the thumbnail field
            suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                                     temp_handle.read(),
                                     content_type='image/png')
            self.thumbnail.save(u'{}.png'.format(suf.name), suf, save=False)

            # save the image object
            super(Tutorial, self).save(force_update, force_insert)
