import os
import requests
from time import sleep
from bs4 import BeautifulSoup

URL = "https://www.autoevolution.com/cars/"  # main page
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
    'Accept': '*/*'}

def loadImg(src, path, name):
    p = requests.get(src)
    sleep(5)
    out = open(path + '/' + name + ".jpg", "wb")
    out.write(p.content)
    out.close()

def get_generations(html, brand_name, model_name):
    soup = BeautifulSoup(html, 'html.parser')
    generations = soup.find_all('div', class_='container carmodel clearfix')

    folder = "generations/" + brand_name + "/" + model_name

    for gen in generations:
        path = gen.find('div', class_='col1width fl')
        if path:
            gen_name = path.find_next('h2', itemprop='name').find_next('span', class_='col-red').get_text()
            if gen_name:
                gen_name = gen_name.replace("/", "_")
                gen_name = brand_name + " " + gen_name
                gen_name = gen_name.replace(" ", "_")

            path = path.find_next('a', class_='mpic fr')
            if path:
                img = path.find('img', itemprop="image").get('src')
                loadImg(img, folder, gen_name)


def get_models(html, brand_name): # по макету изображения на данном уровне не требуются
    soup = BeautifulSoup(html, 'html.parser')
    models = soup.find('div', class_='carmodels col23width clearfix').find_all(class_='carmod clearfix')

    for model in models:
        path = model.find('div', class_='col2width bcol-white fl')
        if path:
            model_name = path.find_next('h4').get_text().replace("  ", " ").replace(" ", "_")
            os.makedirs("generations/" + brand_name + "/" + model_name, exist_ok=True)

            link = path.find_next('a').get('href')
            print(link)
            if link:
                answ = call_get_html(link)
                if not answ[0]:
                    print("Error!")
                else:  # проход по всем моделям
                    get_generations(answ[1], brand_name, model_name)

def get_image_brand(html):
    soup = BeautifulSoup(html, 'html.parser')
    brands = soup.find_all(class_='col2width fl bcol-white carman')

    for brand in brands:
        name = brand.find('h5').get_text(strip=True)
        os.makedirs("generations/" + name, exist_ok=True)

        link = brand.find().get('href')
        if link:
            answ = call_get_html(link)
            if not answ[0]:
                print("Error!")
            else:
                get_models(answ[1], name)

        brand = brand.find('img', class_='jhref').get('src')
        loadImg(brand, 'brands', name)

def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    sleep(5)
    return response

def call_get_html(url):
    html = get_html(url)
    if html.status_code == 200:
        return [True, html.text]
    else:
        return [False]

answ = call_get_html(URL)
if answ[0]:
    cars = get_image_brand(answ[1])
else:
    print("Error!")

