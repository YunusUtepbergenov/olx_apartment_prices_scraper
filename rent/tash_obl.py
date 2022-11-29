import pandas as pd
import requests
from numpy import nan
from datetime import date, timedelta
from pandas import DataFrame
from bs4 import BeautifulSoup
from scrapy import Selector
from re import compile, sub, findall
from math import ceil
from selenium import webdriver

regions = ['akkurgan', 'almalyk', 'angren', 'ahangaran','bekabad', 'buka','gazalkent', 'gulbahor','durmen', 'dustabad','zangiota', 'keles','kibraj', 
            'koksaroy','krasnogórsk', 'nazarbek','tojtepa', 'parkent', 'pskent', 'xojakent','chorvoq', 'chinaz','chirchik', 'eshanguzar',
            'yangibazar', 'yangiyul', 'qorasuv', 'mirobod', 'salar', 'tashmore', 'turkiston', 'yangiobod', 'zafar', 'zangiota']

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Accept-Encoding': '*',
            'Connection': 'keep-alive'
        }

today = date.today()
yesterday = today - timedelta(days=1)
today = today.strftime('%d-%m-%Y')
yesterday = yesterday.strftime('%d-%m-%Y')

fx_rate_url = 'https://cbu.uz/oz/'
fx_rate_html = requests.get(fx_rate_url).content
fx_rate_selector = Selector(text=fx_rate_html)
fx_rate_xpath = '//div[@class="exchange__content"]//div[@class="exchange__item_value"]'
fx_rates = fx_rate_selector.xpath(fx_rate_xpath)
fx_rates = fx_rates.xpath('./text()').extract()
usd_to_uzs = float(fx_rates[0].replace(' = ', ''))

column_names = ['link', 'date', 'price', 'home_type', 'city',
                        'furnished', 'commission', 'num_rooms', 'area', 'apart_floor',
                        'home_floor', 'condition', 'build_type', 'build_plan',
                        'build_year', 'bathroom', 'ceil_height', 'hospital',
                        'playground', 'kindergarten', 'park', 'recreation', 'school',
                        'restaurant', 'supermarket', 'title_text', 'post_text']
month_dict = {
            ' г.': '', ' января ': '-01-', ' февраля ': '-02-', ' марта ': '-03-',
            ' апреля ': '-04-', ' мая ': '-05-', ' июня ': '-06-',
            ' июля ': '-07-', ' августа ': '-08-', ' сентября ': '-09-',
            ' октября ': '-10-', ' ноября ': '-11-', ' декабря ': '-12-',
            compile('^Сегодня.*'): today, compile('^Вчера.*'): yesterday
            }

options= webdriver.EdgeOptions()
options.add_argument("headless")
options.add_argument("disable-gpu")
driver = webdriver.Edge(executable_path=r"C:/SeleniumDrivers/Edge/msedgedriver.exe", options=options)

