import requests
from bs4 import BeautifulSoup as bs
from lists import cities, republics, okrugs

def get_html(url):
    r = requests.get(url)
    return r.text

def get_links(html):
    soup = bs(html, 'html.parser')
    ads = soup.find('div', class_ = 'cl-holder').find_all('div', class_ = 'cl-item clearfix')
    links = []
    for index, i in enumerate(ads):
        link = 'http://www.mchsmedia.ru/' + i.find('a').get('href')
        links.append(link)
    return links

def page_date(url):
    soup = bs(html, 'html.parser')

    try:
        date = soup.find('div', class_ = 'b-article-header__date').text
    except Exception:
        date = ''

    try:
        tags = soup.find('div', class_ = 'b-tags').find_all('a')
    except Exception:
        tags = ''

    region = 'Нет информации о регионе'
    for string in tags:
        for substring in string:
            for i in range(len(cities)):
                if cities[i].find(substring) != -1:
                    region = cities[i]
            for i in range(len(republics)):
                if republics[i].find(substring) != -1:
                    region = republics[i]
            for i in range(len(okrugs)):
                if okrugs[i].find(substring) != -1:
                    region = okrugs[i]
            if region == 'Нет информации о регионе':
                if substring.find('область') != -1 or substring.find('республика') != -1 \
                or substring.find('край') != -1 or substring.find('город') != -1\
                or substring.find('округ') != -1 or substring.find('Республика') != -1 \
                or substring.find('Округ') != -1 or substring.find('Море') != -1 \
                or substring.find('море') != -1 or substring.find('Город') != -1:
                    region = substring


    # тк теги на сайте МЧС порой написаны неточно, то всё, что не имеет достаточно точной
    # категоризации, будет относиться к категории 'Прочее'
    type = 'Прочее'
    situation = 'Прочее'
    victims = 'Нет погибших'
    injured = 'Нет пострадавших'
    for string in tags:
        for substring in string:
            if substring.find('пожар') != -1 or substring.find('Пожар') != -1:
                type = 'Пожар'
                situation = 'Техногенный'
            elif substring.find('подтоп') != -1 or substring.find('Подтоп') != -1:
                type = 'Подтопление'
                situation = 'Экологический'
            elif substring.find('обрушен') != -1 or substring.find('Обрушен') != -1:
                type = 'Обрушение'
                situation = 'Техногенный'
            elif substring.find('непогод') != -1 or substring.find('Непогод') != -1:
                type = 'Непогода'
                situation = 'Экологический'
            elif substring.find('утон') != -1 or substring.find('утоп') != -1:
                type = 'Утопление'
                situation = 'Социальный'
            elif substring.find('ДТП') != -1:
                type = 'ДТП'
                situation = 'Транспортный'
            elif substring.find('помощь') != -1 or substring.find('спасен') != -1 \
            or substring.find('Спасен') != -1 or substring.find('поиск') != - 1 \
            or substring.find('Поиск') != - 1:
                type = 'Спасение'
                situation = 'Социальный'
            elif substring.find('крушен') != -1 or substring.find('паден') != -1 \
            or substring.find('Крушен') != -1 or substring.find('Паден') != -1:
                type = 'Крушение'
                situation = 'Техногенный'
            elif substring.find('выпал') != -1:
                type = 'Падение'
                situation = 'Социальный'
                injured = 'Есть пострадавшие'
            elif substring.find('землетрясени') != -1 or substring.find('Землетрясени') != -1 \
            or substring.find('толч') != -1 or substring.find('Толч') != -1 \
            or substring.find('сейсмо') != -1 or substring.find('Сейсмо') != -1:
                type = 'Землетрясение'
                situation = 'Экологический'
            elif substring.find('авари') != -1 or substring.find('Авари') != -1:
                type = 'Авария'
                situation = 'Техногенный'
            elif substring.find('поджигател') != -1 or substring.find('Поджигател') != -1:
                type = 'Поджог'
                situation = 'Социальный'
            elif substring.find('погиб') != -1 or substring.find('Погиб') != -1 \
            or substring.find('умер') != -1 or substring.find('Умер') != -1:
                victims = 'Есть погибшие'
            elif substring.find('пострадав') != -1 or substring.find('Пострадав') != -1:
                injured = 'Есть пострадавшие'
    data = {'date': date,
            'region': region,
            'type': type,
            'situation': situation,
            'victims': victims,
            'injured': injured}
    return print(data)


count = 1
while count <= 5:
    url = 'http://www.mchsmedia.ru/news/' + str(count) + '/?category=incidents'
    all_links = get_links(get_html(url))
    for link in all_links:
        html = get_html(link)
        data = page_date(html)
    count += 1
