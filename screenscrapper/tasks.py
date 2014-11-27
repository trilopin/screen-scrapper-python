from celery import Celery
from screenshot import ScreenShot
from config import BROKER_URL, BACKEND_URL, PHANTOMJS_PATH, STORE_URL


APP = Celery('screenscrapper',
              broker=BROKER_URL,
              backend=BACKEND_URL)

@APP.task
def take_screenshot(url,size):
    """taks take screenshot"""
    screenshot = ScreenShot(phantom=PHANTOMJS_PATH,redis=STORE_URL)
    screenshot.take(url,size)
    #    #PhantomJS Webdriver
    #    driver = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH)
    #
    #    tmpname = '/app/screenshot.png'
    #
    #    #take screenshot
    #    driver.implicitly_wait(20)
    #    driver.set_window_size(1024, 768)
    #    driver.get(url)
    #    driver.get_screenshot_as_file(tmpname)
    #    #driver.get_screenshot_as_png()
    #
    #    #store in redis
    #    output = StringIO.StringIO()
    #    im = Image.open(tmpname)
    #    im.save(output, format=im.format,optimize=True)
    #    r = redis.StrictRedis(host=STORE_URL)
    #    r.set(url, output.getvalue())
    #    output.close()


