#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-20 14:35:58
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-11-05 10:33:59

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


from hashlib import md5

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string


class Profile(models.Model):
    user = models.OneToOneField(User)
    show_email = models.BooleanField(default=False)
    avatar_url = models.CharField(max_length=256, blank=True, default='')

    is_publisher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def get_avatar_url(self):
        if self.avatar_url:
            return self.avatar_url
        else:
            username_hash = md5(self.user.username).hexdigest()
            size = 100
            return 'https://secure.gravatar.com/avatar/{0}?d=identicon&s={1}'.format(username_hash, size)


class ForgotPasswordToken(models.Model):
    class Meta:
        verbose_name = 'Token réinitialisation mot de passe'
        verbose_name_plural = 'Tokens réinitialisation mot de passe'

    user = models.ForeignKey(User, verbose_name='Utilisateur')
    token = models.CharField(max_length=100)
    expires = models.DateTimeField('Expiration')

    def __str__(self):
        return '<ForgotPasswordToken User={}>'.format(self.user)

    def get_absolute_url(self):
        return reverse('member:password_reset_confirm', args=[self.token])


def send_templated_mail(subject, template, context, recipients):
    """Send an email based on a template.

    Args:
        subject: (string) Subject of the email
        template: (string) Name of the template used for the message
        context: (dictionary) Dictionary used for the message
        recipients: (list) List of the recipients

    Returns:
        Number of successfully delivered messages (0 or 1)

    """

    message = render_to_string(template, context)

    return send_mail(
        recipient_list=recipients,
        subject=subject,
        message=message,
        from_email=None,  # use default one from settings_prod.py
    )
