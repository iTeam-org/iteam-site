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

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from iTeam.publications.models import Publication

def home(request):
    publications_list = Publication.objects.all().filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

    return render(request, 'home.html', {"publications_list": publications_list})

def iteam(request):
    return render(request, 'pages/iteam.html')


def apropos(request):
    return render(request, 'pages/apropos.html')

