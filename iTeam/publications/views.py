#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-21 18:22:36
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-11-04 19:32:21

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
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.utils import timezone

from iTeam.member.models import Profile
from iTeam.publications.models import Publication
from iTeam.publications.forms import PublicationForm


def index(request):
    # get objects
    publications_list = Publication.objects.all().filter(pub_date__lte=timezone.now(), is_draft=False). \
        order_by('-pub_date')

    type = request.GET.get('type')
    if type in settings.PUBLICATIONS_TYPES:
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
    data = {
        "data": publications,
        "cur_type": type,
        "types": settings.PUBLICATIONS_MODEL_TYPES,
    }

    # add active field
    if not (type in settings.PUBLICATIONS_TYPES):
        data['type_all'] = "active"

    return render(request, 'publications/index.html', data)


def detail(request, publication_id, publication_slug):
    publication = get_object_or_404(Publication, pk=publication_id)

    # Redirect if bad tutorial slug but item exists (Make sure the URL is well-formed)
    if publication_slug != slugify(publication.title):
        return redirect(publication.get_absolute_url(), permanent=True)

    # default view, published article
    if not publication.is_draft:
        data = {'publication': publication}
        return render(request, 'publications/detail.html', data)
    # draft
    else:
        # not loged -> redirect login
        if not request.user.is_authenticated():
            return redirect(reverse('member:login_view'))
        # if admin or author -> view
        elif (request.user == publication.author) or request.user.profile.is_admin:
            if (request.method == 'POST') and ('toggle_draft' in request.POST):
                publication.is_draft = not publication.is_draft
                publication.pub_date = timezone.now()
                publication.save()

            data = {'publication': publication}
            return render(request, 'publications/detail.html', data)
        # logged user -> 403
        else:
            raise PermissionDenied


def by_author(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    profileRequest = None
    if request.user.is_authenticated():
        profileRequest = get_object_or_404(Profile, user=request.user)

    publications_all = Publication.objects.all().filter(author=user).order_by('-pub_date')
    if publications_all.count() == 0:
        raise Http404
    publications_list = publications_all.filter(is_draft=False)
    publications_drafts = publications_all.filter(is_draft=True)

    c = {
        'profile_detail': profile,
        'profile_request': profileRequest,
        'publications_list': publications_list,
        'publications_draft_list': publications_drafts,
    }

    return render(request, 'publications/by_author.html', c)


@login_required
def create(request):
    profile = request.user.profile  # login_required
    if (not profile.is_publisher) and (not profile.is_admin):
        raise PermissionDenied

    # preview ?
    if (request.method == 'POST') and ('preview' in request.POST):
        c = {
            'form': PublicationForm(request.POST, request.FILES),
        }

        return render(request, 'publications/create.html', c)

    publication = Publication()
    return save_publication(request, 'publications/create.html', publication)


@login_required
def edit(request, publication_id):
    profile = request.user.profile  # login_required
    publication = get_object_or_404(Publication, pk=publication_id)

    if ((not profile.is_publisher) or publication.author != request.user) and not profile.is_admin:
        raise PermissionDenied

    editing_as_admin = (publication.author != request.user) and profile.is_admin

    # preview ?
    if (request.method == 'POST') and ('preview' in request.POST):
        form = PublicationForm(request.POST, request.FILES)

        c = {
            'form': form,
            'editing_as_admin': editing_as_admin,
            'publication_pk': publication.pk,
        }

        return render(request, 'publications/edit.html', c)

    return save_publication(request, 'publications/edit.html', publication, editing_as_admin=editing_as_admin)


def save_publication(request, template_name, publication, editing_as_admin=False):
    # If the form has been submitted ...
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            # required and auto fields
            if not editing_as_admin:
                publication.author = request.user
                publication.pub_date = timezone.now()

            publication.title = form.cleaned_data['title'][:settings.SIZE_MAX_TITLE]
            publication.text = form.cleaned_data['text']
            publication.type = form.cleaned_data['type']
            publication.is_draft = int(form.cleaned_data['is_draft'])

            # optional fields
            publication.subtitle = form.cleaned_data['subtitle'][:settings.SIZE_MAX_TITLE]

            if 'image' in request.FILES:
                img = request.FILES['image']

                # remove old img (if one)
                if publication.image.name:
                    img_path = os.path.join(settings.MEDIA_ROOT, str(publication.image.name))
                    if os.path.exists(img_path):
                        os.remove(img_path)

                # add event img
                publication.save()  # auto set the pk before saving img
                publication.image = img

            # save publication + Redirect after successfull POST
            publication.save()
            return redirect(publication.get_absolute_url())

    else:  # method == GET
        form = PublicationForm()

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
