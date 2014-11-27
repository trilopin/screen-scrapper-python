import os
from PIL import Image
import redis
import StringIO
import uuid


class ScreenShot(object):
    """Screenshot class"""

    def __init__(self, *args, **kwargs):
        if 'phantom' in kwargs.keys():
            self.phantom = kwargs['phantom']

        if 'redis' in kwargs.keys():
            self.redis = kwargs['redis']

    def take(self,url,size):
        """Take screenshot"""
        print "Take {0} - {1}".format(url,size['width'])
        tmpname = self._unique_path(size)
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
        """Path for temp file"""
        return '/app/{0}_{1}x{2}.png'.format(uuid.uuid4(),
                                             size['width'],
                                             size['height'])

    def _unique_key(self, url, size):
        """Key for redis store"""
        return '{0}||=>w={1}&h={2}'.format(url,
                                           size['width'],
                                           size['height'])

    def _store_image(self, url, size, filename):
        """Store image in redis"""
        output = StringIO.StringIO()
        image = Image.open(filename)
        image.save(output, format=image.format, optimize=True)
        red = redis.StrictRedis(host=self.redis)
        red.set(self._unique_key(url, size), output.getvalue())
        output.close()
        os.remove(filename)
