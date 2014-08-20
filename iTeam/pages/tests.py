
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