for ctr, region in enumerate(regions):
    olx_link = 'https://www.olx.uz/nedvizhimost/kvartiry/arenda-dolgosrochnaya/' + region + '/'
    # html_text = requests.get(olx_link).text
    driver.get(olx_link)
    html_text = driver.page_source

    soup = BeautifulSoup(html_text, 'lxml')
    if soup.find('div', attrs={'data-testid': 'total-count'}):
        total_count = soup.find('div', attrs={'data-testid': 'total-count'}).text
        s = ''.join(x for x in total_count if x.isdigit())
    else:
        continue
    if int(s) > 0 :
        num_pages = ceil(int(s) / 39)
        num_pages = min(num_pages, 25)
        print("Calculating " + region + " and Total " + str(num_pages) + " pages")

        dataframe = DataFrame(columns=column_names)
        row = 1

        for page in range(num_pages):
            print("Scraping page: " + str(page + 1))
            page_link = olx_link + '?page=' + str(page+1)
            driver.get(page_link)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            all_table = soup.find('div', class_="css-pband8")

            if all_table:
                apartments = all_table.find_all('div', attrs={'data-cy': 'l-card'})
                for apartment in apartments:
                    link = apartment.find("a", class_="css-rc5s2u")
                    #Pasted code
                    driver.get("https://www.olx.uz" + link['href'])
                    html = driver.page_source
                    soup1 = BeautifulSoup(html, 'lxml')
                    html_selector = Selector(text=html)

                    dataframe.at[row, 'link'] = link['href']

                    try:
                        district_list = html_selector.xpath('//*[@id="root"]//a/text()').extract()
                        district_pattern = compile(r'Аренда долгосрочная - (.*)')
                        district = list(filter(district_pattern.match, district_list))[1]
                        district = sub(district_pattern, r'\1', district)
                        dataframe.at[row, 'city'] = district
                    except:
                        pass


                    try:
                        date_xpath = '//*[@id="root"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[1]/span/span'
                        announcement_date = soup1.find('span', class_='css-19yf5ek').text
                        dataframe.at[row, 'date'] = announcement_date
                    except:
                        pass

                    try:
                        price_list = html_selector.xpath('//*[@id="root"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[3]/h3')
                        price_list = soup1.find('h3', class_="eu5v0x0").text
                        num = ""
                        for c in price_list:
                            if c.isdigit():
                                num = num + c
                        price = float(num)

                        if price_list.count("сум"):
                            price = price / usd_to_uzs
                        elif not price_list.count('у.е.'):
                            price = nan
                        dataframe.at[row, 'price'] = price
                    except:
                        pass

                    # Other details
                    try:
                        other_details = soup1.find_all('p', class_="css-xl6fe0-Text eu5v0x0")

                    except:
                        other_details = ''

                    try:
                        home_type_pattern = compile(r'Тип жилья: (.*)')
                        for other in other_details:
                            if 'Тип жилья' in other.text:
                                home_type = other.text.replace('Тип жилья:', '')
                        home_type = sub(home_type_pattern, r'\1', home_type)
                        dataframe.at[row, 'home_type'] = home_type
                    except:
                        pass
                    try:
                        rooms_pattern = compile(r'Количество комнат: (\d+).*')
                        for other in other_details:
                            if 'Количество комнат:' in other.text:
                                rooms = other.text.replace('Количество комнат:', '')
                        rooms = sub(rooms_pattern, r'\1', rooms)
                        rooms = int(rooms)
                        dataframe.at[row, 'num_rooms'] = rooms
                    except:
                        pass

                    try:
                        area_pattern = compile(r'Общая площадь: (\d+).*')
                        for other in other_details:
                            if 'Общая площадь:' in other.text:
                                area = other.text.replace('Общая площадь: ', '')
                                num = ""
                                for c in area:
                                    if c.isdigit():
                                        num = num + c
                                    else:
                                        break
                                area = int(num)
                        dataframe.at[row, 'area'] = area
                    except:
                        pass

                    try:
                        dataframe.at[row, 'price_m2'] = dataframe.at[row, 'price'] / dataframe.at[row, 'area']
                    except:
                        pass

                    try:
                        floor_pattern = compile(r'Этаж: (\d+).*')
                        for other in other_details:
                            if 'Этаж:' in other.text:
                                floor = other.text.replace('Этаж:', '')
                        floor = sub(floor_pattern, r'\1', floor)
                        floor = int(floor)
                        dataframe.at[row, 'apart_floor'] = floor
                    except:
                        pass

                    try:
                        home_floor_pattern = compile(r'Этажность дома: (\d+).*')
                        for other in other_details:
                            if 'Этажность дома:' in other.text:
                                home_floor = other.text.replace('Этажность дома: ', '')
                        dataframe.at[row, 'home_floor'] = home_floor
                    except:
                        pass

                    try:
                        building_type_pattern = compile(r'Тип строения: (.*)')
                        for other in other_details:
                            if 'Тип строения:' in other.text:
                                building_type = other.text.replace('Тип строения:', '')
                        building_type = sub(building_type_pattern, r'\1', building_type)
                        dataframe.at[row, 'build_type'] = building_type
                    except:
                        pass

                    try:
                        plan_pattern = compile(r'Планировка: (.*)')
                        for other in other_details:
                            if 'Планировка:' in other.text:
                                plan = other.text.replace('Планировка:', '')
                        plan = sub(plan_pattern, r'\1', plan)
                        dataframe.at[row, 'build_plan'] = plan
                    except:
                        pass

                    try:
                        year_pattern = compile(r'Год постройки/сдачи.*(\d{4})')
                        for other in other_details:
                            if 'Год постройки/сдачи:' in other.text:
                                year = other.text.replace('Год постройки/сдачи: ', '')
                        dataframe.at[row, 'build_year'] = year
                    except:
                        pass

                    try:
                        bath_type_pattern = compile(r'Санузел: (.*)')
                        for other in other_details:
                            if 'Санузел:' in other.text:
                                bath_type = other.text.replace('Санузел:', '')
                        bath_type = sub(bath_type_pattern, r'\1', bath_type)
                        dataframe.at[row, 'bathroom'] = bath_type
                    except:
                        pass

                    try:
                        furnished_pattern = compile(r'Меблирована: (.*)')
                        for other in other_details:
                            if 'Меблирована:' in other.text:
                                furnished = other.text.replace('Меблирована: ', '')
                        # furnished = sub(furnished_pattern, r'\1', furnished)
                        dataframe.at[row, 'furnished'] = {'Да': True, 'Нет': False}.get(furnished)
                    except:
                        pass

                    try:
                        height_pattern = compile(r'Высота потолков: (.*)')
                        for other in other_details:
                            if 'Высота потолков:' in other.text:
                                height = other.text.replace('Высота потолков: ', '')
                        # height = sub(height_pattern, r'\1', height)
                        height = float(height)
                        if height > 150:
                            height /= 100
                        elif height >= 20:
                            height /= 10

                        dataframe.at[row, 'ceil_height'] = height
                    except:
                        pass

                    try:
                        condition_pattern = compile(r'Ремонт: (.*)')
                        for other in other_details:
                            if 'Ремонт:' in other.text:
                                condition = other.text.replace('Ремонт: ', '')
                        dataframe.at[row, 'condition'] = condition
                    except:
                        pass

                    try:
                        commission_pattern = compile(r'Комиссионные: (.*)')
                        for other in other_details:
                            if 'Комиссионные:' in other.text:
                                commission = other.text.replace('Комиссионные: ', '')
                        # commission = sub(commission_pattern, r'\1', commission)
                        dataframe.at[row, 'commission'] = {'Да': True, 'Нет': False}.get(commission)
                    except:
                        pass

                    # Title and text parts
                    try:
                        title = soup1.find('h1', class_="eu5v0x0").text
                        print(title)
                        dataframe.at[row, 'title_text'] = title
                    except:
                        pass

                    try:
                        content = soup1.find('div', class_="css-g5mtbi-Text").text
                        dataframe.at[row, 'post_text'] = content
                    except:
                        pass

                    # Extra Details
                    try:
                        close_things_pattern = compile(r'Рядом есть:')
                        close_things = list(filter(close_things_pattern.match, other_details))[0]
                    except:
                        close_things = ''

                    if 'Больница' in close_things:
                        dataframe.at[row, 'hospital'] = True
                    else:
                        dataframe.at[row, 'hospital'] = False

                    if 'Детская площадка' in close_things:
                        dataframe.at[row, 'playground'] = True
                    else:
                        dataframe.at[row, 'playground'] = False

                    if 'Детский сад' in close_things:
                        dataframe.at[row, 'kindergarten'] = True
                    else:
                        dataframe.at[row, 'kindergarten'] = False

                    if 'Парк' in close_things:
                        dataframe.at[row, 'park'] = True
                    else:
                        dataframe.at[row, 'park'] = False

                    if 'Развлекательные заведения' in close_things:
                        dataframe.at[row, 'recreation'] = True
                    else:
                        dataframe.at[row, 'recreation'] = False

                    if 'Рестораны' in close_things:
                        dataframe.at[row, 'restaurant'] = True
                    else:
                        dataframe.at[row, 'restaurant'] = False

                    if 'Школа' in close_things:
                        dataframe.at[row, 'school'] = True
                    else:
                        dataframe.at[row, 'school'] = False

                    if 'Супермаркет' in close_things:
                        dataframe.at[row, 'supermarket'] = True
                    else:
                        dataframe.at[row, 'supermarket'] = False

                    dataframe.loc[:, 'date'] = dataframe.loc[:, 'date'].replace(month_dict, regex=True)
                    dataframe.dropna(how='all', inplace=True,
                            subset=['price', 'num_rooms', 'area', 'apart_floor'])
                    row = row + 1
        dataframe.to_excel(region + ".xlsx")
        print(region + ".xls file is ready")
