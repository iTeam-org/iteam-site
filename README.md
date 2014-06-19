# Iteam.org

[ITeam](iteam.org) is a french association of the french engineering school [ECE](ece.fr).

Notes :

* commands may need `sudo`
* `python` is an alias to the proper version of python 2.x

## Dependencies

* Python 2.x (and its framework Django)
```shell
apt-get install python2.7 python2.7-dev
apt-get install python-pip
```
* Ruby (for the static files .css)
```shell
apt-get install ruby
```
* Python dependencies
```shell
pip install -r requirements.txt
```
* Ruby dependencies (to generate CSS files)
```shell
gem install --user-install compass zurb-foundation
```

## Seting up the stuff

* Creating tables for the database
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

ITeam uses some code of the [AGP licensed](https://bitbucket.org/MicroJoe/progdupeupl/) project [Progdupeu.pl](http://progdupeu.pl)

