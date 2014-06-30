from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class News(models.Model):
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    TYPES = (
        ('N', u'News'),
        ('T', u'Tutoriel'),
        ('P', u'Publication')
    )

    title = models.CharField(max_length=100, verbose_name=u'Titre')
    subtitle = models.CharField(max_length=100, blank=True, verbose_name=u'Sous-titre')

    author = models.ForeignKey(User, verbose_name=u'Auteur')
    pub_date = models.DateTimeField('Date de publication')

    image = models.ImageField(
        upload_to='news',
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

    def __unicode__(self):
        return self.title

    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return '/media/news/default.png'
