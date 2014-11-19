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
system('rm ../db.sqlite3')
print '=> Done'

###########
# CONF DB
###########

# sync db
print '=> Sync db + migrate'
system('python manage.py syncdb --noinput')
system('./manage.py migrate')
print '=> Done'

###########
# ADD DATA
###########
# create super user
print '=> Creating super user ...'
code = (
    "from django.contrib.auth.models import User",
    "user = User.objects.create_superuser('Nodraak', 'chardond@ece.fr', 'mdp')",
)
system('echo "%s" | ./manage.py shell' % '\n'.join(code))
print '=> Done'

# load data
print '=> Loading fixtures ...'
for fixture in fixtures:
    print '=> %s :' % fixture
    system('python manage.py loaddata %s' % fixture)
print '=> Done'

print '=> Loading data from old website'
system('./manage.py loaddata prod/f_auth.yaml')
system('./manage.py loaddata prod/f_member.yaml')
system('./manage.py loaddata prod/f_pub.yaml')
print '=> Done'

print '#####\n# TODO : Creer un profil pour Nodraak\n#####'
