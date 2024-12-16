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
        EC.element_to_be_clickable(("xpath", "//span[text()='Почта']"))
    )
    news_button.click()
    time.sleep(3)
    assert driver.current_url == "https://workspace.google.com/intl/ru/gmail/", "NO"


def test_lucky_button(driver):
    lucky_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("xpath", "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[2]")))
    lucky_button.click()
    assert driver.current_url == "https://doodles.google/"
