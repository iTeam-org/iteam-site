#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-10-28 19:07:27
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-10-29 13:28:08

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


from django.db import models
from django.utils import timezone


class Log(models.Model):
    ip = models.CharField(max_length=256, default='-')
    date = models.DateTimeField()
    url = models.CharField(max_length=256)
    method = models.CharField(max_length=256, default='-')
    referer = models.CharField(max_length=256, default='-')
    useragent = models.CharField(max_length=256, default='-')

    def set_attr(self, request):
        self.date = timezone.now()
        self.url = request.get_full_path()

        if 'REQUEST_METHOD' in request.META:
            self.method = request.META['REQUEST_METHOD']

        if 'HTTP_USER_AGENT' in request.META:
            self.useragent = request.META['HTTP_USER_AGENT']

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            self.ip = request.META['HTTP_X_FORWARDED_FOR']

        if 'HTTP_REFERER' in request.META:
            self.referer = request.META['HTTP_REFERER']

        return self