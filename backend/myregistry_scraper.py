import json

from pathlib import Path
from lxml import html
import requests

MYREGISTRY_PAGE_ID = 2280168


class MyRegistryScraper:

    def __init__(self, gallery_path: str):
        self.path = Path(gallery_path)
        if not self.path.exists():
            print(f'warning {self.path} does not exist')

    def on_get(self, req, resp):
        item_path = self.path / 'registry_item.html'
        json_dict = scrape_registry_page_gifts()  # testing scraping page for info
        with open(item_path, 'r') as f:
            item_html = f.read()

        registry_html = ''
        for item in json_dict['gifts']:
            registry_html += item_html\
                .replace('[gift-title]', item['title'])\
                .replace('[gift-price]', item['price'])\
                .replace('[gift-image]', item['image'])\
                .replace('[gift-desired]', item['desire'])\
                .replace('[gift-purchased]', item['purchase'])\
                .replace('[gift-bought]', item['bought'])\
                .replace('[gift-link]', item['link'])

        resp.body = registry_html

def scrape_registry_page_gifts():
    MYREGISTRY_GIFT_LINK = f'https://www.myregistry.com/Visitors/Giftlist/PurchaseAssistant.aspx?registryId={MYREGISTRY_PAGE_ID}&giftId='
    MYREGISTRY_GIFT_PURCHASED = f'https://www.myregistry.com/Visitors/GiftList/PurchaseProcess.aspx?giftId='
    page = requests.get(
        f'https://www.myregistry.com/ExternalApps/EmbededVistorView/v2/Visitors/GiftList.aspx?registryId={MYREGISTRY_PAGE_ID}&pageSize=10000')
    tree = html.fromstring(page.content)
    gift_ids = tree.xpath('//tr[@class="itemGiftVisitorList"]/@giftid')
    gift_titles = tree.xpath('//tr[@class="itemGiftVisitorList"]/td/div[@class="gift-title"]/text()')
    gift_prices = tree.xpath('//tr[@class="itemGiftVisitorList"]/td/div[@class="gift-price"]/text()')
    gift_images = tree.xpath('//tr[@class="itemGiftVisitorList"]/td[@class="gift-image"]/img/@src')
    gift_desire = tree.xpath('//tr[@class="itemGiftVisitorList"]/td/div/div[@class="desiredQty"]/text()')
    gift_purcha = tree.xpath('//tr[@class="itemGiftVisitorList"]/td/div/div[@class="receivedQty"]/text()')
    items = {'gifts': [], 'cash_gifts': []}
    if len(gift_titles) == len(gift_prices) and len(gift_prices) == len(gift_images):
        for i in range(len(gift_titles)):
            items['gifts'].append({
                'title': str(gift_titles[i]).replace('\r\n', '').replace('  ', ''),
                'price': str(gift_prices[i]).replace('\r\n', '').replace('  ', ''),
                'image': gift_images[i],
                'link': MYREGISTRY_GIFT_LINK + gift_ids[i],
                'bought': MYREGISTRY_GIFT_PURCHASED + gift_ids[i],
                'desire': str(gift_desire[i]).replace('\r\n', '').replace('  ', ''),
                'purchase': str(gift_purcha[i]).replace('\r\n', '').replace('  ', '')
            })
    else:
        print('error lists are not same length')
        print(f'gift_ids : {len(gift_ids)}')
        print(f'gift_titles : {len(gift_titles)}')
        print(f'gift_prices : {len(gift_prices)}')
        print(f'gift_images : {len(gift_images)}')
        print(f'gift_desire : {len(gift_desire)}')
        print(f'gift_purcha : {len(gift_purcha)}')
    return items
