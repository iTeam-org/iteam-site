import string
import os

from django.db import models

from django.contrib.auth.models import User

from django.conf import settings
from django.utils import timezone


def image_path(instance, filename):
    ext = string.lower(filename.split('.')[-1])
    filename = u'{}_original.{}'.format(str(instance.pk), ext)

    return os.path.join('evenements', filename)


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

    text = models.TextField()

    is_draft = models.BooleanField(u'Est un brouillon', default=True)

    type = models.CharField(
        u'Type de l\'event',
        max_length=1,
        choices=TYPES,
        default='O',
    )

    image = models.ImageField(
        upload_to='publications',
        blank=True,
        null=True,
        default=None
    )

    def status_style(self):
        if (self.date_start < timezone.now()):
            return 'p'
        else:
            return 'a'

    def status_str(self):
        if (self.date_start < timezone.now()):
            return 'A eu lieu le'
        else:
            return 'Aura lieu le'

    def image_url(self):
        if self.image:
            return self.image.url
        elif self.type == 'B':
            return '/static/img/bar.jpeg'
        elif self.type == 'F':
            return '/static/img/formation.jpg'
        else:
            return '/static/img/event.jpeg'
