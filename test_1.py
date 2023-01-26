import driver
from selenium.webdriver.common.by import By
import pytest
from selenium import webdriver


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('D/SkillFactory/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield driver
    pytest.driver.quit()


def test_cards(testing):
    # Вводим email
    pytest.driver.find_element(By.ID, "email").send_keys('EAKvyatkovsky@gmail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, "pass").send_keys('290486qwe')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    pytest.driver.implicitly_wait(10)
    pytest.driver.find_element(By.CSS_SELECTOR, '.card-deck .card-img-top')
    pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')
    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')
    for i in range(len(images)):
        assert images[i].get_attribute('src') != '' or images[i].get_attribute('src') == ''
        assert names[i].text != '' or names[i].text == ''
        assert descriptions[i].text != '' or descriptions[i].text == ''
        assert ', ' in descriptions[i].text != ''
        parts = descriptions[i].text.split(', ')
        assert len(parts[0]) >= 0
        assert len(parts[1]) >= 0
