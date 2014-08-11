from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
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
    """
    VIEWS = ('L', 'W', 'M')
    month_str = [
        'Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre'
    ]

    # get param
    view = request.GET.get('view')
    if view not in VIEWS:
        view = 'L' # default

    if 'm' in request.GET:
        try:
            month = int(request.GET['m'])
        except ValueError:
            month = timezone.now().month
    if ('m' not in request.GET) or (month <= 0) or (month > 12):
        month = timezone.now().month

    if 'y' in request.GET:
        try:
            year = int(request.GET['y'])
        except ValueError:
            year = timezone.now().year
    if ('y' not in request.GET) or (year < 1950) or (year > 2500):
        year = timezone.now().year

    # get events objects
    events_list = Event.objects.all().filter(is_draft=False).order_by('-date_start')

    # profile for groups (can create event ?)
    if request.user.is_authenticated():
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    # data for template
    data = {'profile': profile}

    # events display, function of the view choosen by the user
    if view == 'W':
        data['data'] = index_week(request, events_list)
    elif view == 'M':
        data['data'] = index_month(request, events_list, year, month)
    else: # default : L
        data['data'] = index_list(request, events_list)

    # add active field to proper filter (for view : list, week, month)
    if view in VIEWS:
        data[''.join(("view_", view))] = "active"
    else: # default
        data['view_L'] = "active"

    # data for month view
    data['month_prev'] = month-1
    data['month_next'] = month+1
    data['year_prev'] = year
    data['year_next'] = year

    if data['month_prev'] <= 0:
        data['year_prev'] -= 1
        data['month_prev'] += 12

    if data['month_next'] > 12:
        data['year_next'] += 1
        data['month_next'] -= 12

    data['month_cur'] = month_str[month-1]
    data['year_cur'] = year
    """

    return render(request, 'events/index.html')


def index_month(request, year, month):
    month_str = ['', # january = 1, february = 2, ...
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
    events_list = Event.objects.all().filter(is_draft=False, date_start__year=year, date_start__month=month)
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


import datetime

def index_week(request, events_list, year, week):
    date_from = timezone.now() - datetime.timedelta(days=7)
    date_to = timezone.now()

    events_list = events_list.filter(date_start__gte=date_from).filter(date_start__lte=date_to)
    cal = ViewWeek(events_list).formatweek(year, week)

    return mark_safe(cal)

    DAYS = ('', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi')

    ret = ''

    ret += '<div class="class="custom_table_for_events">'
    ret += '<table class="class="custom_table_for_events">'

    # head
    ret += '<thead>'
    ret += '<tr>'
    for day in DAYS:
        ret += '<th>%s</th>' % day
    ret += '</tr>'
    ret += '</thead>'

    # body
    ret += '<tbody>'
    for hour in range(8, 20):
        ret += '<tr>'
        for day in DAYS:
            if day == '':
                ret += '<th>%dh</th>' % hour
            else:
                ret += '<td>Coucou</td>'
        ret += '</tr>'
    ret += '</tbody>'

    ret += '</table>'
    ret += '</div>'

    return mark_safe(ret)



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
        # else : 404
        else:
            raise Http404
    else:
        raise Http404




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

    if (not profile.is_publisher):
        raise PermissionDenied

    event = get_object_or_404(Event, pk=event_id)

    if (event.author != request.user) and profile.is_admin:
        editing_as_admin = True
    else:
        editing_as_admin = False

    if (event.author == request.user) or profile.is_admin:
        return save_event(request, 'events/edit.html', event, editing_as_admin=editing_as_admin)
    else:
        raise Http404


def save_event(request, template_name, event, editing_as_admin=False):
    # If the form has been submitted ...
    if request.method == 'POST':
        if request.POST['title'] and request.POST['text'] and request.POST['type'] and request.POST['is_draft']:
            # required and auto fields
            if (not editing_as_admin):
                event.author = request.user

            event.title = request.POST['title'][:settings.SIZE_MAX_TITLE]
            event.place = request.POST['place']
            format = '%d/%m/%Y %H:%M'
            time = request.POST['date_start']
            try:
                event.date_start = datetime.strptime(time, format)
            except ValueError:
                event.date_start = timezone.now()
            event.type = request.POST['type']
            event.is_draft = int(request.POST['is_draft']);
            event.text = request.POST['text']

            # save here to get the pk and name the (optional) img with it
            event.save()

            if 'image' in request.FILES:
                img = request.FILES['image']
                ext = string.lower(img.name.split('.')[-1])

                if img.size > settings.SIZE_MAX_IMG:
                    return render(request, template_name, {'msg' : 'Erreur : Fichier trop lourd', 'event': event})
                if ext not in ('png', 'jpg', 'jpeg', 'gif', 'tiff', 'bmp'):
                    return render(request, template_name, {'msg' : 'Erreur : Extension non reconnue, le fichier n\'est pas une image', 'publication': publication})

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
            return render(request, template_name, {'msg': 'Erreur : un champ obligatoire n\'a pas \xc3t\xc3 rempli', 'event': event})
    # if no post data sent ...
    else:
        return render(request, template_name, {'event': event, 'editing_as_admin': editing_as_admin,})




"""
    Overload of default class for displaying an html calendar, due to custom
    attributes (models) and actions (template)
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
        data =  self.monthdays2calendar(theyear, themonth)

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
        if day != 0:
            head = '<div style="text-align: right;">%d</div>' % day

            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.workouts:
                cssclass += ' filled'
                body = []
                body.append('<div class="left"><ul>')
                for workout in self.workouts[day]:
                    body.append('<a href="view/%d">' % workout.pk) # '#' -> event url
                    body.append('<li>%s</li>' % workout.title) # body.append(esc(workout.title))
                    body.append('</a>')
                body.append('</ul></div>')
                return self.day_cell(cssclass, '%s %s' % (head, ''.join(body)))
            return self.day_cell(cssclass, head)
        else:
            return self.day_cell('noday', '&nbsp;')

    def group_by_day(self, workouts):
        field = lambda workout: workout.date_start.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        day_abbr = ['Lundi', 'Mardi', 'Mecredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

        return '<th class="%s">%s</th>' % (self.cssclasses[day], day_abbr[day])

    def formatmonth(self, theyear, themonth, withyear=True):
        self.year, self.month = theyear, themonth
        v = []
        a = v.append
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        return ''.join(v)

