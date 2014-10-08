
from os import system

fixtures = (
    'auth.yaml',
    'member.yaml',
    'publications.yaml',
    'events.yaml',
)

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
    '\'Nodraak\', \'nodraak@mail.fr\', \'mdp\')" | ./manage.py shell'
)
print '=> Done'

# load data
print '=> Loading fixtures ...'
for fixture in fixtures:
    print '=> %s :' % fixture
    system('python manage.py loaddata %s' % fixture)
print '=> Done'
