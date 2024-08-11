import io
import os
import time
from pathlib import Path
from typing import Callable

import img2pdf
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def take_screenshot(url: str, output: str, on_success: Callable, on_failure: Callable, **kwargs) -> None:
    width: int = kwargs.get('width', 1920)
    height: int | None = kwargs.get('height', None)
    image_format: str = kwargs.get('format', 'PNG').upper()
    file_extension = 'png'
    if image_format not in ['PNG', 'JPG', 'PDF']:
        image_format = 'PNG'
    if image_format == 'JPG':
        image_format = 'JPEG'
        file_extension = 'jpg'
    if image_format == 'PDF':
        file_extension = 'pdf'
    timeout: int = kwargs.get('timeout', 2)

    filename = str(Path(output) / os.path.abspath(output) / f'website_screenshot.{file_extension}')

    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.cookies": 2,
            "profile.block_third_party_cookies": True
        })

        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.get(url)
        time.sleep(timeout)

        if not height:
            height = driver.execute_script(
                'return Math.max(document.body.scrollHeight, document.body.offsetHeight, '
                'document.documentElement.clientHeight, document.documentElement.scrollHeight, '
                'document.documentElement.offsetHeight);')

        driver.set_window_size(width, height)
        image_data = driver.get_screenshot_as_png()

        if image_format == 'PDF':
            pdf_bytes = img2pdf.convert(image_data)

            file = open(filename, "wb")
            file.write(pdf_bytes)
            file.close()
        else:
            image = Image.open(io.BytesIO(image_data))
            image.save(fp=filename, format=image_format.upper())

        driver.quit()
        on_success(f'Screenshot saved as:\n{filename}')
    except Exception as e:
        on_failure(f'Error while taking screenshot of ({url}): \n{e}')
