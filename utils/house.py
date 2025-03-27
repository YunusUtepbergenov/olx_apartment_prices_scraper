from bs4 import BeautifulSoup
from re import compile, sub
from numpy import nan

def house_scrape(apartment, dataframe, row, driver, usd_to_uzs, month_dict, getCity, district_dict, type_of_district, district):
    link = apartment.find("a", class_="css-1tqlkj0")
    driver.get("https://www.olx.uz" + link['href'])
    html = driver.page_source
    soup1 = BeautifulSoup(html, 'lxml')

    dataframe.at[row, 'link'] = link['href']

    try:
        location = soup1.find('section', class_="css-wefbef")
        dataframe.at[row, 'city'] = location.find('p', class_="css-z0m36u").text
        dataframe.at[row, 'district'] = getCity(district_dict, soup1, type_of_district, district)
    except:
        pass

    try:
        announcement_date = soup1.find('span', class_='css-pz2ytp').text
        dataframe.at[row, 'date'] = announcement_date
    except:
        pass

    # Other details
    try:
        other_details_list = soup1.find('div', class_="css-41yf00")
        other_details = other_details_list.find_all('p', class_="css-z0m36u")

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
        if soup1.find('div', class_="css-e2ir3r").text:
            price_list = soup1.find('div', class_="css-e2ir3r").text
        else:
            price_list = soup1.find('meta', attrs={'name' : "description"} )['content'].split(':')[0]

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
        for other in other_details:
            if 'Меблирована:' in other.text:
                furnished = other.text.replace('Меблирована: ', '')
        dataframe.at[row, 'furnished'] = {'Да': True, 'Нет': False}.get(furnished)
    except:
        pass

    try:
        for other in other_details:
            if 'Высота потолков:' in other.text:
                height = other.text.replace('Высота потолков: ', '')
        height = float(height)
        if height > 150:
            height /= 100
        elif height >= 20:
            height /= 10

        dataframe.at[row, 'ceil_height'] = height
    except:
        pass

    try:
        for other in other_details:
            if 'Ремонт:' in other.text:
                condition = other.text.replace('Ремонт: ', '')
        dataframe.at[row, 'condition'] = condition
    except:
        pass

    try:
        for other in other_details:
            if 'Комиссионные:' in other.text:
                commission = other.text.replace('Комиссионные: ', '')
        dataframe.at[row, 'commission'] = {'Да': True, 'Нет': False}.get(commission)
    except:
        pass

    # Title and text parts
    try:
        title = soup1.find('h4', class_="css-10ofhqw").text
        dataframe.at[row, 'title_text'] = title
    except:
        pass

    try:
        content = soup1.find('div', class_="css-19duwlz").text
        dataframe.at[row, 'post_text'] = content
    except:
        pass

    # Extra Details
    close_things = ''
    try:
        for other in other_details:
            if 'Рядом есть:' in other.text:
                close_things = other.text.replace('Рядом есть: ', '')
                break
    except:
        pass
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