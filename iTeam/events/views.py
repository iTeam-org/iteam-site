#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-21 18:57:25
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-11-10 23:14:12

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


from datetime import date, timedelta
import os
import time

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
from iTeam.events.models import Event
from iTeam.events.forms import EventForm


def index_list(request):
    # get events objects
    events_list = Event.objects.all().filter(is_draft=False).order_by('-date_start')

    # paginator
    paginator = Paginator(events_list, settings.NB_EVENTS_PER_PAGE)

    page = request.GET.get('page')
    try:
        events_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events_list = paginator.page(paginator.num_pages)

    # data for template
    data = {
        'view': 'list',
        'events_list': events_list,
    }

    return render(request, 'events/index.html', data)


def index_week(request, days_since_epoch):
    if int(days_since_epoch) == 0:
        days_since_epoch = time.time()/24/3600

    wanted_date = date.fromtimestamp(float(days_since_epoch)*24*3600)

    # it works, dont ask how or why.
    date_month_start = date(year=wanted_date.year, month=wanted_date.month, day=1)
    delta = wanted_date - (date_month_start - timedelta(days=1))
    delta_days_in_month = int(delta.total_seconds()/3600/24) + date_month_start.weekday()

    year = wanted_date.year
    month = wanted_date.month
    week_of_month = int((delta_days_in_month-1)/7)

    # get cal
    events_list = Event.objects.all().order_by('-date_start'). \
        filter(is_draft=False, date_start__year=year, date_start__month=month)
    cal, days_nb = ViewWeek(events_list).formatweek(year, month, week_of_month)

    # header of table : days of week
    days_str_ret = []
    for i in range(0, 7):
        days_str_ret.append({'str': settings.DAYS_STR[i], 'nb': days_nb[i]})

    # links : prev and next
    def ft_same_week(date1, date2):
        return (date1.isocalendar()[0] == date2.isocalendar()[0]) and (date1.isocalendar()[1] == date2.isocalendar()[1])

    days_since_epoch_prev = wanted_date
    nb_days_prev = wanted_date.weekday()
    while ft_same_week(wanted_date, days_since_epoch_prev) and (days_str_ret[nb_days_prev]['nb'] != 0):
        days_since_epoch_prev -= timedelta(days=1)
        nb_days_prev -= 1

    days_since_epoch_next = wanted_date
    nb_days_next = wanted_date.weekday()
    while ft_same_week(wanted_date, days_since_epoch_next) and (days_str_ret[nb_days_next]['nb'] != 0):
        days_since_epoch_next += timedelta(days=1)
        nb_days_next += 1

    # data for template
    data = {
        'view': 'week',
        'cal': cal,
        'days_str': days_str_ret,

        'month_cur_str': settings.MONTH_STR[month],
        'year_cur': year,
        'week_of_month': week_of_month+1,
        'days_since_epoch_prev': int(days_since_epoch)+nb_days_prev-wanted_date.weekday(),  # TODO : check > 0, else 500 error in template when building url : event/week/-1
        'days_since_epoch_next': int(days_since_epoch)+nb_days_next-wanted_date.weekday(),
    }

    return render(request, 'events/index.html', data)


def index_month(request, year, month):
    year = int(year)
    if year < 1970:
        year = timezone.now().year

    month = int(month)
    if (month < 1) or (month > 12):
        month = timezone.now().month

    # get events objects
    events_list = Event.objects.all().filter(is_draft=False, date_start__year=year, date_start__month=month). \
        order_by('-date_start')
    cal_data = ViewMonth(events_list).formatmonth(year, month)

    # links : prev and next
    month_prev = month-1
    month_next = month+1
    year_prev = year
    year_next = year

    if month_prev <= 0:
        year_prev -= 1
        month_prev += 12

    if month_next > 12:
        year_next += 1
        month_next -= 12

    # data for template
    data = {
        'view': 'month',
        'cal': cal_data,
        'days_str': settings.DAYS_STR,
        'month_prev_str': settings.MONTH_STR[month_prev],
        'month_cur_str': settings.MONTH_STR[month],
        'month_next_str': settings.MONTH_STR[month_next],
        'month_prev_int': month_prev,
        'month_next_int': month_next,
        'year_prev': year_prev,
        'year_cur': year,
        'year_next': year_next,
    }

    return render(request, 'events/index.html', data)


