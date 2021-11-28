import requests
from bs4 import BeautifulSoup
from time import sleep
import json

URL = "https://www.autoevolution.com/cars/"  # main page

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
    'Accept': '*/*'}


def get_html(url, params=None):
    sleep(2)
    response = requests.get(url, headers=HEADERS, params=params)
    sleep(3)
    return response


def saveJSON(brand, file_name):
    with open('brands/' + file_name + '.json', 'w') as file:
        json.dump(brand, file, indent=3)


def delete_excess(word, sep1, sep2):
    flag1 = False
    flag2 = False
    count1 = 1
    count2 = 0

    for i in word:
        if i == sep1:
            flag1 = True
        elif i == sep2:
            flag2 = True

        if not flag1:
            count1 = count1 + 1
        if not flag2:
            count2 = count2 + 1
    return word[count1:count2 - 1]


def delete_excess2(word, sep1, flag):
    flag1 = False
    count1 = 0

    for i in word:
        if i == sep1:
            flag1 = True
        if not flag1:
            count1 = count1 + 1
    if flag:
        return word[:count1 - 1]
    else:
        return word[:count1]


def repeat(param, info, name, sep1, sep2):
    if param:
        param = param.find_next('dd').get_text()
        if param:
            info.append((name, delete_excess(param, sep1, sep2)))
    return info


def repeat2(param, info, name):
    if param:
        param = param.find_next('dd').get_text()
        if param:
            info.append((name, param[:len(param) - 1]))
    return info


# get info about generations
def get_content_lvl3(html):
    soup = BeautifulSoup(html, 'html.parser')
    path = soup.find('div', class_='container2 clearfix')
    if path:
        path = path.find_next('div', id='newscol2')
        if path:
            path = path.find_next('h1', class_='padcol2 newstitle innews')
            info = []

            name = path.find_next('b', itemprop="brand")
            name_brand = name.get_text() + " "
            name_gen = name.next_sibling.get_text()
            name_brand_gen = (name_brand + name_gen).replace("   ", "  ").replace("  ", " ")
            info.append(('fullName', name_brand_gen[:len(name_brand_gen) - 1]))

            data = path.find_next('em', class_='nowrap col-black faded').get_text()
            info.append(('firstYearProduction', data[0:4]))

            if len(data) >= 7:
                if data[7] == 'P':
                    info.append(('lastYearProduction', 'Present'))
                else:
                    info.append(('lastYearProduction', data[7:12]))

    path_second = soup.find('div', class_='container cartech top2line1')
    if path_second:
        path_second = path_second.find_next('div', class_='enginedata engine-inline')
        if path_second:
            path_second = path_second.find_next('div', class_='techdata')
            if path_second:
                performance_specs = path_second.find_next('dl', title='Performance Specs')
                if performance_specs:
                    topSpeed = performance_specs.find_next('dt', text='Top Speed')
                    repeat(topSpeed, info, 'topSpeed', '(', 'k')

                    acceleration = performance_specs.find_next('dt', text='Acceleration 0-62 Mph (0-100 kph)')
                    if acceleration:
                        acceleration = acceleration.find_next('dd').get_text()
                        if acceleration:
                            info.append(('acceleration', acceleration.replace(' s', '')))

                transmission_specs = path_second.find_next('dl', title='Transmission Specs')
                if transmission_specs:
                    driveType = transmission_specs.find_next('dt', text='Drive Type')
                    repeat2(driveType, info, 'drive type')

                    gearBox = transmission_specs.find_next('dt', text='Gearbox')
                    repeat2(gearBox, info, 'gearBox')

                dimensions = path_second.find_next('dl', title='Dimensions Specs')
                if dimensions:
                    length = dimensions.find_next('dt', text='Length')
                    repeat(length, info, 'length', '(', 'm')

                    width = dimensions.find_next('dt', text='Width')
                    repeat(width, info, 'width', '(', 'm')

                    height = dimensions.find_next('dt', text='Height')
                    repeat(height, info, 'height', '(', 'm')

                    wheelBase = dimensions.find_next('dt', text='Wheelbase')
                    repeat(wheelBase, info, 'wheelBase', '(', 'm')

                    wheelTrack = dimensions.find_next('dt', text='Front/rear Track')
                    if wheelTrack:
                        wheelTrack = wheelTrack.find_next('dd').get_text()
                        if wheelTrack:
                            wheelTrack = delete_excess(wheelTrack, '(', 'm')
                            info.append(('wheelTrack', delete_excess2(wheelTrack, '/', False).replace(',', '.')))

                    cargoVolume = dimensions.find_next('dt', text='Cargo Volume')
                    repeat(cargoVolume, info, 'cargoVolume', '(', 'L')

                    aerodynamics = dimensions.find_next('dt', text='Aerodynamics (frontal area)')
                    if aerodynamics:
                        aerodynamics = aerodynamics.find_next('dd').get_text()
                        if aerodynamics:
                            info.append(('aerodynamics', delete_excess2(aerodynamics, 'm', True)))

                fuel = path_second.find_next('dl', title='General Specs')
                if fuel:
                    fuel = fuel.find_next('dt', text='Fuel')
                    if fuel:
                        fuel = fuel.next_sibling.get_text()
                        if fuel:
                            info.append(('fuel', fuel[:len(fuel) - 1]))
    return dict(info)


