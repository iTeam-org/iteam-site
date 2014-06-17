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

    # Profile
    url(r'^voir/(?P<user_name>.+)$', views.details, name='voir'),
    url(r'^profil/editer$', views.edit_profile, name='editer'),

    # User's actions
    url(r'^publications$', views.publications, name='publications'),

    # Settings
    url(r'^parametres/profil$', views.settings_profile, name='param_profil'),
    url(r'^parametres/compte$', views.settings_account, name='param_compte'),

    url(r'^inscription$', views.register_view, name='register'),
    url(r'^connexion$', views.login_view, name='login'),
    url(r'^deconnexion/$', views.logout_view, name='logout'),
    url(r'^$', views.index, name='index'),
)