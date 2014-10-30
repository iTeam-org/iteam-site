#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import system

fixtures = ()
"""
    'auth.yaml',
    'member.yaml',
    'publications.yaml',
    'events.yaml',
)
"""

###########
# CLEAN
###########
# clean everything
print '=> Cleaning everything ...'
system('rm db.sqlite3')
print '=> Done'

###########
# CONF DB
###########

# sync db
print '=> Sync db ...'
system('python manage.py syncdb --noinput')
print '=> Done'

###########
# ADD DATA
###########
# create super user
print '=> Creating super user ...'
system(
    'echo "from django.contrib.auth.models import User; User.objects.create_superuser('
    '\'Nodraak\', \'chardond@ece.fr\', \'mdp\')" | ./manage.py shell'
)
print '=> Done'

# load data
print '=> Loading fixtures ...'
for fixture in fixtures:
    print '=> %s :' % fixture
    system('python manage.py loaddata %s' % fixture)
print '=> Done'

print '=> Loading prod stuf (migrate + data from old website'
system('./manage.py migrate')
system('./manage.py loaddata prod/f_auth.yaml')
system('./manage.py loaddata prod/f_member.yaml')
system('./manage.py loaddata prod/f_pub.yaml')
print '=> Done'

print '#####\n# TODO : Creer un profil pour Nodraak\n#####'
