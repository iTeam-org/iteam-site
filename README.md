# Iteam.org

[ITeam](http://iteam.org) is a french association of the french engineering school [ECE](http://ece.fr).

Notes :

* commands may need `sudo`
* `python` is an alias to the proper version of python 2.x

## Dependencies

* Python 2.x, its framework Django, the python package installer pip and some dependencies
```shell
apt-get install python2.7 python2.7-dev
apt-get install python-pip
pip install -r requirements.txt
```

* Ruby and other dependencies (to generate CSS files)
```shell
apt-get install ruby
gem install --user-install compass zurb-foundation
```

## Setting up the stuff and run the server

* Compiling the .css stylessheets
```shell
compass compile static/
```

* Configuring the database
```shell
python manage.py syncdb
```

* Running the server
```shell
python manage.py runserver
```
The server will be available at <http://localhost:8000>

## Tests

* Generating fake datas
```shell
python loadFixtures.py
```

* Cleaning the stuff that has just been created (or just comment the proper line in loadFixtures.py and run it again)
```shell
python manage.py sqlclear member | python manage.py dbshell
python manage.py sqlclear auth | python manage.py dbshell
python manage.py sqlclear news | python manage.py dbshell
```

## Copyright

ITeam uses some code of the [AGPL licensed](http://bitbucket.org/MicroJoe/progdupeupl/) project [Progdupeu.pl](http://progdupeu.pl)

