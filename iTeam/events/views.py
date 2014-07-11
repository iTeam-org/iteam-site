from django.shortcuts import render

from iTeam.events.models import Event

# Create your views here.

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

