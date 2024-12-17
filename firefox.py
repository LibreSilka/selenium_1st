import time
import requests
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


# def test_news(driver):
#     apps_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable(("xpath", "//*[@id='gbwa']/div/a"))
#     )
#     apps_button.click()
#
#     iframe = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located(("xpath", "//iframe[@role='presentation']"))
#     )
#     driver.switch_to.frame(iframe)
#     news_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable(("xpath", "//span[text()='Почта']"))
#     )
#     news_button.click()
#     time.sleep(3)
#     assert driver.current_url == "https://workspace.google.com/intl/ru/gmail/", "NO"
#
#
# def test_lucky_button(driver):
#     lucky_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("xpath", "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[2]")))
#     lucky_button.click()
#     assert driver.current_url == "https://doodles.google/"

# def test_pics(driver):
#     pict_but = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("xpath", "//a[text()='Картинки']")))
#     pict_but.click()
#     assert driver.current_url == "https://www.google.com/imghp?hl=ru&ogbl"

# def download_image(driver, image_index=0):
#     # Найти изображения на странице (например, первое изображение)
#     images = WebDriverWait(driver, 10).until(
#         EC.presence_of_all_elements_located(("xpath", "// img[ @ id = 'dimg_yg1gZ8fQL-a1wN4Pyt-d-Aw_19']"))
#     )
#     print(images)
#     if images is not None:
#         # Получить URL изображения
#         image_url = images.get_attribute("src")
#         print(f"Image URL: {image_url}")
#
#         # Скачать изображение
#         if image_url:
#             response = requests.get(image_url, stream=True)
#             if response.status_code == 200:
#                 # Создать папку для сохранения, если ее нет
#                 save_dir = "downloaded_images"
#                 if not os.path.exists(save_dir):
#                     os.makedirs(save_dir)
#
#                 # Имя файла для сохранения
#                 file_name = os.path.join(save_dir, f"image_{image_index}.jpg")
#                 with open(file_name, "wb") as file:
#                     for chunk in response.iter_content(1024):
#                         file.write(chunk)
#                 print(f"Image saved to {file_name}")
#             else:
#                 print(f"Failed to download image, status code: {response.status_code}")
#         else:
#             print("Image URL not found.")
#     else:
#         print("No images found.")
def test_search_func(driver):
    search_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("xpath", "//textarea[@class = 'gLFyf']")))
    search_field.send_keys("крокодил")
    time.sleep(2)
    search_but = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("xpath", "//input[@class = 'gNO89b']")))
    search_but.click()
    time.sleep(3)
    pics_but = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("xpath", "//div[text() = 'Картинки']")))
    pics_but.click()
