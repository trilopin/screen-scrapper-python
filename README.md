cd /opt && wget --no-check-certificate https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2 && tar xvjf phantomjs-1.9.8-linux-i686.tar.bz2
apt-get install redis-server fontconfig ttf-mscorefonts-installer
export C_FORCE_ROOT=1
/etc/init.d/redis-server start
