#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-20 19:01:30
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-11-05 10:39:26

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


from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):

    username = forms.CharField(
        label='Identifiant',
        widget=forms.TextInput(
            attrs={
                'autofocus': '',
                'placeholder': 'Identifiant'
            }
        )
    )
    password = forms.CharField(
        label='Mot magique',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Mot magique'
            }
        )
    )
    auto_login = forms.BooleanField(label='Connexion automatique', required=False)


class RegisterForm(forms.Form):

    username = forms.CharField(
        label='Nom d\'utilisateur',
        widget=forms.TextInput(
            attrs={
                'autofocus': '',
                'placeholder': 'Nom d\'utilisateur'
            }
        )
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Mot de passe'
            }
        )
    )
    password_confirm = forms.CharField(
        label='Confirmation',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmation'
            }
        )
    )
    email = forms.EmailField(
        label='Email',
        error_messages={'invalid': 'Saisissez une adresse email valable.'},
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email'
            }
        )
    )

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        # Check that the password and it's confirmation match
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if not password_confirm == password:
            msg = u'Les mots de passe sont différents.'
            self._errors['password'] = self.error_class([msg])
            self._errors['password_confirm'] = self.error_class([msg])

            if 'password' in cleaned_data:
                del cleaned_data['password']

            if 'password_confirm' in cleaned_data:
                del cleaned_data['password_confirm']

        # Check that the user doesn't exist yet
        username = cleaned_data.get('username')

        if username is not None:
            if username.strip() == '':
                msg = u'Le nom d\'utilisateur ne peut-être vide'
                self._errors['username'] = self.error_class([msg])
            elif User.objects.filter(username=username).count() > 0:
                msg = u'Ce nom d\'utilisateur est déjà utilisé.'
                self._errors['username'] = self.error_class([msg])
            # Forbid the use of comma in the username
            elif username is not None and ',' in username:
                msg = u'Le nom d\'utilisateur ne peut contenir de virgules.'
                self._errors['username'] = self.error_class([msg])
            elif username != username.strip():
                msg = u'Le nom d\'utilisateur ne peut commencer/finir par des espaces.'
                self._errors['username'] = self.error_class([msg])

            # Check that password != username
            if password == username:
                msg = u'Le mot de passe doit être différent du pseudo.'
                self._errors['password'] = self.error_class([msg])
                if 'password' in cleaned_data:
                    del cleaned_data['password']
                if 'password_confirm' in cleaned_data:
                    del cleaned_data['password_confirm']

        # Check that the email is unique
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).count() > 0:
            msg = u'Votre adresse email est déjà utilisée.'
            self._errors['email'] = self.error_class([msg])

        return cleaned_data


class SettingsPasswordForm(forms.Form):

    password_old = forms.CharField(
        label='Ancien mot de passe',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Ancien mot de passe'
            }
        )
    )
    password_new = forms.CharField(
        label='Nouveau mot de passe',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Nouveau mot de passe'
            }
        )
    )
    password_confirm = forms.CharField(
        label='Confirmation',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmation'
            }
        )
    )

    def __init__(self, user, *args, **kwargs):
        super(SettingsPasswordForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super(SettingsPasswordForm, self).clean()

        password_old = cleaned_data.get('password_old')
        password_new = cleaned_data.get('password_new')
        password_confirm = cleaned_data.get('password_confirm')

        # Check the old password
        user_exist = authenticate(username=self.user.username, password=password_old)
        if not user_exist or password_old == '':
            msg = u'Mot de passe incorrect.'
            self._errors['password_old'] = self.error_class([msg])

            if 'password_old' in cleaned_data:
                del cleaned_data['password_old']

        # Check that the new password and it's confirmation match
        if not password_confirm == password_new:
            msg = u'Les mots de passe sont différents.'
            self._errors['password_confirm'] = self.error_class([msg])

            if 'password_new' in cleaned_data:
                del cleaned_data['password_new']

            if 'password_confirm' in cleaned_data:
                del cleaned_data['password_confirm']

        return cleaned_data


class SettingsOtherForm(forms.Form):

    avatar_url = forms.CharField(
        label='Avatar',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ne pas oublier http:// ou https:// devant.'
            }
        )
    )
    show_email = forms.BooleanField(
        required=False,
        label='Afficher l\'email publiquement',
    )


class LostPasswordForm(forms.Form):

    username = forms.CharField(
        label='Identifiant',
        widget=forms.TextInput(
            attrs={
                'autofocus': '',
                'placeholder': 'Identifiant'
            }
        )
    )

    def clean(self):
        cleaned_data = super(LostPasswordForm, self).clean()

        username = cleaned_data.get('username')

        # Check if the user exist
        if User.objects.filter(username=username).count() == 0:
            msg = u"L'utilisateur %s n'a pas été trouvé." % username
            self._errors['username'] = self.error_class([msg])

        return cleaned_data
