import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    # Инициализация браузера
    service = Service("C:\\Program Files (x86)\\Google\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(1)  # Не обязательно менять, но для тестов лучше увеличить до 10 секунд
    yield driver
    driver.quit()

# Тест с параметризацией
@pytest.mark.parametrize("email, password, expected_message", [
    ("hrobostov.nikita@yandex.ru", "&TDDExp1", None),  # TC1: Успешный вход
    ("hrobostov.nikita@yandex.ru", "wrong_password", "ОШИБКА: введено неверное имя пользователя или пароль."),  # TC2: Неверный пароль
    ("", "", "Заполните это поле.")  # TC2: Неверный пароль

])
def test_login_form(driver, email, password, expected_message):
    # Переход на страницу авторизации
    driver.get("https://brainy.run/administrirovanie/my-profile/")
    driver.maximize_window()
    driver.minimize_window()

    # Ввод email
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "log"))
    )
    email_field.clear()
    email_field.send_keys(email)

    # Ввод пароля
    password_field = driver.find_element(By.NAME, "pwd")
    password_field.clear()
    password_field.send_keys(password)

    # Нажатие кнопки "Войти"
    login_button = driver.find_element(By.XPATH, "//button[normalize-space(text())='Войти']")
    login_button.click()

    # Проверка результатов
    # Проверка результатов
    if expected_message == "Заполните это поле.":
        # Проверяем, что браузер показывает встроенное предупреждение
        if not email:
            validation_message = email_field.get_attribute("validationMessage")
            assert validation_message == expected_message, f"Ожидалось: '{expected_message}', но было: '{validation_message}'"

    elif expected_message:
        # Проверка сообщения об ошибке
        error_message_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tutor-alert"))
        )
        actual_message = error_message_element.text
        assert expected_message in actual_message, f"Ожидалось сообщение: '{expected_message}', но было: '{actual_message}'"
    else:
        # Проверка успешного входа (TC1)
        WebDriverWait(driver, 10).until(
            EC.url_contains("https://brainy.run/administrirovanie/my-profile/")
        )
        # Нажатие на вкладку "Курсы на которые я зачислен"
        enrolled_courses_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Курсы, на которые вы зачислены"))
        )
        enrolled_courses_button.click()

        # Проверка URL-адреса вкладки
        WebDriverWait(driver, 10).until(
            EC.url_contains("https://brainy.run/administrirovanie/enrolled-courses/")
        )
        assert "https://brainy.run/administrirovanie/enrolled-courses/" in driver.current_url, \
            "Не удалось открыть вкладку 'Курсы, на которые вы зачислены'"
        # assert "Администрирование - Школа Брейни" in driver.title, "Заголовок страницы не соответствует ожидаемому"

#Проверка гит
#Next commit