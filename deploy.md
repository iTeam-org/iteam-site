# Todo
* robots.txt
* stats (Munin)
* ssl
* for future commit : migrate db


# Todo while running
```
python manage.py clearsessions
```

# Doc

* Official
  * http://docs.python-guide.org/en/latest/dev/virtualenvs/
  * http://gunicorn.org/
  * http://nginx.org/ + http://nginx.org/en/docs/beginners_guide.html
  * www.robotstxt.org
* Tuto
  * https://github.com/zestedesavoir/zds-site/blob/dev/doc/deploy.md
  * https://github.com/zestedesavoir/zds-site/blob/dev/server/deploy.sh
  * http://goodcode.io/blog/django-nginx-gunicorn/
* Django
  * https://docs.djangoproject.com/en/1.6/topics/security/
  * https://docs.djangoproject.com/en/dev/howto/deployment/checklist/
  * https://docs.djangoproject.com/en/dev/topics/security/#user-uploaded-content-security
  * https://code.djangoproject.com/wiki/DjangoAndNginx?version=17


# Django settings : `settings_prod.py`

```python
# disabble debug
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['www.crepes-bretonnes.com', '.super-crepes.fr']


# DB connection + memcache
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zdsdb',
        'USER': 'zds',
        'PASSWORD': 'mot_de_passe',
        'HOST': 'localhost',
        'PORT': '',
    }
    ... memchace ?
}

# mail + admin
SERVER_EMAIL = 'adresse@domain.com'
EMAIL_BACKEND = ...

ADMINS = (('Maxime Lorant', 'maxime@crepes-bretonnes.com'),)

EMAIL_HOST = 'mail.geoffreycreation.com'
EMAIL_HOST_USER = 'zds@geoffreycreation.com'
EMAIL_HOST_PASSWORD = 'mot_de_passe'
EMAIL_PORT = 25

# Static files :
Static files are automatically served by the development server.
# In production, you must define a STATIC_ROOT directory where
# collectstatic will copy them.
# See Managing static files (CSS, images) for more information.

STATIC_ROOT = ...
STATIC_URL = ...

# user uploaded files
# Media files are uploaded by your users. They’re untrusted !
# Make sure your web server never attempt to interpret them.
# For instance, if a user uploads a .php file, the web server
# shouldn’t execute it.
# Now is a good time to check your backup strategy for these files.

MEDIA_ROOT = ...
MEDIA_URL = ...

# https (ssl ?)
HTTPS = ...
CSRF_COOKIE_SECURE = True # Set this to True to avoid transmitting the CSRF cookie over HTTP accidentally.
SESSION_COOKIE_SECURE = True # Set this to True to avoid transmitting the session cookie over HTTP accidentally.

# errors templates
# 403, 404 and 500 templates (500 template should be raw html)


```


# WSGI (from client to django) + static files

| Paramètre       | Valeur   |
|-----------------|----------|
| Moteur WSGI     | Gunicorn |
| Serveurs web    | Nginx    |
| Contrôle des process | Supervisor |
| Surveillance    | Munin    |
| SGBD            | MySQL (zds) / PostgreSQL (pdp) |

```
apt-get install virtualenv
```

## Virtualenv

```
pip install virtualenv
virtualenv zdsenv --python=python2
```

À chaque fois que vous souhaitez travailler dans votre environement, activez le via la commande suivante :

```
source zdsenv/bin/activate
```

-> For more info cf. doc

## Gunicorn

Installer Gunicorn dans le virtualenv.

```
pip install gunicorn
gunicorn myproject.wsgi
```

Dans /opt/zdsenv/unicorn_start :

```bash
#!/bin/bash

NAME="ZesteDeSavoir"
DJANGODIR=/opt/zdsenv/ZesteDeSavoir/
SOCKFILE=/opt/zdsenv/bin/gunicorn.sock
USER=zds
GROUP=root
NUM_WORKERS=5                         # how many worker processes : should be nb_cpu*2+1
DJANGO_SETTINGS_MODULE=zds.settings   # django settings file
DJANGO_WSGI_MODULE=zds.wsgi           # WSGI modul

echo "Starting $NAME"

# Activate the virtual environment
cd $DJANGODIR
source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--user=$USER --group=$GROUP \
--log-level=debug \
--timeout=300 \
--bind=unix:$SOCKFILE

### --log-file=$LOGFILE 2>>$LOGFILE ????

```

