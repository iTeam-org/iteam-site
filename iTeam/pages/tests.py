# coding: utf-8

"""Tests for pages app."""

from django.test import TestCase

from django.core.urlresolvers import reverse


class PagesIntegrationTests(TestCase):

    def test_home(self):
        """Test if the index URL for homepage is ok."""
        resp = self.client.get(reverse('iTeam.pages.views.home'))
        self.assertEquals(200, resp.status_code)

    def test_apropos(self):
        resp = self.client.get(reverse('pages:apropos'))
        self.assertEquals(200, resp.status_code)

