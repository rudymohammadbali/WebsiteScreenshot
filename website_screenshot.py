import os
from pathlib import Path

from playwright.sync_api import sync_playwright


def path_exists(path: str) -> bool:
    return os.path.exists(path)


def take_screenshot(url: str, output_path: str, output_format: str) -> bool:
    """
        Captures a full-page screenshot of a website and saves it to the specified output path.

        Args:
            url (str): The URL of the website to capture.
            output_path (str): The folder where the screenshot will be saved.
            output_format (str): The desired output format ('jpg' or 'png').

        Returns:
            bool: True if the screenshot was successfully taken and saved, False otherwise.

        Raises:
            NotADirectoryError: If the output folder does not exist.
            ValueError: If an unsupported output format is specified.
        """
    if not path_exists(output_path):
        raise NotADirectoryError(f"Output folder {output_path} does not exists.")

    formats = ["jpg", "png"]
    output_format = output_format.lower().strip()

    if output_format not in formats:
        raise ValueError(f"Unsupported output format: {output_format}")

    output_name = str(Path(output_path) / f"website_screenshot.{output_format}")

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()

            page = browser.new_page()
            page.goto(url)
            page.screenshot(path=output_name, full_page=True)

            browser.close()
        return True
    except Exception as e:
        print(f"Error take website screenshot for {url}: {e}")
        return False
