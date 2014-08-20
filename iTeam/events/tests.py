
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
    event = G(Event,
        title = 'title',
        author = user,
        place = 'somewhere',
        date_start = timezone.now(),
        text = 'hello world !',
        pk = 1
    )
    event.save()
    event = G(Event,
        title = 'title',
        author = user,
        place = 'somewhere',
        date_start = timezone.now(),
        text = 'hello world !',
        is_draft = False,
        pk = 2
    )
    event.save()

    user = User.objects.get(username='publisher2')
    event = G(Event,
        title = 'title',
        author = user,
        place = 'somewhere',
        date_start = timezone.now(),
        text = 'hello world !',
        pk = 1
    )
    event.save()
    event = G(Event,
        title = 'title',
        author = user,
        place = 'somewhere',
        date_start = timezone.now(),
        text = 'hello world !',
        is_draft = False,
        pk = 2
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
