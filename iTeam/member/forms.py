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

from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):

    """Form used for login in users."""

    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=76, widget=forms.PasswordInput)


class RegisterForm(forms.Form):

    """Form used for to register new users."""

    email = forms.EmailField()
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=76, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=76, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        self._errors = []

        # Check that the user doesn't exist yet
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).count() > 0:
            self._errors.append(u'Ce nom d\'utilisateur est déjà utilisé')

        # Check that the password and it's confirmation match
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if not password_confirm == password:
            self._errors.append(u'Les mots de passe sont différents')

        return cleaned_data


class SettingsForm(forms.Form):

    """Form used to change an user's personnal informations and options."""

    password_old = forms.CharField(max_length=76, widget=forms.PasswordInput)
    password_new = forms.CharField(max_length=76, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=76, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SettingsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SettingsForm, self).clean()
        self._errors = []

        password_old = cleaned_data.get('password_old')
        password_new = cleaned_data.get('password_new')
        password_confirm = cleaned_data.get('password_confirm')

        # Check the old password
        user_exist = authenticate(username=self.user.username, password=password_old)
        if not user_exist or password_old == "":
            self._errors.append(u'Mot de passe incorrect.')

        # Check that the new password and it's confirmation match
        if not password_confirm == password_new:
            self._errors .append(u'Les mots de passe sont différents.')

        return cleaned_data
