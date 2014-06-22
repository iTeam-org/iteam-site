# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

"""
    models.py

    Define properties of a Profile (= User + special info) and usefull functions
"""

from hashlib import md5
from datetime import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name=u'Utilisateur')
    promo = models.IntegerField()

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'

    def __unicode__(self):
        """
            Textual representation of a profile.
        """
        return ' - '.join((self.user.username, self.get_ing()))

    def get_ing(self, now=datetime.now()):
        """
            Return the proper : ing1 ing2 ing3 ing4 ing5 or none
        """
        # from sept to dec
        if now.month >= 9:
            return str(5 - (self.promo - now.year - 1))
        # from jan to june
        elif now.month <= 6:
            return str(5 - (self.promo - now.year))
        else:
            return None

    def get_absolute_url(self):
        """
            Get URL to view this profile.
        """
        return reverse('iTeam.member.views.details', args=[self.user.username])

    def get_avatar_url(self):
        """
            Get the member's avatar URL.
            This will use custom URL or Gravatar.
        """
        if self.avatar_url:
            return self.avatar_url
        else:
            return 'https://secure.gravatar.com/avatar/{0}?d=identicon'\
                .format(md5(self.user.email).hexdigest())

