from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils import timezone

from iTeam.events.models import Event
from iTeam.member.models import Profile

# Create your views here.

def index(request):
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
    events_list = Event.objects.all().order_by('-date_start')

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

    return render(request, 'events/index.html', data)


def index_list(request, events_list):
    # paginator (for listed view)
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

    return events_list


def index_week(request, events_list):
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


def index_month(request, events_list, year, month):
    events_list = events_list.filter(date_start__year=year, date_start__month=month)
    cal = EventCalendar(events_list).formatmonth(year, month)

    return mark_safe(cal)




def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    return render(request, 'events/detail.html', {'event': event})


def create(request):
    return render(request, 'events/create.html')


"""
    Overload of default class for displaying an html calendar, due to custom
    attributes (models) and actions (template)
"""


from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

class EventCalendar(HTMLCalendar):

    def __init__(self, workouts):
        super(EventCalendar, self).__init__()
        self.workouts = self.group_by_day(workouts)

    def formatday(self, day, weekday):
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

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

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

