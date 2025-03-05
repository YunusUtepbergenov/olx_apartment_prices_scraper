from pandas import DataFrame
from bs4 import BeautifulSoup
from math import ceil
from data.driver import driver
from data.variables import furnished_type, comission_type, house_type, column_names, month_dict, district_dict
from utils.getCurrency import getCurrency
from utils.helpers import getCity, makeFolder, generateLink
from utils.house import house_scrape

usd_to_uzs = getCurrency()

def scrape(district_code_list, type_of_district, scrape_type):
    directory_name = makeFolder(scrape_type, type_of_district)
    
    for district in district_code_list:
        dataframe = DataFrame(columns=column_names)
        row = 1
        for house in house_type:
            for frn in furnished_type:
                for cms in comission_type:
                    olx_link, filename = generateLink(type_of_district, scrape_type, district_dict, district, frn, cms, house)
                    driver.get(olx_link)
                    html_text = driver.page_source
                    soup = BeautifulSoup(html_text, 'lxml')
                    total_count = soup.find('span', attrs={'data-testid': 'total-count'}).text
                    
                    s = ''.join(x for x in total_count if x.isdigit())

                    if int(s) > 0 :
                        num_pages = ceil(int(s) / 39)
                        num_pages = min(num_pages, 25)
                        print("Calculating " + filename + " and Total " + str(num_pages) + " pages")
                        for page in range(num_pages):
                            print("Scraping page: " + str( page + 1))
                            page_link = olx_link + '&page=' + str(page+1)
                            driver.get(page_link)
                            html = driver.page_source
                            soup = BeautifulSoup(html, 'lxml')
                            all_table = soup.find('div', class_="css-j0t2x2")
                            if all_table:
                                apartments = all_table.find_all('div', attrs={'data-cy': 'l-card'})
                                for apartment in apartments:
                                    house_scrape(apartment, dataframe, row, driver, usd_to_uzs, month_dict, getCity, district_dict, type_of_district, district)
                                    row = row + 1
        dataframe.to_excel(directory_name + '/' + filename + ".xlsx", index=False)
        print(filename + ".xlsx file is ready")