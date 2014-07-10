from django.db import models

from django.contrib.auth.models import User

from django.conf import settings

# Create your models here.


class Publication(models.Model):
    TYPES = (
        ('N', u'News'),
        ('T', u'Tutoriel'),
        ('P', u'Publication')
    )

    title = models.CharField(max_length=settings.SIZE_MAX_TITLE, verbose_name=u'Titre')
    subtitle = models.CharField(max_length=settings.SIZE_MAX_TITLE, blank=True, verbose_name=u'Sous-titre')

    author = models.ForeignKey(User, verbose_name=u'Auteur')
    pub_date = models.DateTimeField('Date de publication')

    image = models.ImageField(
        upload_to='publications',
        blank=True,
        null=True,
        default=None
    )

    type = models.CharField(
        u'Type de la publication',
        max_length=1,
        choices=TYPES,
        default='P',
    )

    text = models.TextField()

    is_draft = models.BooleanField(u'Est un brouillon', default=True)

    def __unicode__(self):
        return self.title

    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return '/media/publications/default.png'