def detail(request, event_id, event_slug):
    event = get_object_or_404(Event, pk=event_id)
    file_basename = os.path.basename(event.file.name)

    # Redirect if bad tutorial slug but item exists (Make sure the URL is well-formed)
    if event_slug != slugify(event.title):
        return redirect(event.get_absolute_url(), permanent=True)

    # default view, published events
    if not event.is_draft:
        return render(request, 'events/detail.html', {'event': event, 'file_basename': file_basename})
    # draft
    else:
        # not loged -> redirect login
        if not request.user.is_authenticated():
            return redirect(reverse('member:login_view'))
        # if admin or author -> view
        elif (request.user == event.author) or request.user.profile.is_admin:
            if (request.method == 'POST') and ('toggle_draft' in request.POST):
                event.is_draft = not event.is_draft
                event.save()

            return render(request, 'events/detail.html', {'event': event, 'file_basename': file_basename})
        # logged user -> 403
        else:
            raise PermissionDenied


def by_author(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    profileRequest = None
    if request.user.is_authenticated():
        profileRequest = get_object_or_404(Profile, user=request.user)

    events_all = Event.objects.all().filter(author=user).order_by('-date_start')
    if events_all.count() == 0:
        raise Http404
    events_list = events_all.filter(is_draft=False)
    events_drafts = events_all.filter(is_draft=True)

    c = {
        'profile_detail': profile,
        'profile_request': profileRequest,
        'events_list': events_list,
        'events_draft_list': events_drafts,
    }

    return render(request, 'events/by_author.html', c)


@login_required
def create(request):
    profile = request.user.profile  # login_required

    if (not profile.is_publisher) and (not profile.is_admin):
        raise PermissionDenied

    # preview ?
    if (request.method == 'POST') and ('preview' in request.POST):
        c = {
            'form': EventForm(request.POST, request.FILES),
        }

        return render(request, 'events/create.html', c)

    event = Event()
    event.date_start = timezone.now()
    return save_event(request, 'events/create.html', event)


@login_required
def edit(request, event_id):
    profile = request.user.profile  # login_required
    event = get_object_or_404(Event, pk=event_id)

    if ((not profile.is_publisher) or event.author != request.user) and not profile.is_admin:
        raise PermissionDenied

    editing_as_admin = (event.author != request.user) and profile.is_admin

    # preview ?
    if (request.method == 'POST') and ('preview' in request.POST):
        form = EventForm(request.POST, request.FILES)

        c = {
            'form': form,
            'editing_as_admin': editing_as_admin,
            'event_pk': event.pk,
        }

        return render(request, 'events/edit.html', c)

    return save_event(request, 'events/edit.html', event, editing_as_admin=editing_as_admin)


def save_event(request, template_name, event, editing_as_admin=False):
    # If the form has been submitted ...
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            # required and auto fields
            if not editing_as_admin:
                event.author = request.user

            event.title = form.cleaned_data['title'][:settings.SIZE_MAX_TITLE]
            event.place = form.cleaned_data['place']
            event.type = form.cleaned_data['type']
            event.is_draft = int(form.cleaned_data['is_draft'])
            event.text = form.cleaned_data['text']
            event.date_start = form.cleaned_data['date_start']

            if 'image' in request.FILES:
                img = request.FILES['image']

                # remove old img (if one)
                if event.image and event.image.name:
                    img_path = os.path.join(settings.MEDIA_ROOT, event.image.name)
                    if os.path.exists(img_path):
                        os.remove(img_path)

                # add image to event - save before to set the pk
                event.save()
                event.image = img

            if 'file' in request.FILES:
                f = request.FILES['file']

                # remove old file (if one)
                if event.file and event.file.name:
                    file_path = os.path.join(settings.MEDIA_ROOT, event.file.name)
                    if os.path.exists(file_path):
                        os.remove(file_path)

                # add file to event - save before to set the pk
                event.save()
                event.file = f

            # save event + Redirect after successfull POST
            event.save()
            return redirect(event.get_absolute_url())

    else:  # method == GET
        form = EventForm()

        if event is not None:
            form.fields['title'].initial = event.title
            form.fields['place'].initial = event.place
            form.fields['date_start'].initial = event.date_start
            form.fields['type'].initial = event.type
            form.fields['text'].initial = event.text
            if event.is_draft:
                form.fields['is_draft'].initial = '1'
            else:
                form.fields['is_draft'].initial = '0'

    # if no post data sent ...
    data = {'form': form, 'editing_as_admin': editing_as_admin, 'event_pk': event.pk}
    return render(request, template_name, data)


"""
    Overload of default class for displaying an html calendar, due to custom
    attributes (models) and actions (template)

    note :
    arg 'workouts' passed to __init__() func must be sorted by the same attr as
    the lambda func used in group_by_day() (currently : date_start attr of events)
"""


from calendar import HTMLCalendar
from itertools import groupby
from datetime import datetime
import pytz


class ViewMonth(HTMLCalendar):

    def __init__(self, workouts):
        super(ViewMonth, self).__init__()
        self.workouts = self.group_by_day(workouts)

    def group_by_day(self, workouts):
        field = lambda workout: workout.date_start.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def formatmonth(self, theyear, themonth, withyear=True):
        data = self.monthdays2calendar(theyear, themonth)

        ret = []

        for week in data:
            tmp_week = []
            for day, dayweek in week:
                # for each day of month

                tmp_day = {'day': day, 'noday': False, 'data': None, 'today': False}

                # if in current month
                if day != 0:
                    # if events this day, add them
                    if day in self.workouts:
                        tmp_events = []
                        for workout in self.workouts[day]:
                            tmp_events.append(get_object_or_404(Event, pk=workout.pk))
                        tmp_day['data'] = tmp_events
                    # default : day in current month, no events
                    else:
                        pass

                    # set today field if needed
                    if date.today() == date(theyear, themonth, day):
                        tmp_day['today'] = True
                        tmp_day['day'] = ' - '.join((str(tmp_day['day']), 'Aujourd\'hui'))
                # mark this day no in current month
                else:
                    tmp_day['noday'] = True

                tmp_week.append(tmp_day)
            ret.append(tmp_week)

        return ret


class ViewWeek(HTMLCalendar):

    def __init__(self, workouts):
        super(ViewWeek, self).__init__()
        self.workouts = self.group_by_day(workouts)

    def group_by_day(self, workouts):
        field = lambda workout: self.key(workout.date_start.day, workout.date_start.hour)
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def key(self, day, hour):
        return day*100 + hour

    def formatweek(self, theyear, themonth, weekofmonth, withyear=True):
        week = self.monthdays2calendar(theyear, themonth)[weekofmonth]
        ret = []
        days_nb = []

        # use object and not int for having django convert utc to local
        utc_now_zero = datetime.utcnow().replace(tzinfo=pytz.utc, hour=0)
        time_stepper = utc_now_zero + timedelta(hours=settings.START_HOUR_UTC)
        time_end = utc_now_zero + timedelta(hours=settings.END_HOUR_UTC)

        while time_stepper < time_end:
            tmp_hour_row = [{'event': False, 'data': None, 'hour': time_stepper}]

            for day, dayweek in week:
                tmp_hour_cell = {'event': False, 'data': None, 'hour': None}

                # if in current month
                if day != 0:
                    # if events this day, this hour, add them
                    key = self.key(day, time_stepper.hour)
                    if key in self.workouts:
                        tmp_events = []
                        for workout in self.workouts[key]:
                            tmp_events.append(get_object_or_404(Event, pk=workout.pk))
                        tmp_hour_cell['data'] = tmp_events

                tmp_hour_row.append(tmp_hour_cell)
                days_nb.append(day)

            ret.append(tmp_hour_row)
            time_stepper += timedelta(hours=1)

        return ret, days_nb
