from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django_dynamic_fixture import G

from iTeam.publications.models import Publication
from iTeam.member.models import Profile

# Create your tests here.

def setUpPublication(self):
        # Create user
        self.user = G(User, username='user42')
        self.user.set_password('password')
        self.user.save()

        profile = G(Profile, user=self.user)
        profile.is_publisher = True
        profile.save()

        # Authenticate user
        self.client.login(username='user42', password='password')

        # Create one publication
        publication = G(Publication,
            title = 'title',
            author = self.user,
            pub_date = timezone.now(),
            text = 'hello world !',
            is_draft = False,
            pk = 1)
        publication.save()

        self.client.logout()

class PublicationsIntegrationTests(TestCase):

    def setUp(self):
        setUpPublication(self)

    def test_index(self):
        resp = self.client.get(reverse('publications:index'))
        self.assertEqual(resp.status_code, 200)

    def test_detail(self):
        resp = self.client.get(reverse('publications:detail', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_create(self):
        resp = self.client.get(reverse('publications:create'))
        self.assertEqual(resp.status_code, 302)

    def test_edit(self):
        resp = self.client.get(reverse('publications:edit', args=[1]))
        self.assertEqual(resp.status_code, 302)


class AuthenticatedPublicationsIntegrationTests(TestCase):

    def setUp(self):
        setUpPublication(self)

        # Create user
        self.user = G(User, username='user43')
        self.user.set_password('password')
        self.user.save()

        profile = G(Profile, user=self.user)
        profile.save()

        # Authenticate user
        self.client.login(username='user43', password='password')

    def test_create(self):
        resp = self.client.get(reverse('publications:create'))
        self.assertEqual(resp.status_code, 403)

    def test_edit(self):
        resp = self.client.get(reverse('publications:edit', args=[1]))
        self.assertEquals(resp.status_code, 403)


class AuthenticatedAndPublisherPublicationsIntegrationTests(TestCase):

    def setUp(self):
        setUpPublication(self)

        # Authenticate user
        self.client.login(username='user42', password='password')

    def test_create(self):
        resp = self.client.get(reverse('publications:create'))
        self.assertEqual(resp.status_code, 200)

    def test_edit(self):
        resp = self.client.get(reverse('publications:edit', args=[1]))
        self.assertEquals(resp.status_code, 200)

