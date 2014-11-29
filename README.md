# Screen scrapper in python

DISCLAIMER:

This code are just for fun and learn.
Still in very early stage.
It will be updated without backwards compatibility.

Based in two components:

  * simple screen scrapper lib
  * web microapp that enqueue and visualize screenshot jobs

###Screen scrapper lib###

Screenshots are made with phantomjs browser.

Jobs are asynchronously processed via celery and stored in redis.

###Web microapp###

Screenshots
*Jobs are asynchronously processed via celery and stored in redis.

##RUN WITH DOCKER###

start redis (https://registry.hub.docker.com/_/redis/)

```bash
sudo docker run --name some-redis -d redis
```

start app (after build)
```bash
sudo docker run -t -i -p 5000:5000 --link some-redis:redis -v LOCAL_APP:/app python/scrapper /bin/bash
```

app run
```bash
celery -A screenscrapper.tasks worker
python server.py
```
##TODO###

  * optimize images, saving memory and network bandwitch
  * web layer with style
  * store metadata in redis: datetime, sizes by each url
  * drop old images in redis with periodic task in celery