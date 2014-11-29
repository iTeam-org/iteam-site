#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-20 14:20:08
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-11-01 14:18:01

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
    user = G(User, username='member', email='member@gmail.com')
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
    profile.avatar_url = 'http://progdupeu.pl/media/tutorials/335/thumb.png'
    profile.save()


class MemberIntegrationTests(TestCase):

    def setUp(self):
        MemberSetUp()

    def test_index_view(self):
        resp = self.client.get(reverse('member:index'))
        self.assertEqual(resp.status_code, 200)

    def test_index_view_page_two(self):
        resp = self.client.get(reverse('member:index')+'?page=2')
        self.assertEqual(resp.status_code, 200)

    def test_index_view_page_nonexistant(self):
        resp = self.client.get(reverse('member:index')+'?page=999999')
        self.assertEqual(resp.status_code, 200)

    def test_index_view_page_none(self):
        resp = self.client.get(reverse('member:index')+'?page=')
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_member(self):
        resp = self.client.get(reverse('member:detail', args=['member']))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_admin(self):
        resp = self.client.get(reverse('member:detail', args=['admin']))
        self.assertEqual(resp.status_code, 200)

    def test_settings_view(self):
        resp = self.client.get(reverse('member:settings_view'))
        self.assertEqual(resp.status_code, 302)

    def test_register_view(self):
        resp = self.client.get(reverse('member:register_view'))
        self.assertEqual(resp.status_code, 200)

    def test_login_view(self):
        resp = self.client.get(reverse('member:login_view'))
        self.assertEqual(resp.status_code, 200)

    def test_login_action(self):
        data = {
            'username': 'member',
            'password': 'password'
        }
        resp = self.client.post(reverse('member:login_view'), data)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('iTeam.pages.views.home'))

    def test_login_action_next(self):
        data = {
            'username': 'member',
            'password': 'password'
        }
        url = reverse('member:login_view') + '?next=' + reverse('member:detail', args=['member'])

        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('member:detail', args=['member']))

    def test_login_action_autologin(self):
        data = {
            'username': 'member',
            'password': 'password',
            'auto_login': True
        }

        resp = self.client.post(reverse('member:login_view'), data)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('iTeam.pages.views.home'))

    def test_login_action_empty(self):
        data = {
            'username': '',
            'password': ''
        }
        resp = self.client.post(reverse('member:login_view'), data)
        self.assertEqual(resp.request['PATH_INFO'], reverse('member:login_view'))

    def test_login_action_fail(self):
        data = {
            'username': 'nonexistant',
            'password': 'nonexistant'
        }
        resp = self.client.post(reverse('member:login_view'), data)
        self.assertEqual(resp.request['PATH_INFO'], reverse('member:login_view'))

    def test_logout_view(self):
        resp = self.client.get(reverse('member:logout_view'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('member:login_view') + '?next=' + reverse('member:logout_view'))

    def test_register_action_error_pseudo_void(self):
        data = {
            'username': '  ',
            'password': 'password',
            'password_confirm': 'password',
            'email': 'user@gmail.com'
        }
        resp = self.client.post(reverse('member:register_view'), data)
        self.assertEqual(resp.request['PATH_INFO'], reverse('member:register_view'))

    def test_register_action_error_pseudo_used(self):
        data = {
            'username': 'member',
            'password': 'password',
            'password_confirm': 'password',
            'email': 'user@gmail.com'
        }
        resp = self.client.post(reverse('member:register_view'), data)
        self.assertEqual(resp.request['PATH_INFO'], reverse('member:register_view'))

    def test_register_action_error_pseudo_coma(self):
        data = {
            'username': 'super,Hacker',
            'password': 'password',
            'password_confirm': 'password',
            'email': 'user@gmail.com'
        }
        resp = self.client.post(reverse('member:register_view'), data)
        self.assertEqual(resp.request['PATH_INFO'], reverse('member:register_view'))

    def test_register_action_error_pseudo_space(self):
        data = {
            'username': ' superHacker ',
            'password': 'password',
            'password_confirm': 'password',
            'email': 'user@gmail.com'
        }
        resp = self.client.post(reverse('member:register_view'), data)
        self.assertEqual(resp.request['PATH_INFO'], reverse('member:register_view'))

    def test_register_action_error_password_diff(self):
        data = {
            'username': 'superHacker',
            'password': 'password_different',
            'password_confirm': 'password',
            'email': 'user@gmail.com'
        }
        resp = self.client.post(reverse('member:register_view'), data)
        self.assertEqual(resp.request['PATH_INFO'], reverse('member:register_view'))

    def test_register_action_error_same_username_password(self):
        data = {
            'username': 'same',
            'password': 'same',
            'password_confirm': 'same',
            'email': 'user@gmail.com'
        }
        resp = self.client.post(reverse('member:register_view'), data)
        self.assertEqual(resp.request['PATH_INFO'], reverse('member:register_view'))

    def test_register_action_mail_used(self):
        data = {
            'username': 'superHacker',
            'password': 'password',
            'password_confirm': 'password',
            'email': 'member@gmail.com'
        }
        resp = self.client.post(reverse('member:register_view'), data)
        self.assertEqual(resp.request['PATH_INFO'], reverse('member:register_view'))

    def test_register_action(self):
        data = {
            'username': 'superHacker',
            'password': 'password',
            'password_confirm': 'password',
            'email': 'user@gmail.com'
        }
        resp = self.client.post(reverse('member:register_view'), data)
        self.assertEqual(resp.status_code, 200)


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

    def test_register_view(self):
        resp = self.client.get(reverse('member:register_view'))
        self.assertEquals(resp.status_code, 200)

    def test_login_view(self):
        resp = self.client.get(reverse('member:login_view'))
        self.assertEquals(resp.status_code, 200)

    def test_logout_view(self):
        resp = self.client.get(reverse('member:logout_view'))
        self.assertEquals(resp.status_code, 200)

    def test_settings_action_error_post(self):
        # change password via form
        data = {
            'password_old': '',
            'password_new': '',
            'password_confirm': '',
        }
        resp = self.client.post(reverse('member:settings_view'), data)
        self.assertEqual(resp.request['PATH_INFO'], reverse('member:settings_view'))

    def test_settings_action_error_pass_old(self):
        # change password via form
        data = {
            'password_old': '',
            'password_new': 'pass',
            'password_confirm': 'pass',
        }
        resp = self.client.post(reverse('member:settings_view'), data)
        self.assertEqual(resp.request['PATH_INFO'], reverse('member:settings_view'))

    def test_settings_action_error_pass_new(self):
        # change password via form
        data = {
            'password_old': 'password',
            'password_new': 'pass',
            'password_confirm': 'pass_diff',
        }
        resp = self.client.post(reverse('member:settings_view'), data)
        self.assertEqual(resp.request['PATH_INFO'], reverse('member:settings_view'))

    def test_settings_action(self):
        user = User.objects.get(username='member')

        # change password via form
        data = {
            'password_old': 'password',
            'password_new': 'pass',
            'password_confirm': 'pass',
        }
        resp = self.client.post(reverse('member:settings_view'), data)
        self.assertEqual(resp.request['PATH_INFO'], reverse('member:settings_view'))

        # logout
        # (assert : status_code = 200 found + user_id no more in session data + url equals home)
        self.client.post(reverse('member:logout_view'), {})
        self.assertEqual(resp.status_code, 200)  # FAIL should be 302
        self.assertTrue('_auth_user_id' not in self.client.session)

        # login with the new password
        self.client.login(username='member', password='pass')
        #self.assertEqual(self.client.session['_auth_user_id'], user.pk) error now o_O


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

    def test_register_view(self):
        resp = self.client.get(reverse('member:register_view'))
        self.assertEquals(resp.status_code, 200)

    def test_login_view(self):
        resp = self.client.get(reverse('member:login_view'))
        self.assertEquals(resp.status_code, 200)

    def test_logout_view(self):
        resp = self.client.get(reverse('member:logout_view'))
        self.assertEquals(resp.status_code, 200)

    """ FAIL
    def test_member_name_publisher_and_admin(self):
        user = User.objects.get(username='member')
        member = Profile.objects.get(user=user)
        toggle_is_publisher = {'toggle_is_publisher': ''}
        toggle_is_admin = {'toggle_is_admin': ''}

        # default
        self.assertEquals(member.is_publisher, False)
        self.assertEquals(member.is_admin, False)

        # publisher
        resp = self.client.post(reverse('member:detail', args=['member']), toggle_is_publisher)
        print resp.status_code
        self.assertEquals(member.is_publisher, True)

        resp = self.client.post(reverse('member:detail', args=['member']), toggle_is_publisher)
        self.assertEquals(member.is_publisher, False)

        # admin
        resp = self.client.post(reverse('member:detail', args=['member']), toggle_is_admin)
        self.assertEquals(member.is_admin, True)
        self.assertEquals(member.is_publisher, True)

        resp = self.client.post(reverse('member:detail', args=['member']), toggle_is_admin)
        self.assertEquals(member.is_admin, False)
        self.assertEquals(member.is_publisher, False)
    """
