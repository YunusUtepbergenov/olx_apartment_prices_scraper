import requests
from scrapy import Selector

def getCurrency():
    fx_rate_url = 'https://cbu.uz/oz/'
    fx_rate_html = requests.get(fx_rate_url).content
    fx_rate_selector = Selector(text=fx_rate_html)
    fx_rate_xpath = '//div[@class="exchange__content"]//div[@class="exchange__item_value"]'
    fx_rates = fx_rate_selector.xpath(fx_rate_xpath)
    fx_rates = fx_rates.xpath('./text()').extract()
    return float(fx_rates[0].replace(' = ', ''))