"""Claas screenshot"""
import os
from PIL import Image
import redis
import StringIO
import uuid
from screenscrapper.util import validate_url


class ScreenShot(object):
    """Screenshot class"""

    def __init__(self, **kwargs):
        if 'phantom' in kwargs.keys():
            self.phantom = kwargs['phantom']

        if 'redis' in kwargs.keys():
            self.redis = redis.StrictRedis(host=kwargs['redis'])


    def get(self, url, size):
        """Get image from database"""
        return self.redis.get(self._unique_key(url, size))


    def exists(self, url, size):
        """Check if exists in redis storage"""
        return self.redis.exists(self._unique_key(url, size))


    def take(self, url, size):
        """Take screenshot: get unique filename,
        pass data to phantomjs and call redis storage"""
        if not validate_url(url) or self.exists(url, size):
            return

        tmpname = self._unique_path(size)
        print url
        script = os.path.dirname(os.path.abspath(__file__)) + \
                    '/take_screenshot.js'
        command = self.phantom + " " + \
                  script + " " + \
                  url + " " + \
                  tmpname + \
                  " {0}px*{1}px".format(size['width'], size['height'])
        os.system(command)
        self._store_image(url, size, tmpname)


    def _unique_path(self, size):
        """Unique tmpfile for temp file"""
        return '/app/{0}_{1}x{2}.png'.format(uuid.uuid4(),
                                             size['width'],
                                             size['height'])


    def _unique_key(self, url, size):
        """Unique Key for redis storage"""
        return '{1}x{2}__{0}'.format(url.replace('http://', '').strip(),
                                     size['width'],
                                     size['height'])

    def _store_image(self, url, size, filename):
        """Store image in redis: use StringIO and Pillow image management"""
        output = StringIO.StringIO()
        image = Image.open(filename)
        image.save(output, format=image.format, optimize=True, quality=80)
        self.redis.set(self._unique_key(url, size), output.getvalue())
        output.close()
        os.remove(filename)

