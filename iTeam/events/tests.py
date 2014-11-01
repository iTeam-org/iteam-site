#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-20 14:50:12
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-11-01 14:17:14

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


from datetime import datetime
import pytz

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django_dynamic_fixture import G

from iTeam.events.models import Event
from iTeam.member.tests import MemberSetUp


def EventSetUp():
    MemberSetUp()

    user = User.objects.get(username='publisher1')
    event = G(
        Event,
        title='title',
        author=user,
        place='somewhere',
        date_start=datetime(year=2014, month=9, day=2, hour=10, minute=30, tzinfo=pytz.utc),
        text='hello world !',
        pk=1
    )
    event.save()
    event = G(
        Event,
        title='title',
        author=user,
        place='somewhere',
        date_start=datetime(year=2014, month=9, day=2, hour=12, minute=30, tzinfo=pytz.utc),
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
        date_start=datetime(year=2020, month=9, day=2, hour=14, minute=30, tzinfo=pytz.utc),
        text='hello world !',
        pk=3
    )
    event.save()
    event = G(
        Event,
        title='title',
        author=user,
        place='somewhere',
        date_start=datetime(year=2020, month=9, day=2, hour=16, minute=30, tzinfo=pytz.utc),
        text='hello world !',
        is_draft=False,
        type='B',
        pk=4
    )
    event.save()
    event = G(
        Event,
        title='title',
        author=user,
        place='somewhere',
        date_start=datetime(year=2020, month=9, day=2, hour=16, minute=30, tzinfo=pytz.utc),
        text='hello world !',
        is_draft=False,
        type='F',
        pk=5
    )
    event.save()


class EventsIntegrationTests(TestCase):

    def setUp(self):
        EventSetUp()

    def test_list_view(self):
        resp = self.client.get(reverse('events:index_list'))
        self.assertEqual(resp.status_code, 200)

    def test_index_view_page_two(self):
        resp = self.client.get(reverse('events:index_list')+'?page=2')
        self.assertEqual(resp.status_code, 200)

    def test_index_view_page_nonexistant(self):
        resp = self.client.get(reverse('events:index_list')+'?page=999999')
        self.assertEqual(resp.status_code, 200)

    def test_index_view_page_none(self):
        resp = self.client.get(reverse('events:index_list')+'?page=')
        self.assertEqual(resp.status_code, 200)

    def test_week_view_zero(self):
        resp = self.client.get(reverse('events:index_week', args=[0]))
        self.assertEqual(resp.status_code, 200)

    def test_week_view_today(self):
        resp = self.client.get(reverse('events:index_week', args=[16314]))
        self.assertEqual(resp.status_code, 200)

    def test_month_view_today(self):
        resp = self.client.get(reverse('events:index_month', args=[2014, 9]))
        self.assertEqual(resp.status_code, 200)

    def test_month_view_jan(self):
        resp = self.client.get(reverse('events:index_month', args=[2014, 1]))
        self.assertEqual(resp.status_code, 200)

    def test_month_view_error_year(self):
        resp = self.client.get(reverse('events:index_month', args=[42, 1]))
        self.assertEqual(resp.status_code, 200)

    def test_month_view_error_month(self):
        resp = self.client.get(reverse('events:index_month', args=[2014, 20]))
        self.assertEqual(resp.status_code, 200)

    def test_month_view_dec(self):
        resp = self.client.get(reverse('events:index_month', args=[2014, 12]))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_draft(self):
        e = Event.objects.get(pk=1)
        resp = self.client.get(e.get_absolute_url())
        self.assertEqual(resp.status_code, 302)

    def test_detail_view_notdraft(self):
        e = Event.objects.get(pk=2)
        resp = self.client.get(e.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_create_view(self):
        resp = self.client.get(reverse('events:create'))
        self.assertEqual(resp.status_code, 302)

    def test_edit_view(self):
        resp = self.client.get(reverse('events:edit', args=[1]))
        self.assertEqual(resp.status_code, 302)

    def test_detail_view_invalid_slug(self):
        e = Event.objects.get(pk=1)
        url = e.get_absolute_url()[::-1][2:][::-1]  # truncate the end of the slug
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 301)

    def test_by_author_view(self):
        resp = self.client.get(reverse('events:by_author', args=['publisher1']))
        self.assertEqual(resp.status_code, 200)


class AuthenticatedEventsIntegrationTests(TestCase):

    def setUp(self):
        EventSetUp()
        self.client.login(username='member', password='password')

    def test_list_view(self):
        resp = self.client.get(reverse('events:index_list'))
        self.assertEqual(resp.status_code, 200)

    def test_week_view(self):
        resp = self.client.get(reverse('events:index_week', args=[0]))
        self.assertEqual(resp.status_code, 200)

    def test_month_view(self):
        resp = self.client.get(reverse('events:index_month', args=[2014, 8]))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_draft(self):
        e = Event.objects.get(pk=1)
        resp = self.client.get(e.get_absolute_url())
        self.assertEqual(resp.status_code, 403)

    def test_detail_view_notdraft(self):
        e = Event.objects.get(pk=2)
        resp = self.client.get(e.get_absolute_url())
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
        resp = self.client.get(reverse('events:index_week', args=[0]))
        self.assertEqual(resp.status_code, 200)

    def test_month_view(self):
        resp = self.client.get(reverse('events:index_month', args=[2014, 8]))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_own_draft(self):
        e = Event.objects.get(pk=1)
        resp = self.client.get(e.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_own_notdraft(self):
        e = Event.objects.get(pk=2)
        resp = self.client.get(e.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_notown_draft(self):
        e = Event.objects.get(pk=3)
        resp = self.client.get(e.get_absolute_url())
        self.assertEqual(resp.status_code, 403)

    def test_detail_view_notown_notdraft(self):
        e = Event.objects.get(pk=4)
        resp = self.client.get(e.get_absolute_url())
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

    def test_create_action(self):
        data = {
            'title': 'Test_create_action',
            'place': 'Somewhere',
            'date_start': '2014-09-01 12:30:00',
            'text': 'This is a test !',
            'is_draft': 1,
            'type': 'O',
        }
        resp = self.client.post(reverse('events:create'), data)
        self.assertEqual(resp.status_code, 302)

        data = {
            'title': 'Test_create_action',
            'place': 'Somewhere',
            'date_start': '2014-09-01 12:30:00',
            'text': 'This is a test !',
            'is_draft': 0,
            'type': 'O',
        }
        resp = self.client.post(reverse('events:create'), data)
        self.assertEqual(resp.status_code, 302)


class AdminEventsIntegrationTests(TestCase):

    def setUp(self):
        EventSetUp()
        self.client.login(username='admin', password='password')

    def test_list_view(self):
        resp = self.client.get(reverse('events:index_list'))
        self.assertEqual(resp.status_code, 200)

    def test_week_view(self):
        resp = self.client.get(reverse('events:index_week', args=[0]))
        self.assertEqual(resp.status_code, 200)

    def test_month_view(self):
        resp = self.client.get(reverse('events:index_month', args=[2014, 8]))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_draft(self):
        e = Event.objects.get(pk=1)
        resp = self.client.get(e.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_notdraft(self):
        e = Event.objects.get(pk=2)
        resp = self.client.get(e.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_create_view(self):
        resp = self.client.get(reverse('events:create'))
        self.assertEqual(resp.status_code, 200)

    def test_edit_view(self):
        resp = self.client.get(reverse('events:edit', args=[1]))
        self.assertEqual(resp.status_code, 200)