check gunicorn conf : `gunicorn --check-config APP_MODULE`

## Nginx

### Official doc

Conf file : `nginx.conf`, placed in `/usr/local/nginx/conf`, `/etc/nginx` or `/usr/local/etc/nginx`.

To start nginx, run the executable file. Once nginx is started, it can be controlled by invoking the executable with the -s parameter. Use the following syntax:

    nginx -s signal

Where signal may be one of the following:

    stop — fast shutdown
    quit — graceful shutdown
    reload — reloading the configuration file
    reopen — reopening the log files


```
http
{
    server
    {
        location /
        {
            root /data/www;
        }

        location /images/
        {
            root /data;
        }
    }
}


```

### ZDS

Installer nginx. Sous Debian, la configuration est splittée par site. Pour Zeste de Savoir elle se fait dans `/etc/nginx/sites-available/zestedesavoir` :

zds doc :

```bash
upstream zdsappserver {
    server unix:/opt/zdsenv/bin/gunicorn.sock fail_timeout=0;
}
server {
    server_name www.zestedesavoir.com;
    rewrite ^(.*) http://zestedesavoir.com$1 permanent;
}
server {
    listen [::]:80 ipv6only=on;
    listen 80;

    listen 443 ssl;
    ssl_certificate /etc/ssl/certs/zds/server.crt;
    ssl_certificate_key /etc/ssl/certs/zds/server.key;
    ssl_protocols SSLv3 TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers HIGH:!aNULL:!MD5;

    server_name zestedesavoir.com;
    gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
    #access_log off;
    access_log /opt/zdsenv/logs/nginx-access.log;
    error_log /opt/zdsenv/logs/nginx-error.log;

    #location = /robots.txt {
    #    alias /opt/zdsenv/ZesteDeSavoir/robots.txt ;
    #}

    location /static/admin/ {
        alias /opt/zdsenv/lib/python2.7/site-packages/django/contrib/admin/static/admin/;
    }

    location /static/ {
        alias /opt/zdsenv/ZesteDeSavoir/dist/;
        expires 1d;
        add_header Pragma public;
        add_header Cache-Control "public, must-revalidate, proxy-revalidate";
    }

    location /media/ {
        alias /opt/zdsenv/ZesteDeSavoir/media/;
        expires 1d;
        add_header Pragma public;
        add_header Cache-Control "public, must-revalidate, proxy-revalidate";
    }

    location / {
            #if ($http_host ~* "^www\.(.+)$"){
                #rewrite ^(.*)$ http://%1$request_uri redirect;
            #}
            if ($uri !~ \. ){
                rewrite ^(.*[^/])$ $1/ permanent;
            }
            client_max_body_size 100M;
            proxy_read_timeout 1000s;
            proxy_connect_timeout 1000s;

            auth_basic "Qui es-tu noble etranger ?";
            auth_basic_user_file  /home/zds/.htpasswdclose;
            ####proxy_pass http://176.31.187.88:8001;

            proxy_set_header X-Forwarded-Host $server_name;
            proxy_set_header X-Forwaded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header REMOTE_ADDR $remote_addr;
            
            add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
            if (!-f $request_filename) {
                proxy_pass http://zdsappserver;
                break;
            }

      }
    # Error pages
    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root /opt/zdsenv/ZesteDeSavoir/templates/;
    }
}
```

random doc :

```bash
location / {
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_connect_timeout 10;
        proxy_read_timeout 10;
        proxy_pass http://localhost:8000/;
    }
```

gunicorn doc :

```bash
location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
```

## Supervisor

La conf dans `/etc/supervisor/conf.d/zds.conf` permet de lancer Sdz à l'aide de `supervisorctl start zds` et l'arrêter avec `supervisorctl stop zds`.

```bash
[program:zds]
command = /opt/zdsenv/unicorn_start ;
user = zds ;
stdout_logfile = /opt/zdsenv/logs/gunicorn_supervisor.log ;
redirect_stderr = true ;
```

## Munin
-> cf doc github zds

