
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe
from django.utils import timezone

from datetime import datetime

from iTeam.events.models import Event
from iTeam.member.models import Profile


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

    # profile for groups (can create event ?)
    if request.user.is_authenticated():
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    # data for template
    data = {
        'view': 'list',
        'events_list': events_list,
        'profile': profile,
    }

    return render(request, 'events/index.html', data)


def index_week(request, year, month, week_of_month):
    days_str = [
        'Lundi', 'Mardi', 'Mecredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'
    ]

    year = int(year)
    if (year < 1970):
        year = timezone.now().year

    month = int(month)
    if (month < 1) or (month > 12):
        month = timezone.now().month

    week_of_month = int(week_of_month)
    if (week_of_month < 1) or (week_of_month > 5):
        week_of_month = 3

    events_list = Event.objects.all().filter(is_draft=False, date_start__year=year, date_start__month=month).order_by('-date_start')
    cal, days_nb = ViewWeek(events_list).formatweek(year, month, week_of_month)

    for i in range(0, 7):
        days_str[i] = '%s %s' % (days_str[i], days_nb[i])

    # profile for groups (can create event ?)
    if request.user.is_authenticated():
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    # links : prev and next
    week_prev = week_of_month-1
    week_next = week_of_month+1
    month_prev = month
    month_next = month
    year_prev = year
    year_next = year

    if week_prev < 1:
        month_prev -= 1
        week_prev += 5

    if week_next > 5:
        month_next += 1
        week_next -= 5

    if month_prev < 1:
        year_prev -= 1
        month_prev += 12

    if month_next > 12:
        year_next += 1
        month_next -= 12

    # data for template
    data = {
        'view': 'week',
        'cal': cal,
        'profile': profile,
        'days_str': days_str,

        'week_prev': week_prev,
        'week_next': week_next,
        'month_prev': month_prev,
        'month_next': month_next,
        'year_prev': year_prev,
        'year_next': year_next,
        'week_of_month': week_of_month,
    }

    return render(request, 'events/index.html', data)


def index_month(request, year, month):
    # month_str : january = 1, february = 2, ...
    month_str = [
        '',
        'Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre'
    ]
    days_str = [
        'Lundi', 'Mardi', 'Mecredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'
    ]

    year = int(year)
    if (year < 1970):
        year = timezone.now().year

    month = int(month)
    if (month < 1) or (month > 12):
        month = timezone.now().month

    # get events objects
    events_list = Event.objects.all().filter(is_draft=False, date_start__year=year, date_start__month=month).order_by('-date_start')
    cal_data = ViewMonth(events_list).formatmonth(year, month)

    # profile for groups (can create event ?)
    if request.user.is_authenticated():
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

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
        'profile': profile,
        'days_str': days_str,
        'month_prev_str': month_str[month_prev],
        'month_cur_str': month_str[month],
        'month_next_str': month_str[month_next],
        'month_prev_int': month_prev,
        'month_next_int': month_next,
        'year_prev': year_prev,
        'year_cur': year,
        'year_next': year_next,
    }

    return render(request, 'events/index.html', data)


def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.user.is_authenticated():
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    # default view, published event
    if not event.is_draft:
        return render(request, 'events/detail.html', {'event': event, 'profile': profile})
    elif request.user.is_authenticated():
        profile = get_object_or_404(Profile, user=request.user)

        # if admin or author
        if (request.user == event.author) or (profile.is_admin):
            if (request.method == 'POST') and ('toggle_draft' in request.POST):
                event.is_draft = not event.is_draft
                event.save()
            return render(request, 'events/detail.html', {'event': event, 'profile': profile})
        # not admin nor author
        else:
            raise PermissionDenied
    else: # draft + not logged
        return redirect(reverse('member:login_view'))


@login_required
def create(request):
    profile = get_object_or_404(Profile, user=request.user)

    if (not profile.is_publisher):
        raise PermissionDenied

    event = Event()
    event.date_start = timezone.now()
    return save_event(request, 'events/create.html', event)


