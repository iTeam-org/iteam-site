from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.decorators import login_required

from iTeam.news.models import News

# Create your views here.

def index(request):
    news_list = News.objects.all().order_by('-pub_date')
    paginator = Paginator(news_list, settings.NB_NEWS_PER_PAGE)

    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)

    return render(request, 'news/index.html', {"data": news})


def detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)

    return render(request, 'news/detail.html', {'news': news,})


@login_required(redirect_field_name='suivant')
def create(request):
    # If the form has been submitted ...
    if request.method == 'POST':
        if 'title' in request.POST and 'text' in request.POST:
            # parse data
            title = request.POST['title'][:49]
            if 'subtitle' in request.POST:
                subtitle = request.POST['subtitle'][:49]
            else:
                subtitle = None
            text = request.POST['text']
        
            # Process the data
            news = News(
                title=title, subtitle = subtitle, text=text,
                author=request.user, pub_date=timezone.now()
            )
            news.save()
            
            # Redirect after POST
            return HttpResponseRedirect(reverse('news:detail', args=(news.id,)))
        # missing data
        else:
            return render(request, 'news/create.html', {'msg' : 'Missing data'})
    # if no post data sent ...
    else:
        return render(request, 'news/create.html')



