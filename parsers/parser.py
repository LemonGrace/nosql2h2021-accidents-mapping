from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import json

Cars = []
OneCar = dict(year='0', brand='0', model='0', size='0', modelType='0', overallDeathRate='0',
              multivehicleCrashDeathRate='0', singlevehicleCrashDeathRate='0')
BRANDS = ["MINI", "Fiat", "Mitsubishi", "Kia", "Hyundai", "Ford", "Honda", "Volkswagen", "Nissan", "Acura", "Mazda",
          "Chevrolet", "Toyota", "Subaru", "GMC", "Jeep", "Buick", "Land Rover", "Chrysler", "Mercedes-Benz",
          "Lexus", "Cadillac", "Infiniti", "BMW", "Lincoln", "Dodge", "Audi", "Volvo", "Ram", "Porsche"]


def getTableValue(year, size, modeltype, counter):
    # url of the page
    url = "https://www.iihs.org/ratings/driver-death-rates-by-make-and-model"
    driver = webdriver.Chrome(r'D:\study\chromedriver.exe')
    driver.get(url)
    time.sleep(3)
    # дописать поиск по году!!
    option_valueYear = year
    select_elementYear = driver.find_element(By.XPATH, "//select[option[@value = '%s']]" % option_valueYear)
    options = [x for x in select_elementYear.find_elements_by_tag_name("option")]
    # ищем переданный в функцию элемент
    for option in options:
        if option.get_attribute('value') == year:
            yearUsuall = option.get_attribute('innerText').strip()
            option.click()

            break
    time.sleep(5)

    # поиск конкретного элемента со страницы
    option_valueSize = size
    select_elementSize = driver.find_element(By.XPATH, "//select[option[@value = '%s']]" % option_valueSize)
    options = [x for x in select_elementSize.find_elements_by_tag_name("option")]
    # ищем переданный в функцию элемент
    for option in options:
        if option.get_attribute('value') == size:
            option.click()
            sizeUsuall = option.get_attribute('innerText').strip()
            break

    # обязательно нужно дать время прогрузить страницу, иначе выдаст ошибку
    time.sleep(5)

    option_valueModelType = modeltype
    select_elementModel = driver.find_element(By.XPATH, "//select[option[@value = '%s']]" % option_valueModelType)
    options2 = [x for x in select_elementModel.find_elements_by_tag_name("option")]
    for option in options2:
        if option.get_attribute('value') == modeltype:
            if not (option.is_enabled()):
                return counter
            option.click()
            modeltypeUsuall = option.get_attribute('innerText').strip()
            break

    time.sleep(3)

    html = driver.page_source
    html_dec = html.encode('utf-8').decode('ascii', 'ignore')
    soup = BeautifulSoup(html_dec, "html.parser")
    allVehicle = soup.find_all('td', {'data-label': "Vehicle"})
    allOverall = soup.find_all('td', {'data-label': "Overall death rate (with confidence limits)"})
    allMulti = soup.find_all('td', {'data-label': "Multi-vehicle crash death rate "})
    allSingle = soup.find_all('td', {'data-label': "Single-vehicle crash death rate"})

    counter2 = 0
    #сделать создание словарей
    for m in range(0, len(allVehicle)):
        OneCar['year'] = yearUsuall
        carBrand = allVehicle[m].text.strip()
        print(carBrand)
        flag = False
        for brand in BRANDS:
            if brand in carBrand:
                carBrand = carBrand.split(brand)
                OneCar['brand'] = brand
                OneCar['model'] = carBrand[1].strip()
                flag = True
                break
        if not flag:
            return counter
        OneCar['size'] = sizeUsuall
        OneCar['modelType'] = modeltypeUsuall
        OneCar['overallDeathRate'] = allOverall[m].text.strip()
        OneCar['multivehicleCrashDeathRate'] = allMulti[m].text.strip()
        OneCar['singlevehicleCrashDeathRate'] = allSingle[m].text.strip()
        path = "json/" + str(counter) + str(counter2) + ".json"
        print(path)
        with open(path, 'w') as fp:
            json.dump(OneCar, fp)
        counter2 += 1
        Cars.append(OneCar.copy())

    # Close webdriver
    driver.close()
    return counter


# будем передавать значение из массива размеров (пометить для себя, что где) и значение из массива стиля
# size = [mini, small, midsize, large, very large]
size = ["f9e250da-83db-427d-a82f-2d51bcb7c5dd", "3bec1f1e-1878-41a7-afa7-311fb51c7533",
        "a76114a4-69c9-4f57-90cb-4a435d71d7fc", "43d5cf6c-1c26-4699-8671-521d0a8a69fa",
        "0a36327c-14bd-4bcc-913c-c20d8160ceb9"]
modeltype = ["90871c83-810a-4548-a11a-63d0dc1c102f", "74ecc838-3806-4dd5-85ef-80bd0adde118",
             "f454c0ed-f814-48f0-9a47-e7854cca8fb0", "e648eed2-2b2e-482e-82ab-4fe620357a01",
             "8459da7c-566f-4dd6-8192-f404c41f8283", "8976d584-652e-4494-ae90-274b65f2fdf7",
             "a279e29b-f9da-47b9-bd45-be2059d85546", "fac5ce9b-9b4e-4910-9631-917b107ca5b8"]
years = ["414ad86c-4c36-4cee-8b2f-0ef0e6d02b96", "34d24024-a4ca-4c3b-898d-9dee3beabcb2",
         "6b9565ce-bea3-4577-a91b-2d8408dfc6e3", "71fb8742-0604-42a6-a0fe-0bb720d67cca",
         "d1ac2ced-0561-42e1-99a1-27e3c808ddfc", "4990c875-9391-4b11-97d0-ea4d207a498b"]

counter = 1
for i in range(0, len(years)):
    for j in range(0, len(size)):
        for k in range(0, len(modeltype)):
            counter = getTableValue(years[i], size[j], modeltype[k], counter)
            counter += 1

