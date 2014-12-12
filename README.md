# Iteam.org

[ITeam](http://iteam.org) is a french association for promoting free softwares from the french engineering school [ECE](http://ece.fr).

Notes :

* commands may need `sudo`
* `python` is an alias to the proper version of python 2.x

## Dependencies

* *Python 2.x*, its framework *Django*, the python package installer *pip* and some dependencies :
```shell
apt-get install python2.7 python2.7-dev sqlite3
apt-get install python-pip
pip install -r requirements.txt
```
If the install of pillow fail (on mac osx for example), try :
```shell
sudo su -
export CFLAGS=-Qunused-arguments
pip install pillow
```

or ubuntu :
```shell
export CFLAGS=""
export CPPFLAGS=""
pip install pillow
```

* *Ruby*, *compass* (compile the sass/scss to css) and *zurb-foundation* (css responsive framework) :

Be carrefull with the versions :

* Ruby 1.8(.7)
* Sass 3.4(.5)
* Foundation 4

```shell
apt-get install ruby
gem install compass zurb-foundation

# if it dont work, try :
# apt-get install ruby-compass
# gem uninstall sass && gem install sass --version 3.4.5
```

## Setting up the stuff and run the server

* Compiling the .css stylessheets :
```shell
compass compile assets/
```

* Configuring the database :
```shell
python manage.py syncdb
```

* Running the server :
```shell
python manage.py runserver
```
The server will be available at <http://localhost:8000>

## License and Copyright

ITeam.org is brought to you under GNU Affero General Public Licence version 3+. For further informations please read the LICENSE file.

Special thanks to the open source projects [Progdupeu.pl](http://progdupeu.pl) ([source code](http://bitbucket.org/MicroJoe/progdupeupl/)) and [zestedesavoir.com](http://zestedesavoir.com) ([source code](https://github.com/zestedesavoir/zds-site)). Some code may come from them.

## Dev

*Require other dependencies : coverage and flake8, install them via pip*

* Clearing everything and loading initial datas :
```shell
python loadFixtures.py
```

* launching tests :
```shell
python manage.py test
```

* test coverage :
```shell
coverage erase && coverage run ./manage.py test
coverage html && open htmlcov/index.html
```

* code checking (pep8) :
```shell
flake8 . --max-line-length=120
```

## prod todo

https://docs.djangoproject.com/en/1.6/topics/security/

python manage.py clearsessions

apt-get install Apache2 Django
apt-get install libapache2-mod-wsgi

configure apache2 -> cf tuto zds
