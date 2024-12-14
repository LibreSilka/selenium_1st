import pytest
import re

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    print(f"Тест идет: {item.name}")
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        print("Завал")
        driver = item.funcargs.get("driver")
        if driver:
            # Генерация безопасного имени файла
            safe_name = re.sub(r"[^\w\-.]", "_", item.name)
            screenshot_path = f"screenshots/{safe_name}.png"

            # Сохранение скриншота
            print(f"Сохранил {screenshot_path}")  # Debug
            if driver.save_screenshot(screenshot_path):
                print(f"Точно сохранил: {screenshot_path}")  # Debug

            # Добавление в HTML-отчет
            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html:
                extra = getattr(report, "extra", [])
                extra.append(pytest_html.extras.image(screenshot_path))
                report.extra = extra

# fef