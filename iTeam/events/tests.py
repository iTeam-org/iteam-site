#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-20 14:50:12
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-08-22 17:07:09

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

from iTeam.events.models import Event
from iTeam.member.models import Profile
from iTeam.member.tests import MemberSetUp


def EventSetUp():
    MemberSetUp()

    user = User.objects.get(username='publisher1')
    event = G(
        Event,
        title='title',
        author=user,
        place='somewhere',
        date_start=timezone.now(),
        text='hello world !',
        pk=1
    )
    event.save()
    event = G(
        Event,
        title='title',
        author=user,
        place='somewhere',
        date_start=timezone.now(),
        text='hello world !',
        is_draft=False,
        pk=2
    )
    event.save()

    user = User.objects.get(username='publisher2')
    event = G(
        Event,
        title='title',
        author=user,
        place='somewhere',
        date_start=timezone.now(),
        text='hello world !',
        pk=1
    )
    event.save()
    event = G(
        Event,
        title='title',
        author=user,
        place='somewhere',
        date_start=timezone.now(),
        text='hello world !',
        is_draft=False,
        pk=2
    )
    event.save()


class EventsIntegrationTests(TestCase):

    def setUp(self):
        EventSetUp()

    def test_list_view(self):
        resp = self.client.get(reverse('events:index_list'))
        self.assertEqual(resp.status_code, 200)

    def test_week_view(self):
        resp = self.client.get(reverse('events:index_week', args=[2014, 8, 1]))
        self.assertEqual(resp.status_code, 200)

    def test_month_view(self):
        resp = self.client.get(reverse('events:index_month', args=[2014, 8]))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_draft(self):
        resp = self.client.get(reverse('events:detail', args=[1]))
        self.assertEqual(resp.status_code, 302)

    def test_detail_view_notdraft(self):
        resp = self.client.get(reverse('events:detail', args=[2]))
        self.assertEqual(resp.status_code, 200)

    def test_create_view(self):
        resp = self.client.get(reverse('events:create'))
        self.assertEqual(resp.status_code, 302)

    def test_edit_view(self):
        resp = self.client.get(reverse('events:edit', args=[1]))
        self.assertEqual(resp.status_code, 302)


class AuthenticatedEventsIntegrationTests(TestCase):

    def setUp(self):
        EventSetUp()
        self.client.login(username='member', password='password')

    def test_list_view(self):
        resp = self.client.get(reverse('events:index_list'))
        self.assertEqual(resp.status_code, 200)

    def test_week_view(self):
        resp = self.client.get(reverse('events:index_week', args=[2014, 8, 1]))
        self.assertEqual(resp.status_code, 200)

    def test_month_view(self):
        resp = self.client.get(reverse('events:index_month', args=[2014, 8]))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_draft(self):
        resp = self.client.get(reverse('events:detail', args=[1]))
        self.assertEqual(resp.status_code, 403)

    def test_detail_view_notdraft(self):
        resp = self.client.get(reverse('events:detail', args=[2]))
        self.assertEqual(resp.status_code, 200)

    def test_create_view(self):
        resp = self.client.get(reverse('events:create'))
        self.assertEqual(resp.status_code, 403)

    def test_edit_view(self):
        resp = self.client.get(reverse('events:edit', args=[1]))
        self.assertEqual(resp.status_code, 403)


class PublisherEventsIntegrationTests(TestCase):

    def setUp(self):
        EventSetUp()
        self.client.login(username='publisher1', password='password')

    def test_list_view(self):
        resp = self.client.get(reverse('events:index_list'))
        self.assertEqual(resp.status_code, 200)

    def test_week_view(self):
        resp = self.client.get(reverse('events:index_week', args=[2014, 8, 1]))
        self.assertEqual(resp.status_code, 200)

    def test_month_view(self):
        resp = self.client.get(reverse('events:index_month', args=[2014, 8]))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_own_draft(self):
        resp = self.client.get(reverse('events:detail', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_own_notdraft(self):
        resp = self.client.get(reverse('events:detail', args=[2]))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_notown_draft(self):
        resp = self.client.get(reverse('events:detail', args=[3]))
        self.assertEqual(resp.status_code, 403)

    def test_detail_view_notown_notdraft(self):
        resp = self.client.get(reverse('events:detail', args=[4]))
        self.assertEqual(resp.status_code, 200)

    def test_create_view(self):
        resp = self.client.get(reverse('events:create'))
        self.assertEqual(resp.status_code, 200)

    def test_edit_view_own(self):
        resp = self.client.get(reverse('events:edit', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_edit_view_not_own(self):
        resp = self.client.get(reverse('events:edit', args=[3]))
        self.assertEqual(resp.status_code, 403)


class AdminEventsIntegrationTests(TestCase):

    def setUp(self):
        EventSetUp()
        self.client.login(username='admin', password='password')

    def test_list_view(self):
        resp = self.client.get(reverse('events:index_list'))
        self.assertEqual(resp.status_code, 200)

    def test_week_view(self):
        resp = self.client.get(reverse('events:index_week', args=[2014, 8, 1]))
        self.assertEqual(resp.status_code, 200)

    def test_month_view(self):
        resp = self.client.get(reverse('events:index_month', args=[2014, 8]))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_draft(self):
        resp = self.client.get(reverse('events:detail', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_notdraft(self):
        resp = self.client.get(reverse('events:detail', args=[2]))
        self.assertEqual(resp.status_code, 200)

    def test_create_view(self):
        resp = self.client.get(reverse('events:create'))
        self.assertEqual(resp.status_code, 200)

    def test_edit_view(self):
        resp = self.client.get(reverse('events:edit', args=[1]))
        self.assertEqual(resp.status_code, 200)
