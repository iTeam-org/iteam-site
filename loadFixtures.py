
from os import system

apps = (
    'auth',
    'member',
    'news',
)

fixtures = (
    'fixtures/auth.yaml',
    'fixtures/member.yaml',
    'fixtures/news.yaml',
    )

# clean everything
print '=> Cleaning everything ...'
for app in apps:
    system('python manage.py sqlclear %s | python manage.py dbshell' % app)
print '=> Done'

# sync db
print '=> Sync db ...'
system('python manage.py syncdb')
print '=> Done'

# load data
print '=> Loading fixtures ...'
for fixture in fixtures:
    print '=> %s :' % fixture
    system('python manage.py loaddata %s' % fixture)
print '=> Done'
