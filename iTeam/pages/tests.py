#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-20 11:52:21
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-08-22 17:02:41

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
from django.test import TestCase


class PagesIntegrationTests(TestCase):

    def test_home_view(self):
        resp = self.client.get(reverse('iTeam.pages.views.home'))
        self.assertEquals(200, resp.status_code)

    def test_apropos_view(self):
        resp = self.client.get(reverse('pages:apropos'))
        self.assertEquals(200, resp.status_code)

    def test_hallOfFame_view(self):
        resp = self.client.get(reverse('pages:hallOfFame'))
        self.assertEquals(200, resp.status_code)

    def test_cookies_view(self):
        resp = self.client.get(reverse('pages:cookies'))
        self.assertEquals(200, resp.status_code)
