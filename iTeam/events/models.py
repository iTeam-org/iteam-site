from django.db import models

from django.contrib.auth.models import User

from django.conf import settings

# Create your models here.

class Event(models.Model):
    TYPES = (
        ('F', u'Formation'),
        ('C', u'Conference'),
        ('B', u'Bar'),
        ('J', u'Journee portes ouvertes'),
        ('A', u'AG'),
        ('O', u'Autre'), # other
    )

    title = models.CharField(max_length=settings.SIZE_MAX_TITLE, verbose_name=u'Titre')
    author = models.ForeignKey(User, verbose_name=u'Auteur')
    place = models.TextField()

    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    text = models.TextField()

    type = models.CharField(
        u'Type de l\'event',
        max_length=1,
        choices=TYPES,
        default='O',
    )
