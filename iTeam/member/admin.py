#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-07-13 18:51:48
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-11-02 17:54:01

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


from django.contrib import admin

from iTeam.member.models import Profile, ForgotPasswordToken


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']

admin.site.register(Profile, ProfileAdmin)


class ForgotPasswordTokenAdmin(admin.ModelAdmin):
    search_fields = ['user__username']

admin.site.register(ForgotPasswordToken, ForgotPasswordTokenAdmin)
