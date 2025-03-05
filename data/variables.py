from datetime import date, timedelta
from re import compile, sub

furnished_type = ['yes', 'no']
comission_type = ['yes', 'no']
house_type = ['secondary', 'primary']

today = date.today()
yesterday = today - timedelta(days=1)
today = today.strftime('%d-%m-%Y')
yesterday = yesterday.strftime('%d-%m-%Y')

column_names = [    
                'link', 'date', 'price', 'home_type', 'city', 'district',
                'furnished', 'commission', 'num_rooms', 'area', 'apart_floor',
                'home_floor', 'condition', 'build_type', 'build_plan',
                'build_year', 'bathroom', 'ceil_height', 'hospital',
                'playground', 'kindergarten', 'park', 'recreation', 'school',
                'restaurant', 'supermarket', 'title_text', 'post_text'
               ]

month_dict = {
                ' г.': '', ' января ': '-01-', ' февраля ': '-02-', ' марта ': '-03-',
                ' апреля ': '-04-', ' мая ': '-05-', ' июня ': '-06-',
                ' июля ': '-07-', ' августа ': '-08-', ' сентября ': '-09-',
                ' октября ': '-10-', ' ноября ': '-11-', ' декабря ': '-12-',
                compile('^Сегодня.*'): today, compile('^Вчера.*'): yesterday
            }

district_dict = {
                    20: 'Olmazor', 18: 'Bektemir', 13: 'Mirobod', 12: 'Mirzo-Ulugbek',
                    19: 'Sergeli', 21: 'Uchtepa', 23: 'Chilonzor', 24: 'Shayhontohur',
                    25: 'Yunusobod', 26: 'Yakkasaroy', 22: 'Yashnobod'
                }