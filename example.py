from website_screenshot import take_screenshot


def success_callback(msg: str):
    print(msg)


def failure_callback(msg: str):
    print(msg)


options = {
    "width": 1920,
    "height": None,
    "format": 'png',
    "timeout": 2
}
take_screenshot('https://www.python.org/', './', success_callback, failure_callback, **options)