@login_required
def edit(request, event_id):
    profile = get_object_or_404(Profile, user=request.user)
    event = get_object_or_404(Event, pk=event_id)

    if ((not profile.is_publisher) or event.author != request.user) and not profile.is_admin:
        raise PermissionDenied

    if (event.author != request.user) and profile.is_admin:
        editing_as_admin = True
    else:
        editing_as_admin = False

    return save_event(request, 'events/edit.html', event, editing_as_admin=editing_as_admin)


def save_event(request, template_name, event, editing_as_admin=False):
    # If the form has been submitted ...
    if request.method == 'POST':
        if request.POST['title'] and request.POST['text'] and request.POST['type'] and request.POST['is_draft']:
            # required and auto fields
            if (not editing_as_admin):
                event.author = request.user

            event.title = request.POST['title'][:settings.SIZE_MAX_TITLE]
            event.place = request.POST['place']
            event.type = request.POST['type']
            event.is_draft = int(request.POST['is_draft']);
            event.text = request.POST['text']

            format = '%d/%m/%Y %H:%M'
            time = request.POST['date_start']
            try:
                event.date_start = datetime.strptime(time, format)
            except ValueError:
                return render(request, template_name, {'msg' : 'Erreur : Date mal formatee', 'event': event})

            # save here to get the pk and name the (optional) img with it
            event.save()

            if 'image' in request.FILES:
                img = request.FILES['image']
                ext = string.lower(img.name.split('.')[-1])

                if img.size > settings.SIZE_MAX_IMG:
                    return render(request, template_name, {'msg' : 'Erreur : Fichier trop lourd', 'event': event})
                if ext not in ('png', 'jpg', 'jpeg', 'gif', 'tiff', 'bmp'):
                    return render(request, template_name, {'msg' : 'Erreur : Extension non reconnue, le fichier n\'est pas une image', 'event': event})

                # remove old img (if one)
                if event.image.name:
                    img_path = os.path.join(settings.MEDIA_ROOT, str(event.image.name))
                    if os.path.exists(img_path):
                        os.remove(img_path)

                # add publication img
                event.image = img
                event.image.name = '.'.join((str(event.pk), ext))
                event.save()

            # Redirect after successfull POST
            return HttpResponseRedirect(reverse('events:detail', args=(event.id,)))
        # missing data
        else:
            return render(request, template_name, {'msg': 'Erreur : un champ obligatoire n\'a pas ete rempli', 'event': event})
    # if no post data sent ...
    else:
        return render(request, template_name, {'event': event, 'editing_as_admin': editing_as_admin,})




"""
    Overload of default class for displaying an html calendar, due to custom
    attributes (models) and actions (template)

    note :
    arg 'workouts' passed to __init__() func must be sorted by the same attr as
    the lambda func used in group_by_day() (currently : date_start attr of events)
"""


from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

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
                            tmp_events.append({'title': workout.title, 'pk': workout.pk})
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

        data = self.monthdays2calendar(theyear, themonth)

        ret = []
        days_nb = []
        current_week = 1
        current_hour = 8

        for week in data:
            if current_week == weekofmonth:
                for hour in range(8, 18+1):
                    tmp_hour_row = []

                    tmp_hour_row.append({'event': False, 'data': None, 'hour': current_hour})
                    current_hour += 1

                    for day, dayweek in week:
                        tmp_hour_cell = {'event': False, 'data': None, 'hour': None}

                        # if in current month
                        if day != 0:
                            # if events this day, this hour, add them
                            key = self.key(day, hour)
                            if key in self.workouts:
                                tmp_events = []
                                for workout in self.workouts[key]:
                                    tmp_events.append({'title': workout.title, 'pk': workout.pk})
                                tmp_hour_cell['data'] = tmp_events
                            # default : day in current month, no events
                            else:
                                pass

                            ## set today field if needed
                            #if date.today() == date(theyear, themonth, day):
                            #    tmp_day['today'] = True
                            #    tmp_day['day'] = ' - '.join((str(tmp_day['day']), 'Aujourd\'hui'))
                        # mark this day no in current month
                        else:
                            pass

                        tmp_hour_row.append(tmp_hour_cell)

                        days_nb.append(day)
                    ret.append(tmp_hour_row)

            current_week += 1

        return ret, days_nb

