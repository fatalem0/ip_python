import requests
from bs4 import BeautifulSoup as bs
from lists import cities, republics, okrugs
from datetime import date

date_list = []
region_list = []
type_list = []
situation_list = []
victims_list = []
injured_list = []
current_date = date.today().strftime("%d/%m/%Y")

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

def page_date(html):
    soup = bs(html, 'html.parser')
    try:
        date = soup.find('div', class_ = 'b-article-header__date').text
    except Exception:
        date = ''
    # date_list.append(str(date))
    if date.find('Сегодня') != -1:
        # date_list.append(str(date.rsplit(' ', 1)[-1]))
        date = current_date
        date_list.append(date)
    else:
        # date_list.append(str(date.split(' ', 2)[-1]))
        date = str(date.split(' ', 2)[-1])
        d, m, y = date.split(' ')

        if m.find('Янв') != -1:
            m = '01'
        elif m.find('Фев') != -1:
            m = '02'
        elif m.find('Мар') != -1:
            m = '03'
        elif m.find('Апр') != -1:
            m = '04'
        elif m.find('Ма') != -1:
            m = '05'
        elif m.find('Июн') != -1:
            m = '06'
        elif m.find('Июл') != -1:
            m = '07'
        elif m.find('Авг') != -1:
            m = '08'
        elif m.find('Сен') != -1:
            m = '09'
        elif m.find('Окт') != -1:
            m = '10'
        elif m.find('Ноя') != -1:
            m = '11'
        else:
            m = '12'

        date = d + "/" + m + "/" + y
        date_list.append(date)

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
    region_list.append(str(region))

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
    type_list.append(str(type))
    situation_list.append(str(situation))
    victims_list.append(str(victims))
    injured_list.append(str(injured))

    # data = {'date': date,
    #         'region': region,
    #         'type': type,
    #         'situation': situation,
    #         'victims': victims,
    #         'injured': injured}
    # return data

# ДЛЯ СЛОВАРЯ

# count = 1
# while count <= 5:
#     url = 'http://www.mchsmedia.ru/news/' + str(count) + '/?category=incidents'
#     all_links = get_links(get_html(url))
#     for link in all_links:
#         html = get_html(link)
#         data = page_date(html)
#         print(type(data['date']))
#     count += 1

# ДЛЯ СПИСКОВ

count = 1
while count <= 5:
    url = 'http://www.mchsmedia.ru/news/' + str(count) + '/?category=incidents'
    all_links = get_links(get_html(url))
    for link in all_links:
        html = get_html(link)
        page_date(html)
    count += 1

# for i in date_list:
#     print(i)