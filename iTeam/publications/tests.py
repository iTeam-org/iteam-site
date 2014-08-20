
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django_dynamic_fixture import G

from iTeam.publications.models import Publication
from iTeam.member.models import Profile
from iTeam.member.tests import MemberSetUp


def PublicatonSetUp():
    MemberSetUp()

    user = User.objects.get(username='publisher1')
    publication = G(Publication,
        title = 'title',
        author = user,
        pub_date = timezone.now(),
        text = 'hello world !',
        pk = 1
    )
    publication.save()
    publication = G(Publication,
        title = 'title',
        author = user,
        pub_date = timezone.now(),
        text = 'hello world !',
        is_draft = False,
        pk = 2
    )
    publication.save()

    user = User.objects.get(username='publisher2')
    publication = G(Publication,
        title = 'title',
        author = user,
        pub_date = timezone.now(),
        text = 'hello world !',
        pk = 3
    )
    publication.save()
    publication = G(Publication,
        title = 'title',
        author = user,
        pub_date = timezone.now(),
        text = 'hello world !',
        is_draft = False,
        pk = 4
    )
    publication.save()


class PublicationsIntegrationTests(TestCase):

    def setUp(self):
        PublicatonSetUp()

    def test_index_view(self):
        resp = self.client.get(reverse('publications:index'))
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
