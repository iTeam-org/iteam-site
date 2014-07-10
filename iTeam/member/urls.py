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
)
