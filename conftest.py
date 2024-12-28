import pytest
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service
@pytest.fixture
def driver():
    service = Service(EdgeChromiumDriverManager().install())
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    driver = webdriver.Edge(service=service, options=options)
    driver.implicitly_wait(10)
    driver.get('https://google.com')
    yield driver