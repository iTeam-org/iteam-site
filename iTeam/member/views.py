#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-20 18:26:44
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-11-05 10:44:35

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

import uuid
import string
import random

from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.http import HttpResponse
from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from iTeam.member.models import Profile, ForgotPasswordToken, send_templated_mail
from iTeam.member.forms import LoginForm, RegisterForm, SettingsPasswordForm, SettingsOtherForm, LostPasswordForm
from iTeam.publications.models import Publication
from iTeam.events.models import Event


def index(request):
    members = User.objects.all().order_by('-date_joined')

    paginator = Paginator(members, settings.NB_MEMBERS_PER_PAGE)
    page = request.GET.get('page')

    try:
        shown_members = paginator.page(page)
    except PageNotAnInteger:
        shown_members = paginator.page(1)
    except EmptyPage:
        shown_members = paginator.page(paginator.num_pages)

    return render(request, 'member/index.html', {
        'data': shown_members,
        'members_count': members.count(),
    })


def detail(request, user_name):
    user = get_object_or_404(User, username=user_name)
    profile = get_object_or_404(Profile, user=user)
    profileRequest = None

    # admin actions
    if request.user.is_authenticated():
        profileRequest = get_object_or_404(Profile, user=request.user)

        if profileRequest.is_admin and request.method == 'POST':
            need_redirect = False

            if 'toggle_is_publisher' in request.POST:
                profile.is_publisher = not profile.is_publisher
                profile.save()
                need_redirect = True
            if 'toggle_is_admin' in request.POST:
                profile.is_admin = not profile.is_admin
                profile.is_publisher = profile.is_admin
                profile.save()
                need_redirect = True

            if need_redirect:
                redirect(reverse('member:detail', args=[user_name]))

    c = {
        'profile_detail': profile,
        'profile_request': profileRequest,
    }

    return render(request, 'member/detail.html', c)


@sensitive_post_parameters('password')
def login_view(request):
    csrf_tk = {}
    csrf_tk.update(csrf(request))

    if 'next' in request.GET:
        csrf_tk['next'] = request.GET['next']

    error = False

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                # Yeah auth successful
                if user.is_active:
                    login(request, user)
                    if 'auto_login' not in request.POST:
                        request.session.set_expiry(0)

                    if 'next' in request.GET:
                        return redirect(request.GET['next'])
                    else:
                        return redirect(reverse('iTeam.pages.views.home'))
                else:
                    error = (u'Le compte a été désactivé. Pour toute '
                             u'réclamation, merci de contacter '
                             u'l\'administrateur.')
            else:
                # auth failed
                error = u'Les identifiants fournis ne sont pas valides.'
        else:
            error = (u'Veuillez spécifier votre identifiant '
                     u'et votre mot de passe.')
    else:
        form = LoginForm()

    csrf_tk['error'] = error
    csrf_tk['form'] = form

    return render(request, 'member/login.html', csrf_tk)


@login_required
def logout_view(request):
    # If we got a secure POST, we disconnect
    if request.method == 'POST':
        logout(request)
        request.session.clear()  # clean explicitly stored data about the user
        return redirect(reverse('iTeam.pages.views.home'))
    # Elsewise we ask the user to submit a form with correct csrf token
    else:
        return render(request, 'member/logout.html')


@sensitive_post_parameters('password', 'password_confirm')
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password']
            )

            profile = Profile(user=user)
            profile.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            return render(request, 'member/register_success.html')
    else:  # method == GET
        form = RegisterForm()
    return render(request, 'member/register.html', {'form': form})


def password_reset_ask(request):
    if request.method == 'POST':
        form = LostPasswordForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            user = get_object_or_404(User, username=username)

            # Generate a new token
            token = ForgotPasswordToken()
            token.user = user
            token.token = str(uuid.uuid4())
            token.expires = timezone.now() + settings.FORGOT_PASSWORD_TOKEN_EXPIRES
            token.save()

            # send mail
            subject = '[iteam.org] Réinitialisation du mot de passe'
            context = {
                'username': token.user.username,
                'link': token.get_absolute_url(),
            }
            send_templated_mail(subject, 'mail/password_reset.txt', context, (token.user.email,))

            return render(request, 'member/password_reset_confirm.html')
    else:
        form = LostPasswordForm()

    return render(request, 'member/password_reset.html', {'form': form})


def password_reset_confirm(request, token):
    if not request.user.is_authenticated():
        token = get_object_or_404(ForgotPasswordToken, token=token)

        if token.expires > timezone.now():
            user = token.user

            # Set a new password
            length = 10
            chars = string.ascii_letters + string.digits
            password = ''.join(random.choice(chars) for _ in range(length))
            user.set_password(password)
            user.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            token.delete()

            return render(request, 'member/password_reset_changed.html', {'new_password': password})
        else:
            token.delete()
            return HttpResponse('Erreur : le token a expiré, merci de recommencer.')
    else:
        raise PermissionDenied


@login_required
@sensitive_post_parameters('password_old', 'password_new', 'password_confirm')
def settings_view(request):
    p = get_object_or_404(Profile, user=request.user)

    formPassword = SettingsPasswordForm(request.user)
    formOther = SettingsOtherForm({'avatar_url':p.avatar_url, 'show_email': p.show_email })
    msg = ''

    if request.method == 'POST' and 'form' in request.POST:
        if 'password' == request.POST['form']:
            formPassword = SettingsPasswordForm(request.user, request.POST)

            if formPassword.is_valid():
                request.user.set_password(formPassword.cleaned_data['password_new'])
                request.user.save()

                msg = u'Le mot de passe a bien été modifié.'
        elif 'other' == request.POST['form']:
            formOther = SettingsOtherForm(request.POST)

            if formOther.is_valid():
                data = formOther.cleaned_data
                if 'avatar_url' in data:
                    p.avatar_url = data['avatar_url']
                p.show_email = data['show_email']
                p.save()

                msg = u'Le compte a bien été modifié.'

    c = {
        'formPassword': formPassword,
        'formOther': formOther,
        'msg': msg,
    }

    return render(request, 'member/settings_account.html', c)
