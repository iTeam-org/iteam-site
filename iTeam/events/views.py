from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.utils.safestring import mark_safe

from iTeam.events.models import Event
from iTeam.member.models import Profile

# Create your views here.

def index(request):
    VIEWS = ('L', 'W', 'M')
    view = request.GET.get('view')

    # get objects
    events_list = Event.objects.all()

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

    # profile for groups (create event)
    if request.user.is_authenticated():
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    # data for template
    data = {'data': events_list, 'profile': profile, 'cur_type': view}

    # add active field to proper filter
    if view in VIEWS:
        data[''.join(("view_", view))] = "active"
    else: # default
        data['view_L'] = "active"

    # data for weekly and monthly views
    if view == 'W':
        data['data'] = index_week(request, events_list)
    elif view == 'M':
        data['data'] = index_month(request, events_list)

    return render(request, 'events/index.html', data)

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


def index_month(request, events_list):
    return mark_safe('coucou month')




def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    return render(request, 'events/detail.html', {'event': event})


def create(request):
    return render(request, 'events/create.html')



"""

####
####

from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe

##

from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

class EventCalendar(HTMLCalendar):

    def __init__(self, workouts):
        super(EventCalendar, self).__init__()
        self.workouts = self.group_by_day(workouts)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.workouts:
                cssclass += ' filled'
                body = ['<ul>']
                for workout in self.workouts[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % '#') # '#' -> event url
                    body.append('+1 event') # body.append(esc(workout.title))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, workouts):
        field = lambda workout: workout.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

def index(request):
    year = 2014
    month = 7

    my_events = Event.objects.all()
    cal = EventCalendar(my_events).formatmonth(year, month)
    return render_to_response('events/index.html', {'calendar': mark_safe(cal),})


    #events_list = Event.objects.all()
    #return render(request, 'events/index.html', {'events_list': events_list,})

