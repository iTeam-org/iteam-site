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

"""Models for member app."""

from hashlib import md5

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Profile(models.Model):

    """Represents an user profile."""

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'

    user = models.ForeignKey(User, unique=True, verbose_name=u'Utilisateur')

    def __unicode__(self):
        """Textual representation of a profile.

        Returns:
            string

        """
        return self.user.username

    def get_absolute_url(self):
        """Get URL to view this profile.

        Returns:
            string

        """
        return reverse('pdp.member.views.details', args=[self.user.username])

    def get_avatar_url(self):
        """Get the member's avatar URL.

        This will use custom URL or Gravatar.

        Returns:
            string

        """
        if self.avatar_url:
            return self.avatar_url
        else:
            return 'https://secure.gravatar.com/avatar/{0}?d=identicon'\
                .format(md5(self.user.email).hexdigest())
