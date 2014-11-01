#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-20 14:35:58
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-11-01 14:33:28

# This file is part of iTeam.org.
# Copyright (C) 2014 Adrien Chardon (Nodraak).
#
# iTeam.org is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# iTeam.org is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with iTeam.org. If not, see <http://www.gnu.org/licenses/>.


from hashlib import md5

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    promo = models.IntegerField(blank=True, null=True)
    avatar_url = models.CharField(max_length=256, blank=True, default='')

    is_publisher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def get_avatar_url(self):
        if self.avatar_url:
            return self.avatar_url
        else:
            username_hash = md5(self.user.username).hexdigest()
            size = 100
            return 'https://secure.gravatar.com/avatar/{0}?d=identicon&s={1}'.format(username_hash, size)
