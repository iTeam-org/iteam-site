from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class News(models.Model):
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    TYPE = (
        ('N', u'News'),
        ('T', u'Tutoriel'),
    )


    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True)

    author = models.ForeignKey(User, verbose_name=u'Auteur')
    pub_date = models.DateTimeField('Date de publication')

    image = models.ImageField(
        upload_to='news',
        blank=True,
        null=True,
        default=None
    )

    """
    size = models.CharField(
        u'Type de la publication',
        max_length=1,
        choices=TYPE,
    )
    """

    text = models.TextField()

    def __unicode__(self):
        return self.title

    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return '/media/news/default.png'
