import os
def getCity(district_dict, soup, type, district):
    if type == 'tashkent':
        return district_dict[district]
    else:
        return soup.find('p', class_="css-nk9te6").text.replace(',', '')
    
def makeFolder(scrape_type, type_of_district):
    directory_name = os.getcwd() + '/results/' + scrape_type + '/' + type_of_district
    print(directory_name)

    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return directory_name

def generateLink(type_of_district, scrape_type, district_dict, district, frn, cms, house='secondary'):
    if scrape_type == 'prodazha':
        if type_of_district == 'tashkent':
            olx_link = 'https://www.olx.uz/d/nedvizhimost/kvartiry/' + scrape_type +'/tashkent/?search%5Bdistrict_id%5D=' + str(district) + '&search%5Bfilter_enum_furnished%5D%5B0%5D=' + frn + '&search%5Bfilter_enum_comission%5D%5B0%5D=' + cms + '&search%5Bfilter_enum_type_of_market%5D%5B0%5D=' + house
            return olx_link, district_dict[district]
        else:
            olx_link = 'https://www.olx.uz/d/nedvizhimost/kvartiry/' + scrape_type + '/' + district + '/?search%5Bfilter_enum_furnished%5D%5B0%5D=' + frn + '&search%5Bfilter_enum_comission%5D%5B0%5D=' + cms + '&search%5Bfilter_enum_type_of_market%5D%5B0%5D=' + house
            return olx_link, district
    else:
        if type_of_district == 'tashkent':
            olx_link = 'https://www.olx.uz/d/nedvizhimost/kvartiry/' + scrape_type +'/tashkent/?search%5Bdistrict_id%5D=' + str(district) + '&search%5Bfilter_enum_furnished%5D%5B0%5D=' + frn + '&search%5Bfilter_enum_comission%5D%5B0%5D=' + cms
            return olx_link, district_dict[district]
        else:
            olx_link = 'https://www.olx.uz/d/nedvizhimost/kvartiry/' + scrape_type + '/' + district + '/?search%5Bfilter_enum_furnished%5D%5B0%5D=' + frn + '&search%5Bfilter_enum_comission%5D%5B0%5D=' + cms
            return olx_link, district