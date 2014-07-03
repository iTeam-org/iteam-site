from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.decorators import login_required

import string
import os

from iTeam.news.models import News

# Create your views here.

def index(request):
    TYPES = ('N', 'T', 'P')

    # get objects
    news_list = News.objects.all().filter(pub_date__lte=timezone.now()).order_by('-pub_date')

    type = request.GET.get('type')
    if type in TYPES:
        news_list = news_list.filter(type=type)

    # paginator
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

    # build data for template
    data = {"data":news, "cur_type":type}

    # add active field to proper filter
    if type in TYPES:
        data[''.join(("type_", type))] = "active"
    else:
        data['type_all'] = "active"

    return render(request, 'news/index.html', data)


def detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)

    if news.pub_date > timezone.now() and not request.user.is_authenticated():
        raise Http404

    return render(request, 'news/detail.html', {'news': news,})


@login_required(redirect_field_name='suivant')
def create(request):
    news = News()
    return save_news(request, 'news/create.html', news)

@login_required(redirect_field_name='suivant')
def edit(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if news.author.pk is not request.user.pk:
        raise Http404
    else:
        return save_news(request, 'news/edit.html', news)


def save_news(request, template_name, news):
    # If the form has been submitted ...
    if request.method == 'POST':
        if request.POST['title'] and request.POST['text'] and request.POST['type']:
            # required and auto fields
            news.author = request.user
            news.pub_date = timezone.now()

            news.title = request.POST['title'][:99]
            news.text = request.POST['text']
            news.type = request.POST['type']

            # optional fields
            if 'subtitle' in request.POST:
                news.subtitle = request.POST['subtitle'][:99]

            # save here to get the pk and name the (optional) img with it
            news.save()

            if 'image' in request.FILES:
                img = request.FILES['image']
                ext = string.lower(img.name.split('.')[-1])

                if img.size > 10*1024*1024:
                    return render(request, template_name, {'msg' : 'Erreur : Fichier trop lourd', 'news': news})
                if ext not in ('png', 'jpg', 'jpeg', 'gif', 'tiff', 'bmp'):
                    return render(request, template_name, {'msg' : 'Erreur : Extension non reconnue, le fichier n\'est pas une image', 'news': news})

                # remove old img (if one)
                if news.image.name:
                    img_path = os.path.join(settings.MEDIA_ROOT, str(news.image.name))
                    if os.path.exists(img_path):
                        os.remove(img_path)

                # add new img
                news.image = img
                news.image.name = '.'.join((str(news.pk), ext))
                news.save()

            # Redirect after successfull POST
            return HttpResponseRedirect(reverse('news:detail', args=(news.id,)))
        # missing data
        else:
            return render(request, template_name, {'msg': 'Erreur : un champ obligatoire n\'a pas ete rempli', 'news': news})
    # if no post data sent ...
    else:
        return render(request, template_name, {'news': news,})


