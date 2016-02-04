#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-10-28 11:31:30
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-10-28 11:36:55

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


def piwik_url(request):
    """
        Return the root url of piwik.
    """
    return {'piwik_url': 'analytics.iteam.org'}


def git_version(request):
    """
        Return the current deployed git version.

        If not running on a production machine (if the 'git_version.txt' file is
        not found), this will just display that the running version is local.
    """

    try:
        with open('git_version.txt') as f:
            v = f.read().strip()
    except IOError:
        v = 'local_version'

    return {'git_version': v}
