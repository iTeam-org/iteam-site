#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-10-28 19:29:36
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-12-04 19:37:15

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

from django.conf import settings
from django.http import HttpResponse

from iTeam.stats.models import Log


class Log_middleware(object):

    def process_request(self, request):
        url = request.get_full_path()
        head = url.split('/')[1]

        if head != 'a':
            l = Log().set_attr(request)
            l.save()

            if 'bot' not in l.useragent.lower():
                fucker = l.useragent.startswith('() { :;};')
                for word in settings.FORBIDDEN_WORDS:
                    fucker = fucker or (word in url)

                if fucker:
                    l.useragent += ' -- Spotted'
                    l.save()
                    return HttpResponse('Il semblerait que vous soyez mal intentionné, merci de ne pas recommencer ><', status=418)
