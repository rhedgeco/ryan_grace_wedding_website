import json

from lxml import html
import requests

MYREGISTRY_PAGE_ID = 2280168


class MyRegistryScraper:
    def on_get(self, req, resp):
        print('getting title')
        titles = scrape_registry_page()  # testing scraping page for info
        json_dict = {'titles': titles}
        for i in range(len(titles)):
            titles[i] = str(titles[i]).replace('\r', '').replace('\n', '')
        resp.body = json.dumps(json_dict, ensure_ascii=False)


def scrape_registry_page():
    page = requests.get(
        f'https://www.myregistry.com/ExternalApps/EmbededVistorView/v2/Visitors/GiftList.aspx?registryId={MYREGISTRY_PAGE_ID}&pageSize=10000')
    print('got server response ' + str(page.content))
    tree = html.fromstring(page.content)
    titles = tree.xpath('//div[@class="gift-title"]/text()')
    return titles
