
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_dynamic_fixture import G

from iTeam.member.models import Profile


def MemberSetUp():
    user = G(User, username='member')
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
    profile.save()


class MemberIntegrationTests(TestCase):

    def setUp(self):
        MemberSetUp()

    def test_index_view(self):
        resp = self.client.get(reverse('member:index'))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view(self):
        resp = self.client.get(reverse('member:detail', args=['member']))
        self.assertEqual(resp.status_code, 200)

    def test_settings_view(self):
        resp = self.client.get(reverse('member:settings_view'))
        self.assertEqual(resp.status_code, 302)

    def test_publications_view(self):
        resp = self.client.get(reverse('member:publications'))
        self.assertEqual(resp.status_code, 302)

    def test_events_view(self):
        resp = self.client.get(reverse('member:events'))
        self.assertEqual(resp.status_code, 302)

    def test_register_view(self):
        resp = self.client.get(reverse('member:register_view'))
        self.assertEqual(resp.status_code, 200)

    def test_login_view(self):
        resp = self.client.get(reverse('member:login_view'))
        self.assertEqual(resp.status_code, 200)

    def test_login_action(self):
        user = User.objects.get(username='member')
        data = {
            'username': 'member',
            'password': 'password'
        }
        self.client.post(reverse('member:login_view'), data)
        self.assertEqual(self.client.session['_auth_user_id'], user.pk)

    def test_logout_view(self):
        resp = self.client.get(reverse('member:logout_view'))
        self.assertEqual(resp.status_code, 302)


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

    def test_publications_view(self):
        resp = self.client.get(reverse('member:publications'))
        self.assertEqual(resp.status_code, 403)

    def test_events_view(self):
        resp = self.client.get(reverse('member:events'))
        self.assertEqual(resp.status_code, 403)

    def test_register_view(self):
        resp = self.client.get(reverse('member:register_view'))
        self.assertEquals(resp.status_code, 200)

    def test_login_view(self):
        resp = self.client.get(reverse('member:login_view'))
        self.assertEquals(resp.status_code, 200)

    def test_logout_view(self):
        resp = self.client.get(reverse('member:logout_view'))
        self.assertEquals(resp.status_code, 200)


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

    def test_publications_view(self):
        resp = self.client.get(reverse('member:publications'))
        self.assertEqual(resp.status_code, 200)

    def test_events_view(self):
        resp = self.client.get(reverse('member:events'))
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

    def test_publications_view(self):
        resp = self.client.get(reverse('member:publications'))
        self.assertEqual(resp.status_code, 200)

    def test_events_view(self):
        resp = self.client.get(reverse('member:events'))
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
