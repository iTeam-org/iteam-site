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

"""Member app's views."""

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
from iTeam.member.forms import LoginForm, ProfileForm, RegisterForm, \
    ChangePasswordForm


###############################
from hashlib import md5
from time import time


def generate_token():
    return md5('lcdldses?nas. {0} salt'.format(time())).hexdigest()[:12]
##############################

def index(request):
    """Display list of registered users.

    Returns:
        HttpResponse

    """
    #members = User.objects.all().order_by('-date_joined')
    members = Profile.objects.all()

    """
    paginator = Paginator(members, settings.MEMBERS_PER_PAGE)
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
    """
    return render(request, 'member/index.html', {
        'members': members, #shown_members
        'members_count': members.count(),
        'pages': 1,#range(1, paginator.num_pages), #paginator_range(page, paginator.num_pages),
        'nb': None,
    })


@login_required(redirect_field_name='suivant')
def actions(request):
    """Show avaible actions for current user, like a customized homepage.

    This may be very temporary.

    Returns:
        HttpResponse

    """

    # TODO: Seriously improve this page, and see if cannot be merged in
    #       pdp.pages.views.home since it will be more coherent to give an
    #       enhanced homepage for registered users

    return render(request, 'member/actions.html')


def details(request, user_name):
    """Display details about a profile.

    Returns:
        HttpResponse

    """
    usr = get_object_or_404(User, username=user_name)

    return render(request, 'member/detail.html', {'member': usr})


@sensitive_post_parameters('password')
def login_view(request):
    """Allow users to log into their accounts.

    If the `suivant` HTTP GET field is given, then this view will redirect the
    user to the given URL after successful auth.

    Returns:
        HttpResponse

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
    """Allow users to log out of their accounts.

    Returns:
        HttpResponse

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
    """Allow new users to register, creating them an account.

    Returns:
        HttpResponse

    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.data
            user = User.objects.create_user(
                data['username'],
                data['email'],
                data['password'])

            profile = Profile(user=user, show_email=False)
            profile.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            if settings.BOT_ENABLED:
                bot.send_welcome_private_message(user)

            login(request, user)

            return render(request, 'member/register_success.html')
        else:
            return render(request, 'member/register.html', {'form': form})

    form = RegisterForm()
    return render(request, 'member/register.html', {
        'form': form
    })


# Settings for public profile

@login_required(redirect_field_name='suivant')
def settings(request):
    """Set current user's account settings.

    Returns:
        HttpResponse

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
        form = ChangePasswordForm(request.user)
        c = {
            'form': form,
        }
        return render(request, 'member/settings_account.html', c)
