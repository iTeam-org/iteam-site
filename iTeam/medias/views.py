
from django.shortcuts import render
from django.shortcuts import redirect

import requests
import urlparse
import facebook
from django.utils import timezone
from datetime import timedelta

from iTeam.medias.models import Facebook

app_id = '1534380566781826'
app_secret = '0ec2c70bb4defc3710200b3cefa6236e'
redirect_uri = 'http://localhost:8000/medias/fb/'
scope = 'publish_actions'


def fb(request):
    # if we want to post something
    if request.method == 'POST':
        print '==>> method == POST'

        data_list = Facebook.objects.all()
        if data_list:
            data = data_list[0]

        # check acces token
        if data_list and data and (data.expires > timezone.now()):
            print '==>> acces_token ok, posting'
            return fb_post_msg(data.access_token, request.POST['text'])
        else:
            print '==>> bad access_token, getting a new one'

            if data_list and data:
                data.delete()

            return fb_get_acces_token(request)

    # if we are getting a new access_token
    print request.GET
    if 'access_token' in request.GET:
        print '==>> get access_token ok'

        access_token = str(request.GET['access_token'])
        expires = int(request.GET['expires_in'])
        print 'access_token=%s' % access_token

        data = Facebook()
        data.access_token = access_token
        data.expires = timezone.now() + timedelta(seconds=expires)
        data.save()

        return render(request, 'medias/fb.html', {'result': 'access_token ok, you may post now'})

    # default, method != POST and not asking for new code / acces_token
    return render(request, 'medias/fb.html', {'result': 'default'})


def fb_get_acces_token(request):
    print '==>> Gettting access_token'

    url_login_dialog = 'https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&response_type=token&scope=%s' % (app_id, redirect_uri, scope)

    return redirect(url_login_dialog)


def fb_post_msg(access_token, msg):
    print '==>> Posting'
    graph = facebook.GraphAPI(access_token)
    response = graph.put_object("me", "feed", message=msg)
    return render(request, 'medias/fb.html', {'result': 'post ok : %s' % response})

