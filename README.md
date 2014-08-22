# Iteam.org

[ITeam](http://iteam.org) is a french association for promoting free softwares from the french engineering school [ECE](http://ece.fr).

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

## Tests and initial datas

* Clearing everything and loading initial datas
```shell
python loadFixtures.py
```

* launching test
```shell
./manage.py test
```

## License and Copyright

ITeam.org is brought to you under GNU Affero General Public Licence version 3+. For further informations please read the LICENSE file.

Special thanks to the open source projects [Progdupeu.pl](http://progdupeu.pl) ([source code](http://bitbucket.org/MicroJoe/progdupeupl/)) and [zestedesavoir.com](http://zestedesavoir.com) ([source code](https://github.com/zestedesavoir/zds-site)). Some code may come from them.


## Dev
### test coverage
```shell
coverage erase && coverage run --omit="/Library/*" --branch --timid ./manage.py test
coverage html && open htmlcov/index.html
```

### code checking (pep8)
```shell
flake8 . --max-line-length=120 --exclude=medias
```

### db dump
```shell
python manage.py dumpdata --format=yaml --natural member > data.yaml
```

## prod

https://docs.djangoproject.com/en/1.6/topics/security/

./manage.py clearsessions

apt-get install Apache2 Django
apt-get install libapache2-mod-wsgi

configure apache2 -> cf tuto zds
