
from os import system

apps = (
    'auth',
    'member',
    'publications',
    'medias',
    'events',
)

fixtures = (
    'fixtures/auth.yaml',
    'fixtures/member.yaml',
    'fixtures/publications.yaml',
    'fixtures/events.yaml',
)

###########
# CLEAN
###########
# clean everything
print '=> Cleaning everything ...'
for app in apps:
    system('python manage.py sqlclear %s | python manage.py dbshell' % app)
print '=> Done'

###########
# CONF DB
###########

# sync db
print '=> Sync db ...'
system('python manage.py syncdb --noinput')
print '=> Done'

# add groups
print '=> WARNING remember to create group staff with proper perms'

###########
# ADD DATA
###########
# create super user
print '=> Creating super user ...'
system('echo "from django.contrib.auth.models import User; User.objects.create_superuser(\'Nodraak\', \'nodraak@mail.fr\', \'mdp\')" | ./manage.py shell')
print '=> Done'

# load data
print '=> Loading fixtures ...'
for fixture in fixtures:
    print '=> %s :' % fixture
    system('python manage.py loaddata %s' % fixture)
print '=> Done'
