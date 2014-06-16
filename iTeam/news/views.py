from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.conf import settings

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


def create(request):
    # If the form has been submitted ...
    if request.method == 'POST':
        # parse data
        title = request.POST['title'][:49]
        author = request.POST['author'][:49]
        text = request.POST['text']
        
        # if all data is ok
        if title and author and text:
            # Process the data
            news = News(title=title, author=author, pub_date=timezone.now(), text=text)
            news.save()
            
            # Redirect after POST
            return HttpResponseRedirect(reverse('news:detail', args=(news.id,)))
        # missing data
        else:
            return render(request, 'news/create.html', {'msg' : 'Missing data'})
    # if no post data sent ...
    else:
        return render(request, 'news/create.html')