def remove_start_space(text):
    if text.startswith(" "):
        return text[1:]
    else:
        return text


def get_content_lvl2(html):
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find('div', class_='container2 clearfix')
    info = []
    info_one = item.find('div', id='newscol2').find_next('h1', class_='padsides_20i newstitle innews')
    info_two = item.find('div', id='newscol2').find_next('div', class_='padsides_20i newstext mgbot_20 fsz14')

    if info_one:
        model_name = info_one.find_next('a').get('title').replace("  ", " ")
        info.append(("modelName", model_name))

    if info_two:
        temp_2 = info_two.find_next('strong', text='First production year:')
        if temp_2:
            first_year_prod = temp_2.next_sibling
            if first_year_prod:
                info.append(('firstYearProduction', first_year_prod.get_text(strip=True)))

        temp = info_two.find_next('strong', text='Engines:')
        if temp:
            engine_type = temp.next_sibling
            if engine_type:
                info.append(('engineType', engine_type.get_text(strip=True)))

        style = info_two.find_next('strong', text='Body style:')
        if style:
            style = style.next_sibling
            if style:
                style = style.get_text()
                style = remove_start_space(style)
                info.append(('style', style))

    items = soup.find_all('div', class_='container carmodel clearfix')
    generations = []
    for item_ in items:
        path = item_.find('div', class_='col1width fl').find_next('a').get('href')
        res = call_get_html(path)
        if not res[0]:
            print("Error!")
        else:  # проход по всем поколениям
            generations.append(get_content_lvl3(res[1]))
    if generations:
        info.append(('generations', generations))
    return dict(info)


def get_content_lvl1(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(class_='carmod clearfix')
    models = []

    for item in items:
        path = item.find('div', class_='col2width bcol-white fl').find_next('a').get('href')
        res = call_get_html(path)
        if not res[0]:
            print("Error!")
        else:  # проход по всем моделям
            models.append(get_content_lvl2(res[1]))
    return models


def get_content_lvl0(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(class_='col2width fl bcol-white carman')
    cars = []

    for item in items:
        item_ = item.find().get('href')
        if item_:
            res = call_get_html(item_)
            if not res[0]:
                print("Error!")
            else:  # проход по всем брендам
                name = item.find('h5').get_text(strip=True)

                cars.append({'brand': name,
                             'models': get_content_lvl1(res[1])
                             })
                saveJSON(cars[len(cars) - 1], name)


def call_get_html(url):
    sleep(3)
    html = get_html(url)
    sleep(2)
    if html.status_code == 200:
        return [True, html.text]
    else:
        return [False]


answ = call_get_html(URL)
cars = []
if answ[0]:
    get_content_lvl0(answ[1])
else:
    print("Error!")
