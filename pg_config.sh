#!/bin/sh
sudo apt-get -qqy update
sudo apt-get -qqy install postgresql python-pip
sudo apt-get -qqy install python-dev python-setuptools libpq-dev
sudo apt-get -qqy install libtiff5-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

sudo pip install virtualenv
sudo pip install virtualenvwrapper

pip install psycopg2
pip install Flask-SQLAlchemy
pip install Flask-OAuth
pip install Flask-Mail
pip install Flask-Login
pip install Pillow

sudo su postgres -c 'createuser -dRS vagrant'
sudo su vagrant -c 'createdb'
sudo su vagrant -c 'createdb test'
sudo -u postgres psql -c "ALTER USER vagrant WITH PASSWORD 'vagrant';"