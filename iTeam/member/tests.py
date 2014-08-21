#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-20 14:20:08
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-08-22 17:07:52

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


from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_dynamic_fixture import G

from iTeam.member.models import Profile


def MemberSetUp():
    user = G(User, username='member')
    user.set_password('password')
    user.save()
    profile = G(Profile, user=user)
    profile.save()

    user = G(User, username='publisher1')
    user.set_password('password')
    user.save()
    profile = G(Profile, user=user)
    profile.is_publisher = True
    profile.save()

    user = G(User, username='publisher2')
    user.set_password('password')
    user.save()
    profile = G(Profile, user=user)
    profile.is_publisher = True
    profile.save()

    user = G(User, username='admin')
    user.set_password('password')
    user.save()
    profile = G(Profile, user=user)
    profile.is_publisher = True
    profile.is_admin = True
    profile.save()


class MemberIntegrationTests(TestCase):

    def setUp(self):
        MemberSetUp()

    def test_index_view(self):
        resp = self.client.get(reverse('member:index'))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view(self):
        resp = self.client.get(reverse('member:detail', args=['member']))
        self.assertEqual(resp.status_code, 200)

    def test_settings_view(self):
        resp = self.client.get(reverse('member:settings_view'))
        self.assertEqual(resp.status_code, 302)

    def test_publications_view(self):
        resp = self.client.get(reverse('member:publications'))
        self.assertEqual(resp.status_code, 302)

    def test_events_view(self):
        resp = self.client.get(reverse('member:events'))
        self.assertEqual(resp.status_code, 302)

    def test_register_view(self):
        resp = self.client.get(reverse('member:register_view'))
        self.assertEqual(resp.status_code, 200)

    def test_login_view(self):
        resp = self.client.get(reverse('member:login_view'))
        self.assertEqual(resp.status_code, 200)

    def test_login_action(self):
        user = User.objects.get(username='member')
        data = {
            'username': 'member',
            'password': 'password'
        }
        self.client.post(reverse('member:login_view'), data)
        self.assertEqual(self.client.session['_auth_user_id'], user.pk)

    def test_logout_view(self):
        resp = self.client.get(reverse('member:logout_view'))
        self.assertEqual(resp.status_code, 302)


class AuthenticatedMemberIntegrationTests(TestCase):

    def setUp(self):
        MemberSetUp()
        self.client.login(username='member', password='password')

    def test_index_view(self):
        resp = self.client.get(reverse('member:index'))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view(self):
        resp = self.client.get(reverse('member:detail', args=['member']))
        self.assertEqual(resp.status_code, 200)

    def test_settings_view(self):
        resp = self.client.get(reverse('member:settings_view'))
        self.assertEqual(resp.status_code, 200)

    def test_publications_view(self):
        resp = self.client.get(reverse('member:publications'))
        self.assertEqual(resp.status_code, 403)

    def test_events_view(self):
        resp = self.client.get(reverse('member:events'))
        self.assertEqual(resp.status_code, 403)

    def test_register_view(self):
        resp = self.client.get(reverse('member:register_view'))
        self.assertEquals(resp.status_code, 200)

    def test_login_view(self):
        resp = self.client.get(reverse('member:login_view'))
        self.assertEquals(resp.status_code, 200)

    def test_logout_view(self):
        resp = self.client.get(reverse('member:logout_view'))
        self.assertEquals(resp.status_code, 200)


class PublisherMemberIntegrationTests(TestCase):

    def setUp(self):
        MemberSetUp()
        self.client.login(username='publisher1', password='password')

    def test_index_view(self):
        resp = self.client.get(reverse('member:index'))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view(self):
        resp = self.client.get(reverse('member:detail', args=['member']))
        self.assertEqual(resp.status_code, 200)

    def test_settings_view(self):
        resp = self.client.get(reverse('member:settings_view'))
        self.assertEqual(resp.status_code, 200)

    def test_publications_view(self):
        resp = self.client.get(reverse('member:publications'))
        self.assertEqual(resp.status_code, 200)

    def test_events_view(self):
        resp = self.client.get(reverse('member:events'))
        self.assertEqual(resp.status_code, 200)

    def test_register_view(self):
        resp = self.client.get(reverse('member:register_view'))
        self.assertEquals(resp.status_code, 200)

    def test_login_view(self):
        resp = self.client.get(reverse('member:login_view'))
        self.assertEquals(resp.status_code, 200)

    def test_logout_view(self):
        resp = self.client.get(reverse('member:logout_view'))
        self.assertEquals(resp.status_code, 200)


class AdminMemberIntegrationTests(TestCase):

    def setUp(self):
        MemberSetUp()
        self.client.login(username='admin', password='password')

    def test_index_view(self):
        resp = self.client.get(reverse('member:index'))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view(self):
        resp = self.client.get(reverse('member:detail', args=['member']))
        self.assertEqual(resp.status_code, 200)

    def test_settings_view(self):
        resp = self.client.get(reverse('member:settings_view'))
        self.assertEqual(resp.status_code, 200)

    def test_publications_view(self):
        resp = self.client.get(reverse('member:publications'))
        self.assertEqual(resp.status_code, 200)

    def test_events_view(self):
        resp = self.client.get(reverse('member:events'))
        self.assertEqual(resp.status_code, 200)

    def test_register_view(self):
        resp = self.client.get(reverse('member:register_view'))
        self.assertEquals(resp.status_code, 200)

    def test_login_view(self):
        resp = self.client.get(reverse('member:login_view'))
        self.assertEquals(resp.status_code, 200)

    def test_logout_view(self):
        resp = self.client.get(reverse('member:logout_view'))
        self.assertEquals(resp.status_code, 200)
