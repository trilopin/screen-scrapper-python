#!/usr/bin/python
# -*- coding: utf -*-
"""Application main"""
from flask import Flask, render_template, request, abort, Response, url_for, jsonify
from screenscrapper.config import STORE_URL
from screenscrapper.tasks import take_screenshot
from screenscrapper.screenshot import ScreenShot
from screenscrapper.util import validate_url
import jinja2
import time

app = Flask(__name__,static_url_path='/assets',static_folder='assets')
app.debug = True

#secs wait for long polling mode
LONG_POLLING_TIMEOUT = 60
LONG_POLLING_TICK = 0.5

@app.route('/', methods=['GET'])
def home():
    """Site homepage"""
    return render_template('home.html')


@app.route('/', methods=['POST'])
def enqueue():
    """Enqueue one url with multiple sizes"""
    if 'url' not in request.form \
            or 'sizes' not in request.form \
            or not validate_url(request.form['url']):
        abort(400)
    try:
        sizes = []
        images = []
        url = request.form['url'].replace('http://','')
        for line_size in request.form['sizes'].split("\n"):
            parts = line_size.strip().split('x')
            if len(parts)==2:
                size = {'width':parts[0], 'height':parts[1]}
                sizes.append(size)
                take_screenshot.delay(request.form['url'], size)
                image_src = url_for('image',size="{0}x{1}".format(parts[0],parts[1]),url=url)
                images.append( {'src':image_src,'size': size} )
        return jsonify( **{'images':images, 'url':url} )
    except Exception, e:
        return str(e)


@app.route('/screenshot/<size>/http://<path:url>', methods=['GET'])
@app.route('/screenshot/<size>/https://<path:url>', methods=['GET'])
def image(size,url):
    """Request image for one url and size"""

    img = None
    init_time = time.time()

    size = size.strip().split('x')
    size = {'width':size[0],'height':size[1]}

    screenshot = ScreenShot(redis=STORE_URL)

    #long polling with timeout
    while img == None and time.time()-init_time < LONG_POLLING_TIMEOUT:
        time.sleep(LONG_POLLING_TICK)
        img = screenshot.get(url,size)

    #result
    if img != None:
        return Response(img, mimetype='image/png')
    else:
        abort(404)


if __name__ == '__main__':
    app.run(host= '0.0.0.0')
