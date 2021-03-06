#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-21 18:43:38
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-10-27 19:35:33

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


import string
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify


def image_path(instance, oldFilename):
    newFilename = 'image' + '.' + string.lower(oldFilename.split('.')[-1])

    return os.path.join('evenements', str(instance.pk), newFilename)


def file_path(instance, filename):
    return os.path.join('evenements', str(instance.pk), filename)


class Event(models.Model):
    title = models.CharField(max_length=settings.SIZE_MAX_TITLE)
    author = models.ForeignKey(User)
    place = models.TextField()
    date_start = models.DateTimeField()
    text = models.TextField()
    is_draft = models.BooleanField(default=True)
    type = models.CharField(
        max_length=1,
        choices=settings.EVENTS_MODEL_TYPES,
        default='O',
    )
    image = models.ImageField(
        upload_to=image_path,
        blank=True,
        null=True,
        default=None
    )

    file = models.FileField(
        upload_to=file_path,
        blank=True,
        null=True,
        default=None
    )

    def status_style(self):
        if self.date_start < timezone.now():
            return 'p'
        else:
            return 'a'

    def status_str(self):
        if self.date_start < timezone.now():
            return 'A eu lieu le'
        else:
            return 'Aura lieu le'

    def image_url(self):
        if self.image:
            return self.image.url
        elif self.type == 'B':
            return '/static/images/bar.jpeg'
        elif self.type == 'F':
            return '/static/images/formation.jpg'
        else:
            return '/static/images/event.jpeg'

    def get_absolute_url(self):
        return reverse('events:detail', args=[self.pk, slugify(self.title)])
