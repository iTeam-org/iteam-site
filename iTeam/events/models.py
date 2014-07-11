from django.db import models

from django.contrib.auth.models import User

from django.conf import settings

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=settings.SIZE_MAX_TITLE, verbose_name=u'Titre')

    author = models.ForeignKey(User, verbose_name=u'Auteur')
    date = models.DateTimeField()

    text = models.TextField()
