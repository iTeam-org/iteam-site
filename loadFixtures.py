
from os import system

fixtures = (
    'fixtures/auth.yaml',
    'fixtures/member.yaml',
    'fixtures/news.yaml',
    )

# clean everything
system('python manage.py sqlclear member | python manage.py dbshell')
system('python manage.py sqlclear auth | python manage.py dbshell')
system('python manage.py sqlclear news | python manage.py dbshell')
system('python manage.py syncdb')

# load data
system('python manage.py loaddata {0}'.format(' '.join(fixtures)))
