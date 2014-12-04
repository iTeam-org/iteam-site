#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-19 18:35:38
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-12-04 16:35:31

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


from django.shortcuts import render
from django.utils import timezone

from iTeam.publications.models import Publication
from iTeam.events.models import Event


def index(request):
    return render(request, 'pages/index.html')


def home(request):
    publications_list = Publication.objects.all().filter(pub_date__lte=timezone.now(), is_draft=False). \
        order_by('-pub_date')[:5]
    events_list = Event.objects.all().filter(is_draft=False). \
        order_by('-date_start')[:5]

    return render(request, 'home.html', {"publications_list": publications_list, 'events_list': events_list})


def apropos(request):
    return render(request, 'pages/apropos.html')


def hallOfFame(request):
    return render(request, 'pages/hallOfFame.html')


def cookies(request):
    return render(request, 'pages/cookies.html')

def links(request):
    return render(request, 'pages/links.html')
