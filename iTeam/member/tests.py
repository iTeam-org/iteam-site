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


from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_dynamic_fixture import G

from iTeam.member.models import Profile


class MemberIntegrationTests(TestCase):

    def test_index(self):
        resp = self.client.get(reverse('member:index'))
        self.assertEqual(resp.status_code, 200)

    def test_details(self):
        user = G(User, username='user42')
        user.save()
        profile = G(Profile, user=user)
        profile.save()

        resp = self.client.get(reverse('member:detail', args=[user.username]))
        self.assertEqual(resp.status_code, 200)

    def test_settings(self):
        resp = self.client.get(reverse('member:settings_view'))
        self.assertEqual(resp.status_code, 302)

    def test_publications(self):
        resp = self.client.get(reverse('member:publications'))
        self.assertEqual(resp.status_code, 302)

    def test_register_view(self):
        resp = self.client.get(reverse('member:register_view'))
        self.assertEqual(resp.status_code, 200)

    def test_login_view(self):
        resp = self.client.get(reverse('member:login_view'))
        self.assertEqual(resp.status_code, 200)

    def test_login_action(self):
        user = G(User, username='user42')
        user.set_password('password')
        user.save()

        G(Profile, user=user)

        self.client.post(reverse('member:login_view'),
                         {'username': 'user42',
                          'password': 'password'})

        self.assertEqual(self.client.session['_auth_user_id'], user.pk)

    def test_logout_view(self):
        resp = self.client.get(reverse('member:logout_view'))
        self.assertEqual(resp.status_code, 302)


class AuthenticatedMemberIntegrationTests(TestCase):

    def setUp(self):
        # Create user
        self.user = G(User, username='user42')
        self.user.set_password('password')
        self.user.save()

        # Create profile
        self.profile = G(Profile, user=self.user)

        # Authenticate user
        self.client.login(username='user42', password='password')

    def test_settings_view(self):
        resp = self.client.get(reverse('member:settings_view'))
        self.assertEqual(resp.status_code, 200)

    def test_publications(self):
        resp = self.client.get(reverse('member:publications'))
        self.assertEqual(resp.status_code, 403)

    def test_logout_view(self):
        resp = self.client.get(reverse('member:logout_view'))
        self.assertEquals(resp.status_code, 200)
