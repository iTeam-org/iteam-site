from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class News(models.Model):
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, verbose_name=u'Auteur')
    pub_date = models.DateTimeField('Date de publication')
    text = models.TextField()

    image = models.ImageField(
        upload_to='news',
        blank=True,
        null=True,
        default=None
    )

    def __unicode__(self):
        return self.title

    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return '/static/img/tux.png'
