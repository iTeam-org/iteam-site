from django.db import models

# Create your models here.


class News(models.Model):
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    pub_date = models.DateTimeField('Date de publication')
    text = models.TextField()

    def __unicode__(self):
        return self.title



