import driver
from selenium.webdriver.common.by import By
import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('D/SkillFactory/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield driver
    pytest.driver.quit()


def test_pets(testing):
    # Вводим email
    pytest.driver.find_element(By.ID, "email").send_keys('EAKvyatkovsky@gmail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, "pass").send_keys('290486qwe')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    pytest.driver.find_element(By.CSS_SELECTOR, 'div#navbarNav > ul > li > a').click()
    assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "Evgeny Kvyatkovsky"

    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > th > img')))
    images = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > th > img')
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')))
    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    breed = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    age = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

    # проверяем что бы кол-во карточек с фото было >= 50%
    count = 0
    count1 = 0
    for i in images:
        if i.get_attribute('src') != '':
            count += 1
        if i.get_attribute('src') == '':
            count1 += 1
        print(count, count1)
        assert count >= round((count1 + count)/100*50)
    # проверяем наличие имен и отсутствие одинаковых
    pet_names = []
    for n in names:
        pet_names.append(n.text)
        assert n.text != ''
        assert len(set(pet_names)) == len(pet_names)
    print(pet_names)
    # проверяем наличие породы
    for b in breed:
        assert b.text != ''
    # проверяем наличие возраста
    for a in age:
        assert a.text != ''
    # и наконец проверяем питомцев на уникальность
    all_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    all_pets1 = []
    for pet in all_pets:
        all_pets1.append(pet.text)
    assert len(set(all_pets1)) == len(all_pets1)
    print(all_pets1)
