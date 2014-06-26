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
    user = models.ForeignKey(User, unique=True)
    promo = models.IntegerField(blank=True)
    avatar_url = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'

    def __unicode__(self):
        """
            Textual representation of a profile.
        """
        return ' - '.join((self.user.username, self.get_ing()))

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
            return 'https://secure.gravatar.com/avatar/{0}?d=identicon&s=50'.format(md5(self.user.username).hexdigest())





