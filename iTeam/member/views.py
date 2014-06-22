# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.


from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.views.decorators.debug import sensitive_post_parameters

from iTeam.member.models import Profile
from iTeam.member.forms import LoginForm, RegisterForm, SettingsForm

###############################
from hashlib import md5
from time import time


def generate_token():
    return md5('lcdldses?nas. {0} salt'.format(time())).hexdigest()[:12]
##############################

def index(request):
    """
        Display list of registered users.
    """
    members = User.objects.all().order_by('-date_joined')

    paginator = Paginator(members, settings.NB_MEMBERS_PER_PAGE)
    page = request.GET.get('page')

    try:
        shown_members = paginator.page(page)
        page = int(page)
    except PageNotAnInteger:
        shown_members = paginator.page(1)
        page = 1
    except EmptyPage:
        shown_members = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'member/index.html', {
        'data': shown_members,
        'members_count': members.count(),
    })


def detail(request, user_name):
    """
        Display details about a profile.
    """
    user = get_object_or_404(User, username=user_name)

    return render(request, 'member/detail.html', {'member': user})


@sensitive_post_parameters('password')
def login_view(request):
    """
        Allow users to log into their accounts.

        If the 'suivant' HTTP GET field is given, then this view will redirect the
        user to the given URL after successful auth.
    """
    csrf_tk = {}
    csrf_tk.update(csrf(request))

    if 'suivant' in request.GET:
        csrf_tk['next'] = request.GET['suivant']

    error = False
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
            # Yeah auth successful
                login(request, user)
                request.session['get_token'] = generate_token()

                if 'remember' not in request.POST:
                    request.session.set_expiry(0)

                if 'suivant' in request.GET:
                    return redirect(request.GET['suivant'])
                else:
                    return redirect(reverse('iTeam.pages.views.home'))
            else:
            # auth failed
                error = u'Les identifiants fournis ne sont pas valides'
        else:
            error = (u'Veuillez spécifier votre identifiant '
                     u'et votre mot de passe')
    else:
        form = LoginForm()

    csrf_tk['error'] = error
    csrf_tk['form'] = form

    return render(request, 'member/login.html', csrf_tk)


@login_required(redirect_field_name='suivant')
def logout_view(request):
    """
        Allow users to log out of their accounts.
    """
    # If we got a secure POST, we disconnect
    if request.method == 'POST':
        logout(request)
        request.session.clear()
        return redirect(reverse('iTeam.pages.views.home'))

    # Elsewise we ask the user to submit a form with correct csrf token
    return render(request, 'member/logout.html')


@sensitive_post_parameters('password', 'password_confirm')
def register_view(request):
    """
        Allow new users to register, creating them an account.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.data
            user = User.objects.create_user(
                data['username'],
                data['email'],
                data['password'])

            profile = Profile(user=user, promo=0)
            profile.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)

            return render(request, 'member/register_success.html')
        else:
            return render(request, 'member/register.html', {'form': form})

    form = RegisterForm()
    return render(request, 'member/register.html', {
        'form': form
    })


@login_required(redirect_field_name='suivant')
def settings_view(request):
    """
        Set current user's account settings.
    """
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        c = {
            'form': form,
        }
        if form.is_valid():
            request.user.set_password(form.data['password_new'])
            request.user.save()

            messages.success(request, u'Le mot de passe a bien été modifié.')
            return redirect('/membres/parametres/profil')

        else:
            return render(request, 'member/settings_account.html', c)
    else:
        form = SettingsForm(request.user)
        c = {
            'form': form,
        }
        return render(request, 'member/settings_account.html', c)
