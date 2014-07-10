from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.decorators import login_required

import string
import os

from iTeam.publications.models import Publication

# Create your views here.

def index(request):
    TYPES = ('N', 'T', 'P')

    # get objects
    publications_list = Publication.objects.all().filter(pub_date__lte=timezone.now(), is_draft=False).order_by('-pub_date')

    type = request.GET.get('type')
    if type in TYPES:
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
    data = {"data":publications, "cur_type":type}

    # add active field to proper filter
    if type in TYPES:
        data[''.join(("type_", type))] = "active"
    else:
        data['type_all'] = "active"

    return render(request, 'publications/index.html', data)


def detail(request, publication_id):
    publication = get_object_or_404(Publication, pk=publication_id)

    if (not publication.is_draft) or (request.user.pk == publication.author.pk): # publication.pub_date > timezone.now()
        if request.method == 'POST':
            if 'toggle_draft' in request.POST:
                publication.is_draft = not publication.is_draft
                publication.save()

        return render(request, 'publications/detail.html', {'publication': publication,})
    else:
        raise Http404


@login_required
def create(request):
    publication = Publication()
    return save_publication(request, 'publications/create.html', publication)

@login_required
def edit(request, publication_id):
    publication = get_object_or_404(Publication, pk=publication_id)

    if publication.author.pk is request.user.pk:
        return save_publication(request, 'publications/edit.html', publication)
    else:
        raise Http404


def save_publication(request, template_name, publication):
    # If the form has been submitted ...
    if request.method == 'POST':
        if request.POST['title'] and request.POST['text'] and request.POST['type'] and request.POST['is_draft']:
            # required and auto fields
            publication.author = request.user
            publication.pub_date = timezone.now()

            publication.title = request.POST['title'][:settings.SIZE_MAX_TITLE]
            publication.text = request.POST['text']
            publication.type = request.POST['type']
            publication.is_draft = request.POST['is_draft'];

            # optional fields
            if 'subtitle' in request.POST:
                publication.subtitle = request.POST['subtitle'][:settings.SIZE_MAX_TITLE]

            # save here to get the pk and name the (optional) img with it
            publication.save()

            if 'image' in request.FILES:
                img = request.FILES['image']
                ext = string.lower(img.name.split('.')[-1])

                if img.size > settings.SIZE_MAX_IMG:
                    return render(request, template_name, {'msg' : 'Erreur : Fichier trop lourd', 'publication': publication})
                if ext not in ('png', 'jpg', 'jpeg', 'gif', 'tiff', 'bmp'):
                    return render(request, template_name, {'msg' : 'Erreur : Extension non reconnue, le fichier n\'est pas une image', 'publication': publication})

                # remove old img (if one)
                if publication.image.name:
                    img_path = os.path.join(settings.MEDIA_ROOT, str(publication.image.name))
                    if os.path.exists(img_path):
                        os.remove(img_path)

                # add publication img
                publication.image = img
                publication.image.name = '.'.join((str(publication.pk), ext))
                publication.save()

            # Redirect after successfull POST
            return HttpResponseRedirect(reverse('publications:detail', args=(publication.id,)))
        # missing data
        else:
            return render(request, template_name, {'msg': 'Erreur : un champ obligatoire n\'a pas \xc3t\xc3 rempli', 'publication': publication})
    # if no post data sent ...
    else:
        return render(request, template_name, {'publication': publication,})


