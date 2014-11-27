from screenscrapper.tasks import take_screenshot

if __name__ == '__main__':

    sizes = [{'label': 'Desktop 19', 'width': 1280, 'height': 800},
             {'label': 'Desktop 17', 'width': 1024, 'height': 768},
             {'label': 'Iphone', 'width': 720, 'height': 460},
             {'label': 'Nokia', 'width': 520, 'height': 460},
            ]
    for size in sizes:
        take_screenshot.delay('http://www.amazon.es',size)
