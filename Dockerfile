###
# Experimental docker file for iTeam.org
# Nodraak (Adrien Chardon)
#
# http://github.com/Nodraak/Team.org
# htpp://iteam.org
###

FROM ubuntu:14.04

MAINTAINER Nodraak (Adrien Chardon)


###
# Packaged dependencies
###

RUN apt-get update

RUN apt-get install -y \
    build-essential \
    git \
    python2.7 \
    python2.7-dev \
    python-pip \
    sqlite3 \ # mysql / postgresql
    # nginx \
    # gunicorn ?
    # supervisor
    # munin ?
    ruby

RUN gem install --user-install compass zurb-foundation
#RUN export PATH=$PATH:~/.gem/ruby/1.8/bin


###
# Custom dependencies : clone project, install dep and setup the stuff
###

RUN git clone http://github.com/Nodraak/iTeam.org /home/docker/iTeam.org
RUN cd /home/docker/iTeam.org
RUN pip install -r requirements.txt
RUN compass compile assets/
RUN python manage.py syncdb

# RUN /urs/bin/python loadFixtures.py
# python manage.py test


# setup all the configfiles
#RUN echo "daemon off" >> /etc/nginx/nginx.conf
#run rm /etc/nginx/sites-enabled/default
#run ln -s /home/docker/code/nginx-app.conf /etc/nginx/sites-enabled/
#run ln -s /home/docker/code/supervisor-app.conf /etc/supervisor/conf.d/



###
# Start the dock
###

#VOLUME ["/home/docker/code/django"]
#VOLUME ["/var/log"]
#VOLUME  /var/lib/docker-zds

EXPOSE 8000

#CMD ["supervisord", "-n"]
CMD ["/usr/bin/python", "manage.py", "runserver"]

