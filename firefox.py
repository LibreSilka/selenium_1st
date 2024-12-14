import time
import pytest
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            # Генерация безопасного имени файла
            safe_name = re.sub(r"[^\w\-.]", "_", item.name)
            screenshot_path = f"screenshots/{safe_name}.png"

            # Сохранение скриншота
            print(f"Saving screenshot to {screenshot_path}")  # Debug
            if driver.save_screenshot(screenshot_path):
                print(f"Screenshot saved: {screenshot_path}")  # Debug

            # Добавление в HTML-отчет
            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html:
                extra = getattr(report, "extra", [])
                extra.append(pytest_html.extras.image(screenshot_path))
                report.extra = extra


# service = Service(EdgeChromiumDriverManager().install())
# driver = webdriver.Edge(service=service)
@pytest.fixture
def driver():
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
    driver.implicitly_wait(10)
    driver.get('https://google.com')
    yield driver
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     rep = outcome.get_result()
#     if rep.when == "call" and rep.failed:
#         driver = item.funcargs.get("driver")
#         if driver:
#             screenshot_path = f"screenshots/{item.name}.png"
#             driver.save_screenshot(screenshot_path)
#             pytest_html = item.config.pluginmanager.getplugin("html")
#             extra = getattr(rep, "extra", [])
#             extra.append(pytest_html.extras.image(screenshot_path))
#             rep.extra = extra
def test_news(driver):
    apps_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(("xpath", "//*[@id='gbwa']/div/a"))
    )
    apps_button.click()

    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(("xpath", "//iframe[@role='presentation']"))
    )
    driver.switch_to.frame(iframe)
    news_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(("xpath", "//span[text()='Новости']"))
    )
    news_button.click()
    assert driver.current_url == "https://news.google.com/home?hl=ru&gl=RU&ceid=RU:r", "NO"

# def test_lucky_button(driver):
#     lucky_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("xpath", "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[2]")))
#     lucky_button.click()
#     assert driver.current_url == "https://doodles.google/"
