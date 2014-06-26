from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class News(models.Model):
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50)
    author = models.ForeignKey(User, verbose_name=u'Auteur')
    pub_date = models.DateTimeField('Date de publication')
    text = models.TextField()
    # img

    def __unicode__(self):
        return self.title



