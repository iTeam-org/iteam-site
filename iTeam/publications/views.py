#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-21 18:22:36
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-08-22 17:08:11

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


import os

from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from iTeam.publications.models import Publication
from iTeam.publications.forms import PublicationForm
from iTeam.member.models import Profile


def index(request):
    TYPES = ('N', 'T', 'P')

    if request.user.is_authenticated():
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    # get objects
    publications_list = Publication.objects.all().filter(pub_date__lte=timezone.now(), is_draft=False). \
        order_by('-pub_date')

    type = request.GET.get('type')
    if type in TYPES:
        publications_list = publications_list.filter(type=type)

    # paginator
    paginator = Paginator(publications_list, settings.NB_PUBLICATIONS_PER_PAGE)

    page = request.GET.get('page')
    try:
        publications = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        publications = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        publications = paginator.page(paginator.num_pages)

    # build data for template
    data = {"data": publications, "cur_type": type, "profile": profile}

    # add active field to proper filter
    if type in TYPES:
        data[''.join(("type_", type))] = "active"
    else:
        data['type_all'] = "active"

    return render(request, 'publications/index.html', data)


def detail(request, publication_id):
    publication = get_object_or_404(Publication, pk=publication_id)

    if request.user.is_authenticated():
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    # default view, published article
    if not publication.is_draft:
        data = {'publication': publication, 'profile': profile}
        return render(request, 'publications/detail.html', data)
    elif request.user.is_authenticated():
        profile = get_object_or_404(Profile, user=request.user)

        # if admin or author
        if (request.user == publication.author) or (profile.is_admin):
            if (request.method == 'POST') and ('toggle_draft' in request.POST):
                publication.is_draft = not publication.is_draft
                publication.pub_date = timezone.now()
                publication.save()

            data = {'publication': publication, 'profile': profile}
            return render(request, 'publications/detail.html', data)
        else:  # not admin nor author
            raise PermissionDenied
    else:  # draft + not logged
        return redirect(reverse('member:login_view'))


@login_required
def create(request):
    profile = get_object_or_404(Profile, user=request.user)

    if (not profile.is_publisher) and (not profile.is_admin):
        raise PermissionDenied

    publication = Publication()
    return save_publication(request, 'publications/create.html', publication)


@login_required
def edit(request, publication_id):
    profile = get_object_or_404(Profile, user=request.user)
    publication = get_object_or_404(Publication, pk=publication_id)

    if ((not profile.is_publisher) or publication.author != request.user) and not profile.is_admin:
        raise PermissionDenied

    if (publication.author != request.user) and profile.is_admin:
        editing_as_admin = True
    else:
        editing_as_admin = False

    return save_publication(request, 'publications/edit.html', publication, editing_as_admin=editing_as_admin)


def save_publication(request, template_name, publication, editing_as_admin=False):
    # If the form has been submitted ...
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            # required and auto fields
            if (not editing_as_admin):
                publication.author = request.user
                publication.pub_date = timezone.now()

            publication.title = form.cleaned_data['title'][:settings.SIZE_MAX_TITLE]
            publication.text = form.cleaned_data['text']
            publication.type = form.cleaned_data['type']
            publication.is_draft = int(form.cleaned_data['is_draft'])

            # optional fields
            if 'subtitle' in request.POST:
                publication.subtitle = form.cleaned_data['subtitle'][:settings.SIZE_MAX_TITLE]

            if 'image' in request.FILES:
                img = request.FILES['image']

                # remove old img (if one)
                if publication.image.name:
                    img_path = os.path.join(settings.MEDIA_ROOT, str(publication.image.name))
                    if os.path.exists(img_path):
                        os.remove(img_path)

                # save here to get the pk of the publication and name the img with it
                publication.save()
                publication.image = img

            # save publication + Redirect after successfull POST
            publication.save()
            return HttpResponseRedirect(reverse('publications:detail', args=(publication.id,)))

    else:  # method == GET
        form = PublicationForm()

        if publication is not None:
            form.fields['title'].initial = publication.title
            form.fields['subtitle'].initial = publication.subtitle
            form.fields['type'].initial = publication.type
            form.fields['text'].initial = publication.text
            if publication.is_draft:
                form.fields['is_draft'].initial = '1'
            else:
                form.fields['is_draft'].initial = '0'

    # if no post data sent ...
    data = {'form': form, 'editing_as_admin': editing_as_admin, 'publication_pk': publication.pk}
    return render(request, template_name, data)
