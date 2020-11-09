import time
import zillow_functions as zl
import get_html as ht
from bs4 import BeautifulSoup
import boto
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from get_data import parse_json_file, parse_zip_code


driver = ht.init_driver("/anaconda/bin/chromedriver")
# driver = webdriver.Chrome(ChromeDriverManager().install())


def scrape_data(zip):
    url = "http://www.zillow.com/homes/" + zip
    ht.navigate_to_website(driver, url)
    rawdata = ht.get_html(driver)
    print(str(len(rawdata)) + " pages of listings found")
    # listings = zl.get_listings(rawdata)
    # print("rana")
    # print(listings)

    to_write = 'addresses' + zip + '.html'
    w = open(to_write, 'w', encoding='utf-8')
    for n in rawdata:
        w.write(n)
    w.close()


# for key, value in enumerate(zipcodes):
#     scrape_data(value)
if __name__ == '__main__':
    json_rest = parse_json_file('zip_list.json')
    zip_codes = parse_zip_code(json_rest, 'Travis')
    for zip in zip_codes:
        scrape_data(zip)
        time.sleep(3000)

# scrape_data(['94105'])

# Close the webdriver connection.
    zl.close_connection(driver)
