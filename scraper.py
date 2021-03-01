import re
from config import keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def get_url(search_term):
    # template = 'https://www.newegg.com/p/pl?d={}'
    template = 'https://www.newegg.com/p/pl?d={}&N=4814%204023%204021%20100006662%204085%204022'
    search_term = search_term.replace(' ', '+')

    url = template.format(search_term)

    url += '&page={}'

    return url


def extract_record(item):
    try:
        a_tag = item.find('a', "item-title")
        title = a_tag.text
    except:
        title = a_tag
    print(f'EXTRACT_RECORD TITLE: {title}')

    try:
        li_tag = item.findAll('li', {"class": "price-current"})
        price = li_tag[0].text.replace(u'\xa0–', u'')
        price = clean_price(price)
    except:
        price = 'OUT OF STOCK'

    if price == '':
        price = 'OUT OF STOCK'

    print(f'EXTRACT_RECORD PRICE: {price}')

    href_tag = item.findAll('a', href=True)
    url = href_tag[0]["href"].split(' ')[0]
    print(f'EXTRACT_RECORD URL: {url}')

    print("\n")

    result = (title, price, url)
    return result


def search_newegg(search_term):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    records = []
    url = get_url(search_term)

    for page in range(1, 11):
        driver.get(url.format(page))
        if driver.current_url != url.format(page):
            print('Out of pages!')
            break
        else:
            print(f'Searching through page {page}.')
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            results = soup.find_all("div", {"class": "item-container"})

            for item in results:
                record = extract_record(item)
                if record[0]:
                    if 'ads/'not in record[2]:
                        if record[1] != 'OUT OF STOCK':
                            records.append(record)
            print("Done!")

    driver.close()
    return records


def filter_products(title):
    if keys["search_term"] in title:
        if keys["filterword6"] in title:
            return False
        elif keys["filter_word2"] in title:
            return False
        elif keys["filter_word3"] in title:
            return False
        else:
            return True
    else:
        return False


def clean_price(price):
    try:
        price_num = price.replace('$', '').replace(',', '')
    except:
        price_num = price.replace('$', '')

    price_num = float(price_num)

    return price_num


def print_list(arr):
    count = 1
    for item in arr:
        print(f'{count}. {item}')
        count += 1


def check_stock(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("div", {"id": "ProductBuy"})
    if results:
        result = results.text
        if "Add to cart" in result:
            return True
        else:
            return False
    else:
        return False


