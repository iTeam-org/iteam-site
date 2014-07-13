
from hashlib import md5

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    promo = models.IntegerField(null=True)
    avatar_url = models.CharField(max_length=256, null=True, default='')

    is_publisher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'

    def __unicode__(self):
        """
            Textual representation of a profile.
        """
        return self.user.username

    def get_avatar_url(self):
        """
            Get the member's avatar URL.
            This will use custom URL or Gravatar.
        """
        if self.avatar_url:
            return self.avatar_url
        else:
            return 'https://secure.gravatar.com/avatar/{0}?d=identicon&s=50'.format(md5(self.user.username).hexdigest())

