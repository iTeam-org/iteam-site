#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-10-28 19:45:49
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-10-29 12:36:19

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


from django.contrib import admin
from iTeam.stats.models import Log


class LogAdmin(admin.ModelAdmin):
    # fields for ALL publications
    list_display = ('ip', 'date', 'method', 'useragent', 'url', 'referer')

    list_filter = ['date', 'method']
    search_fields = ['ip', 'date', 'url', 'method', 'referer', 'useragent']


admin.site.register(Log, LogAdmin)
