#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-19 17:38:33
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-11-02 18:08:40

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

from iTeam.member import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),

    url(r'^voir/(?P<user_name>.+)/$', views.detail, name='detail'),
    url(r'^parametres/$', views.settings_view, name='settings_view'),

    url(r'^inscription/$', views.register_view, name='register_view'),
    url(r'^connexion/$', views.login_view, name='login_view'),
    url(r'^deconnexion/$', views.logout_view, name='logout_view'),

    url(r'^oubli/$', views.password_reset_ask, name='password_reset_ask'),
    url(r'^oubli/(?P<token>.+)/$', views.password_reset_confirm, name='password_reset_confirm'),
)

# Note : '_view' because of weird recursive function call ...
