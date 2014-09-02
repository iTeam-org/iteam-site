
"""

https://developers.facebook.com/docs/graph-api/reference/v2.0/user/feed
https://github.com/simplegeo/python-oauth2


https://github.com/omab/python-social-auth
http://psa.matiasaguirre.net/
http://python-social-auth.readthedocs.org/en/latest/

"""


import facebook
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils import timezone

from iTeam.medias.models import Facebook

import requests

app_id = '1504292026482703'
app_secret = 'af32525c8a08a66c54579a5ff8e90a7e'
redirect_uri = 'http%3A%2F%2Flocalhost%3A8000%2Fmedias%2Ffb_get_token%2F'
scope = 'publish_actions'


def fb(request):
    print 'page : fb'

    data_list = Facebook.objects.all()
    if data_list:
        data = data_list[0]

    if data_list and data and (data.expires > timezone.now()):
        return render(request, 'medias/fb.html', {'have_token': 1})
    else:
        if data_list and data:
            data.delete()
        return render(request, 'medias/fb.html', {'have_token': 0})


def fb_post(request):
    print 'page : fb_post'

    data_list = Facebook.objects.all()
    if data_list:
        data = data_list[0]

    if not (data_list and data and (data.expires > timezone.now())):
        if data_list and data:
            data.delete()
        return render(request, 'medias/fb_post.html', {'have_token': 0})
    else:
        if request.method == 'POST':
            graph = facebook.GraphAPI(data.access_token)
            response = graph.put_object("me", "feed", message=request.POST['text'])
            return render(request, 'medias/fb_post.html', {'result': 'post ok (maybe) : %s' % response})
        else:
            return render(request, 'medias/fb_post.html', {'have_token': 1})


def fb_get_token(request):
    print 'page : fb_get_token'

    ###
    # Getting new access_token from code
    ###
    if 'code' in request.GET:
        print 'code in request.get'
        code = request.GET['code']
        url_login_dialog = 'https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s' % (app_id, redirect_uri, app_secret, code)
        r = requests.post(url_login_dialog)
        print r.text
        return redirect(url_login_dialog)
        #return render(request, 'medias/fb_post.html', {'have_token': 1})
    else:
        print 'NOT code in request.get'

    ###
    # New access token
    ###
    if ('access_token' in request.GET) and ('expires' in request.GET):
        print 'access_token and expires in request.get'
        data = Facebook()
        data.access_token = str(request.GET['access_token'])
        data.expires = timezone.now() + timedelta(seconds=int(request.GET['expires_in']))
        data.save()
        return render(request, 'medias/fb_post.html', {'have_token': 1})
    else:
        print 'NOT access_token and expires in request.get'

    # default
    print 'default'
    url_login_dialog = 'https://graph.facebook.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code&scope=%s' % (app_id, redirect_uri, scope)
    return redirect(url_login_dialog)

