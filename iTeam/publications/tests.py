#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-20 14:09:26
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-09-02 14:34:23

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


from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django_dynamic_fixture import G

from iTeam.publications.models import Publication
from iTeam.member.tests import MemberSetUp


def PublicatonSetUp():
    MemberSetUp()

    user = User.objects.get(username='publisher1')
    publication = G(
        Publication,
        title='title',
        author=user,
        pub_date=timezone.now(),
        text='hello world !',
        pk=1
    )
    publication.save()
    publication = G(
        Publication,
        title='title',
        author=user,
        pub_date=timezone.now(),
        text='hello world !',
        is_draft=False,
        pk=2
    )
    publication.save()

    user = User.objects.get(username='publisher2')
    publication = G(
        Publication,
        title='title',
        author=user,
        pub_date=timezone.now(),
        text='hello world !',
        pk=3
    )
    publication.save()
    publication = G(
        Publication,
        title='title',
        author=user,
        pub_date=timezone.now(),
        text='hello world !',
        is_draft=False,
        pk=4
    )
    publication.save()


class PublicationsIntegrationTests(TestCase):

    def setUp(self):
        PublicatonSetUp()

    def test_index_view(self):
        resp = self.client.get(reverse('publications:index'))
        self.assertEqual(resp.status_code, 200)

    def test_index_view_type_n(self):
        resp = self.client.get(reverse('publications:index')+'?type=N')
        self.assertEqual(resp.status_code, 200)

    def test_index_view_type_t(self):
        resp = self.client.get(reverse('publications:index')+'?type=T')
        self.assertEqual(resp.status_code, 200)

    def test_index_view_type_p(self):
        resp = self.client.get(reverse('publications:index')+'?type=P')
        self.assertEqual(resp.status_code, 200)

    def test_index_view_page_two(self):
        resp = self.client.get(reverse('publications:index')+'?page=2')
        self.assertEqual(resp.status_code, 200)

    def test_index_view_page_nonexistant(self):
        resp = self.client.get(reverse('publications:index')+'?page=999999')
        self.assertEqual(resp.status_code, 200)

    def test_index_view_page_none(self):
        resp = self.client.get(reverse('publications:index')+'?page=')
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_draft(self):
        resp = self.client.get(reverse('publications:detail', args=[1]))
        self.assertEqual(resp.status_code, 302)

    def test_detail_view_notdraft(self):
        resp = self.client.get(reverse('publications:detail', args=[2]))
        self.assertEqual(resp.status_code, 200)

    def test_create_view(self):
        resp = self.client.get(reverse('publications:create'))
        self.assertEqual(resp.status_code, 302)

    def test_edit_view(self):
        resp = self.client.get(reverse('publications:edit', args=[1]))
        self.assertEqual(resp.status_code, 302)


class AuthenticatedPublicationsIntegrationTests(TestCase):

    def setUp(self):
        PublicatonSetUp()
        self.client.login(username='member', password='password')

    def test_index_view(self):
        resp = self.client.get(reverse('publications:index'))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_draft(self):
        resp = self.client.get(reverse('publications:detail', args=[1]))
        self.assertEqual(resp.status_code, 403)

    def test_detail_view_notdraft(self):
        resp = self.client.get(reverse('publications:detail', args=[2]))
        self.assertEqual(resp.status_code, 200)

    def test_create_view(self):
        resp = self.client.get(reverse('publications:create'))
        self.assertEqual(resp.status_code, 403)

    def test_edit_view(self):
        resp = self.client.get(reverse('publications:edit', args=[1]))
        self.assertEquals(resp.status_code, 403)


class PublisherPublicationsIntegrationTests(TestCase):

    def setUp(self):
        PublicatonSetUp()
        self.client.login(username='publisher1', password='password')

    def test_index_view(self):
        resp = self.client.get(reverse('publications:index'))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_own_draft(self):
        resp = self.client.get(reverse('publications:detail', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_own_notdraft(self):
        resp = self.client.get(reverse('publications:detail', args=[2]))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_notown_draft(self):
        resp = self.client.get(reverse('publications:detail', args=[3]))
        self.assertEqual(resp.status_code, 403)

    def test_detail_view_notown_notdraft(self):
        resp = self.client.get(reverse('publications:detail', args=[4]))
        self.assertEqual(resp.status_code, 200)

    def test_create_view(self):
        resp = self.client.get(reverse('publications:create'))
        self.assertEqual(resp.status_code, 200)

    def test_edit_view_own(self):
        resp = self.client.get(reverse('publications:edit', args=[1]))
        self.assertEquals(resp.status_code, 200)

    def test_edit_view_notown(self):
        resp = self.client.get(reverse('publications:edit', args=[3]))
        self.assertEquals(resp.status_code, 403)

    def test_create_action(self):
        data = {
            'title': 'Test_create_action',
            'text': 'This is a test !',
            'is_draft': 1,
            'type': 'P',
        }
        resp = self.client.post(reverse('publications:create'), data)
        self.assertEqual(resp.status_code, 302)


class AdminPublicationsIntegrationTests(TestCase):

    def setUp(self):
        PublicatonSetUp()
        self.client.login(username='admin', password='password')

    def test_index_view(self):
        resp = self.client.get(reverse('publications:index'))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_draft(self):
        resp = self.client.get(reverse('publications:detail', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_notdraft(self):
        resp = self.client.get(reverse('publications:detail', args=[2]))
        self.assertEqual(resp.status_code, 200)

    def test_create_view(self):
        resp = self.client.get(reverse('publications:create'))
        self.assertEqual(resp.status_code, 200)

    def test_edit_view_draft(self):
        resp = self.client.get(reverse('publications:edit', args=[1]))
        self.assertEquals(resp.status_code, 200)

    def test_edit_view_notdraft(self):
        resp = self.client.get(reverse('publications:edit', args=[2]))
        self.assertEquals(resp.status_code, 200)
