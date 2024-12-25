import time
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os

# Создание папки для скриншотов, если она не существует
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")


@allure.feature("Google News")
@allure.story("Поиск новостей")
@allure.title("Новости")
@allure.description("Тест выполняет переход по ссылке новости'.")
def test_news(driver):
    with allure.step("Нажатие iframe"):
        apps_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", "//*[@id='gbwa']/div/a"))
        )
        apps_button.click()
    with allure.step("Нажатие кнопки news в iframe"):
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(("xpath", "//iframe[@role='presentation']"))
        )
        driver.switch_to.frame(iframe)
        news_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", "//span[text()='Новости']"))
        )
        news_button.click()
        time.sleep(3)

    # Проверка URL после перехода
    assert driver.current_url == "https://news.google.com/home?hl=ru&gl=RU&ceid=RU:ru", "Не загрузил страницу новости"


@allure.feature("Google Lucky")
@allure.story("Нажатие на Lucky Button")
@allure.title("Lucky_Button")
@allure.description("Тест выполняет переход по ссылке Lucky_Button'.")
def test_lucky_button(driver):
    lucky_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("xpath", "/html/body/div[1]/div["
                                                                                        "3]/form/div[1]/div[1]/div["
                                                                                        "3]/center/input[2]")))
    lucky_button.click()
    # Проверка URL после перехода
    assert driver.current_url == "https://doodles.google/", "Не загрузил страницу - тебе повезет"


@allure.feature("Google Картинки")
@allure.story("Картинки")
@allure.title("Картинки")
@allure.description("Тест выполняет переход по ссылке Картинки'.")
def test_pics(driver):
    pict_but = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("xpath", "//a[text()='Картинки']")))
    pict_but.click()
    # Проверка URL после перехода
    assert driver.current_url == "https://www.google.com/imghp?hl=ru&ogbl", "Не перешел на страницу картинок"


@allure.feature("Google Search")
@allure.story("Поиск информации о 'крокодил'")
@allure.title("Поиск изображений")
@allure.description("Тест выполняет поиск слова 'крокодил' и открывает раздел 'Картинки'.")
def test_search_func(driver):
    with allure.step("Открытие поискового поля"):
        search_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", "//textarea[@class = 'gLFyf']")))
        search_field.send_keys("крокодил")
        time.sleep(2)
    with allure.step("Нажатие на кнопку поиска"):
        search_but = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(("xpath", "//input[@class = 'gNO89b']")))
        search_but.click()
        time.sleep(3)
    with allure.step("Переход в раздел 'Картинки'"):
        pics_but = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("xpath", "//div[text() = 'Картинки']")))
        pics_but.click()
    with allure.step("Сделать скриншот"):
        screenshot_path = f"screenshots/test_search_func.png"
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name="Скриншот результата", attachment_type=allure.attachment_type.PNG)


@allure.feature("Pics download")
@allure.story("Скачивание изображения")
@allure.title("Скачивание Изоб")
@allure.description("Тест выполняет скачивание первой картинки в поиске'.")
def test_scroll_image(driver):
    with allure.step("Сделать поиск крокодила"):
        search_box = driver.find_element("name", 'q')
        search_box.send_keys('crocodile')
        search_box.send_keys(Keys.RETURN)  # Press Enter to perform the search
        time.sleep(5)
    with allure.step("Переход в раздел 'Картинки'"):
        pics_but = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("xpath", "//div[text() = 'Картинки']")))
        pics_but.click()
    with allure.step("Scroll"):
        for _ in range(3):  # Количество прокруток
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # Скроллим вниз
            time.sleep(2)
