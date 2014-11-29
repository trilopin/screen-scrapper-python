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
