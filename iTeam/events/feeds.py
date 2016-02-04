#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-11-05 12:04:47
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-11-05 13:50:57

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


from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from iTeam.events.models import Event


class LastEventsFeedRSS(Feed):
    title = "iTeam - Événements"
    link = "/events/list/"
    description = "Les derniers événements de l'iTeam"

    def items(self):
        return Event.objects.filter(is_draft=False).order_by('-date_start')[:5]

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_start

    def item_description(self, item):
        return item.text

    def item_author_name(self, item):
        return item.author

    def item_link(self, item):
        return item.get_absolute_url()


class LastEventsFeedATOM(LastEventsFeedRSS):
    feed_type = Atom1Feed
    subtitle = LastEventsFeedRSS.description
