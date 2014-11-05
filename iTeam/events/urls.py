#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-20 14:39:03
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-11-05 12:08:17

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


from django.conf.urls import patterns, url

from iTeam.events import views, feeds


urlpatterns = patterns('',
    url(r'^feed/rss/$', feeds.LastEventsFeedRSS(), name='events_feed_rss'),
    url(r'^feed/atom/$', feeds.LastEventsFeedATOM(), name='events_feed_atom'),

    url(r'^list/$', views.index_list, name='index_list'),
    url(r'^week/(?P<days_since_epoch>\d+)/$', views.index_week, name='index_week'),
    url(r'^month/(?P<year>\d+)/(?P<month>\d+)/$', views.index_month, name='index_month'),

    url(r'^create/$', views.create, name='create'),
    url(r'^view/(?P<event_id>\d+)/(?P<event_slug>.+)/$', views.detail, name='detail'),
    url(r'^edit/(?P<event_id>\d+)/$', views.edit, name='edit'),
    url(r'^author/(?P<username>.+)$', views.by_author, name='by_author'),
)
