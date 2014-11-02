# How to deploy

* Install fresh server (ubuntu / debian ?)
* virtualenv
    * apt-get install python-virtualenv
    * (once) sudo virtualenv /opt/iteam-env
    * (each time we work) source bin/activate
    * (to exit the virtual env) deactivate
* App
    * git clone
    * standard install : cf README.md
    * mkdir media + static + log (inside app or .. ?)
    * cp settings_prod.py iTeam/ : change infos + db (mysql / postgresql)
    * python manage.py collectstatic
    * python manage.py : syncdb + migrate + loaddata
* Nginx
    * apt-get install
    * Conf file :
        * `cp prod/nginx.conf /etc/nginx/sites-available/iteam` + maintenance
        * `vim /etc/nginx/sites-available/iteam` -> static/ + media/ path
        * cp favicon robots.txt + check conf file
        * `ln -s /etc/nginx/sites-available/iteam /etc/nginx/sites-enabled/iteam`
    * check nginx conf : `nginx -t`
* Gunicorn
    * `pip install gunicorn`
    * `cp prod/gunicorn_start.sh gunicorn_start.sh`
    * `vim gunicorn_start.sh`
    * check gunicorn conf : `gunicorn --check-config APP_MODULE`
* Supervisor
    * `cp prod/supervisor.conf /etc/supervisor/conf.d/iteam.conf`
    * `vim /etc/supervisor/conf.d/iteam.conf`
    * Mise a jour de la conf de supervisor : `supervisorctl reread` puis `supervisorctl reload`
    * démarrer et arréter le serveur : `supervisorctl start zds` et `supervisorctl stop zds`
* Bobonuxnux
    * django : log + disable django admin ??
    * backup : db.sqlite3 + media/
    * Nginx : gzip + www. -> redirection
    * memcache / redis
    * Munin (stat) -> cf zds code
    * for future commit : migrate db
    * `python manage.py clearsessions`
    * solr ?

```python
    publications = Publication.objects.all()

    from __future__ import unicode_literals
    from os import system
    import sys

    for p in publications:
        # write to file
        tmp_html = open('tmp.html', 'w')
        text_html = p.text.encode('utf8')
        tmp_html.write(text_html)
        tmp_html.flush()

        # call pandoc
        system('pandoc tmp.html -o tmp.md')

        # load from file
        tmp_md = open('tmp.md', 'r')
        text_md = tmp_md.read().decode('utf8')
        p.text = '\n\n'.join((p.text, '```text', text_md, '```'))
        p.save()

        system('rm tmp.html tmp.md')
```

**Resumé des technos utilisées :**

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
* migrate http://www.djangopro.com/2011/01/django-database-migration-tool-south-explained/



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


## Munin
-> cf doc github zds

