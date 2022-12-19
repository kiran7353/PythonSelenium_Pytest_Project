import glob
import os
import shutil
from pathlib import Path

import pytest
from selenium import webdriver

driver = None
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath("Selenium_Python_PytestFramework")))
CHROME_DRIVER_PATH = PROJECT_DIR + "\\ExecutableDrivers\\chromedriver.exe"
FIREFOX_DRIVER_PATH = PROJECT_DIR + "\\ExecutableDrivers\\geckodriver.exe"
for path in Path(PROJECT_DIR + "\\TestResults").glob("**/*"):
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )


@pytest.fixture(scope="class")
def setup(request):
    global driver
    if os.path.exists(PROJECT_DIR + "\\tests\\output.json"):
        os.remove(PROJECT_DIR + "\\tests\\output.json")
        os.remove(PROJECT_DIR + "\\tests\\pytest_html_report.html")
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    elif browser_name == "firefox":
        driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH)
    elif browser_name == "IE":
        print("IE driver")
    driver.get("https://rahulshettyacademy.com/angularpractice/")
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.close()
    if os.path.exists(PROJECT_DIR + "\\tests\\output.json"):
        os.remove(PROJECT_DIR + "\\tests\\output.json")
        os.remove(PROJECT_DIR + "\\tests\\pytest_html_report.html")


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(PROJECT_DIR + "\\TestResults\\" + file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)
