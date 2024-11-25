import pytest
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

@pytest.fixture
def driver():
    # Инициализация браузера
    print("Запуск браузера")
    service = Service("C:\\Program Files (x86)\\Google\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)  # Не обязательно менять, но для тестов лучше увеличить до 10 секунд
    yield driver
    print("Закрытие браузера")
    driver.quit()
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = f"screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)
            pytest_html = item.config.pluginmanager.getplugin("html")
            extra = getattr(report, "extra", [])
            extra.append(pytest_html.extras.image(screenshot_path))
            report.extra = extra

# Тест с параметризацией
@pytest.mark.parametrize("email, password, expected_message", [
    ("hrobostov.nikita@yandex.ru", "&TDDExp1", None),  # TC1: Успешный вход
    ("hrobostov.nikita@yandex.ru", "wrong_password", "ОШИБКА: введено неверное имя пользователя или пароль."),  # TC2: Неверный пароль
    ("", "", "Заполните это поле.")  # TC3: Пустое поле

])

def test_login_form(driver, email, password, expected_message):
    # Переход на страницу авторизации
    driver.get("https://brainy.run/administrirovanie/my-profile/")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    driver.maximize_window()

    try:
        # Ввод email
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "log"))
        )
        email_field.clear()
        email_field.send_keys(email)
        print("Email введен")
    except TimeoutException:
        driver.save_screenshot("screenshots/error_email_field.png")
        raise AssertionError("Поле email не найдено")

    try:
        # Ввод пароля
        password_field = driver.find_element(By.NAME, "pwd")
        password_field.clear()
        password_field.send_keys(password)
        print("Пароль введен")
    except Exception as e:
        driver.save_screenshot("screenshots/error_password_field.png")
        raise AssertionError(f"Ошибка при вводе пароля: {e}")

    # Нажатие кнопки "Войти"
    login_button = driver.find_element(By.XPATH, "//button[normalize-space(text())='Войти']")
    login_button.click()

    # Проверка результатов
    if expected_message:
        if expected_message == "Заполните это поле.":
            validation_message = email_field.get_attribute("validationMessage")
            assert validation_message == expected_message, f"Ожидалось: '{expected_message}', но было: '{validation_message}'"
        else:
            error_message_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tutor-alert"))
            )
            assert expected_message in error_message_element.text, "Сообщение об ошибке неверное"
    else:
        WebDriverWait(driver, 10).until(
            EC.url_contains("https://brainy.run/administrirovanie/my-profile/")
        )

def test_forgot_button(driver):
    # Переход на страницу авторизации
    driver.get("https://brainy.run/administrirovanie/my-profile/")
    driver.maximize_window()
    forgot_password_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Забыли?"))
    )
    forgot_password_button.click()
    assert "https://brainy.run/administrirovanie/retrieve-password/" in driver.current_url, \
        "Неправильная ссылка на восстановление пароля"
