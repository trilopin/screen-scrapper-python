# ScreenScrapper
#
# VERSION               0.0.1

FROM      phusion/baseimage:latest
MAINTAINER José Manuel Peso <jmpeso@gmail.com>

# -------------------------------------------------
# multiverse repository for ttf-msttcore-fonts
# -------------------------------------------------
RUN echo "deb http://es.archive.ubuntu.com/ubuntu/ trusty multiverse" >> /etc/apt/sources.list

# -------------------------------------------------
# dependencies: redis, python, fonts and wget
# -------------------------------------------------
RUN apt-get update -q && apt-get install -q -y python python-pip redis-server fontconfig ttf-mscorefonts-installer wget python-dev zlib1g-dev

# -------------------------------------------------
# allow use celery as root
# -------------------------------------------------
RUN export C_FORCE_ROOT=1

# -------------------------------------------------
# start redis
# -------------------------------------------------
RUN /etc/init.d/redis-server start

# -------------------------------------------------
# Phantomjs: download, extract, move and clean
# -------------------------------------------------
WORKDIR /tmp
RUN cd /tmp && wget --no-check-certificate https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2 && tar xvjf phantomjs-1.9.8-linux-x86_64.tar.bz2 && mv  /tmp/phantomjs-1.9.8-linux-x86_64/bin/phantomjs  /usr/bin/ && rm -rf /tmp/phantomjs-1.9.8-linux-x86_64/

# -------------------------------------------------
# PIP install dependencies
# -------------------------------------------------
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt