A lire :
* https://github.com/zestedesavoir/zds-site/wiki/Surveillance-du-serveur-avec-Munin
* http://supervisord.org/running.html
* http://docs.gunicorn.org/en/latest/configure.html
* http://stackoverflow.com/questions/12063463/where-is-the-gunicorn-config-file
* conf file https://github.com/Remiz/playbook-demo/tree/master/templates
* graph pr une eventuelle forma http://sametmax.com/quest-ce-que-wsgi-et-a-quoi-ca-sert/
* munin http://sametmax.com/monitorez-vos-serveurs-avec-munin-et-notifications-par-email/
* django cache https://docs.djangoproject.com/en/dev/topics/cache/
* nginx + static + gzip : http://sametmax.com/servir-des-fichiers-statiques-avec-nginx/


# How to

**Deploy :**
* Install fresh server (ubuntu / debian ?)
* Install prod
  * virtualenv
    * apt-get install python-virtualenv
    * (once) sudo virtualenv /opt/iteam-env
    * (each time we work) source bin/activate
    * (to exit the virtual env) deactivate
  * App
     * git clone
     * standard install : cf README.md
     * mkdir media + static (inside app or .. ?)
     * cp settings_prod.py iTeam/ : change infos + db (mysql / postgresql)
     * python manage.py collectstatic
     * python manage.py syncdb (loadFixtures ?)
  * Nginx
     * apt-get install
     * vim / cp ... /etc/nginx/site-available/iteam
     * ln -s ... (cf zds doc)
  * Gunicorn
     * pip install
* Bobonuxnux
  * Supervisor
  * django log ???
  * backup

**Nginx :**
* gzip
* www. -> redirection
* fail2ban (or block django admin ?)

**Todo later :**
* memcache / redis
* Munin (stat) -> cf zds code
* ssl : 443
* for future commit : migrate db
* `python manage.py clearsessions`
* solr ?


| Paramètre       | Valeur   |
|-----------------|----------|
| Serveurs web    | Nginx    |
| Moteur WSGI     | Gunicorn |
| SGBD            | MySQL (zds) / PostgreSQL (pdp) |
| Contrôle des process | Supervisor |
| Surveillance         | Munin      |


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


# Nginx


Conf file : `nginx.conf`, placed in `/usr/local/nginx/conf`, `/etc/nginx` or `/usr/local/etc/nginx`.

`/etc/nginx/sites-available/zestedesavoir` -> cf conf file in `prod/`

To start nginx, run the executable file. Once nginx is started, it can be controlled by invoking the executable with the -s parameter. Use the following syntax:

    nginx -s signal

Where signal may be one of the following:

    stop — fast shutdown
    quit — graceful shutdown
    reload — reloading the configuration file
    reopen — reopening the log files

check nginx conf : `nginx -t`


# Gunicorn

```
pip install gunicorn
```

-> cf `prod/gunicorn_start.sh`


check gunicorn conf : `gunicorn --check-config APP_MODULE`


# Django settings : `settings_prod.py`

A rajouter ?

```python
EMAIL_BACKEND = ???

# DB connection + memcache / redis
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zdsdb',
        'USER': 'zds',
        'PASSWORD': 'mot_de_passe',
        'HOST': 'localhost',
        'PORT': '',
    }
    ... memcache / redis ?
}

# https (ssl ?)
HTTPS = ...
CSRF_COOKIE_SECURE = True # Set this to True to avoid transmitting the CSRF cookie over HTTP accidentally.
SESSION_COOKIE_SECURE = True # Set this to True to avoid transmitting the session cookie over HTTP accidentally.

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

Mise a jour de la conf de supervisor :
```
supervisorctl reread
supervisorctl reload
```

## Munin
-> cf doc github zds

