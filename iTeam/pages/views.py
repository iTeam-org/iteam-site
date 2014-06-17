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

from iTeam.news.models import News

def home(request):
    """Display the home page with last articles, tutorials and topics added.

    Returns:
        HttpResponse

    """

    news_list = News.objects.all().order_by('-pub_date')[:5]

    return render(request, 'home.html', {"data": news_list})

def iteam(request):
    return HttpResponse('iteam')


def apropos(request):
    return HttpResponse('apropos')

