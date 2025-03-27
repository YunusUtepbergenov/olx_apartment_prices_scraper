from scraper import scrape
from utils.merge_files import mergeFiles

regions = ['andizhanskaya-oblast', 'dzhizakskaya-oblast', 'karakalpakstan', 'kashkadarinskaya-oblast',
            'navoijskaya-oblast' ,'namanganskaya-oblast', 'surhandarinskaya-oblast','syrdarinskaya-oblast', 
            'ferganskaya-oblast', 'horezmskaya-oblast', 'buharskaya-oblast', 'samarkandskaya-oblast'
          ]

# district_dict = {
#                     20: 'Olmazor', 18: 'Bektemir', 13: 'Mirobod', 12: 'Mirzo-Ulugbek',
#                     19: 'Sergeli', 21: 'Uchtepa', 23: 'Chilonzor', 24: 'Shayhontohur',
#                     25: 'Yunusobod', 26: 'Yakkasaroy', 22: 'Yashnobod'
#                 }

tashkent_code_list = [26,22]

tash_obl = [
            'akkurgan', 'almalyk', 'angren', 'ahangaran','bekabad', 'buka','gazalkent', 'gulbahor','durmen', 'dustabad','zangiota', 'keles','kibraj', 
            'koksaroy','krasnogórsk', 'nazarbek','tojtepa', 'parkent', 'pskent', 'xojakent','chorvoq', 'chinaz','chirchik', 'eshanguzar',
            'yangibazar', 'yangiyul', 'qorasuv', 'mirobod', 'salar', 'tashmore', 'turkiston', 'yangiobod', 'zafar'
           ]

# scrape(regions, 'viloyatlar', 'prodazha')
# scrape(tash_obl, 'tash_obl', 'prodazha')
# mergeFiles('tash_obl', 'prodazha')
scrape(tashkent_code_list, 'tashkent', 'prodazha')
mergeFiles('tashkent', 'prodazha')

# scrape(regions, 'viloyatlar', 'arenda-dolgosrochnaya')
# scrape(tash_obl, 'tash_obl', 'arenda-dolgosrochnaya')
# mergeFiles('tash_obl', 'arenda-dolgosrochnaya')
# scrape(tashkent_code_list, 'tashkent', 'arenda-dolgosrochnaya')
# mergeFiles('tashkent', 'arenda-dolgosrochnaya')