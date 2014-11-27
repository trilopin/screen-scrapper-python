Screen scrapper in python

This code are just for fun, and learn.

I have developed scrapper through PhantomJS as system call.
Jobs are asynchronously processed via celery and stored in redis.

RUN WITH DOCKER

start redis (https://registry.hub.docker.com/_/redis/)
sudo docker run --name some-redis -d redis

start app
sudo docker run -t -i -p 5000:5000 --link some-redis:redis -v /home/jpeso/git-projects/python/:/app python/scrapper /bin/bash

TODO:

optimize images
tornado/webpy microservice for enqueue jobs and retrieve images
drop old images in redis with periodic task in celery

