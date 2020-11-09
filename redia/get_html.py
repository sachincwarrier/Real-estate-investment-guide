import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


def zipcodes_list(st_items):
    # If st_items is a single zipcode string.
    if type(st_items) == str:
        zcObjects = zipcode.islike(st_items)
        output = [str(i).split(" ", 1)[1].split(">")[0]
                  for i in zcObjects]
    # If st_items is a list of zipcode strings.
    elif type(st_items) == list:
        zcObjects = [n for i in st_items for n in zipcode.islike(str(i))]
        output = [str(i).split(" ", 1)[1].split(">")[0]
                  for i in zcObjects]
    else:
        raise ValueError("input 'st_items' must be of type str or list")
    return (output)


def init_driver(filepath):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.wait = WebDriverWait(driver, 10)
    return (driver)


def navigate_to_website(driver, site):
    driver.get(site)


def click_buy_button(driver):
    try:
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "nav-header")))
        button.click()
        time.sleep(8)
    except (TimeoutException, NoSuchElementException):
        raise ValueError("Clicking the 'Buy' button failed")


def enter_search_term(driver, search_term):
    try:
        searchBar = driver.wait.until(EC.presence_of_element_located(
            (By.ID, "citystatezip")))
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "zsg-icon-searchglass")))
        searchBar.clear()
        time.sleep(2)
        searchBar.send_keys(search_term)
        time.sleep(2)
        button.click()
        time.sleep(2)
        return (True)
    except (TimeoutException, NoSuchElementException):
        return (False)


def results_test(driver):
    # Check to see if there are any returned results
    try:
        no_results = driver.find_element_by_css_selector(
            '.zoom-out-message').is_displayed()
    except (NoSuchElementException, TimeoutException):
        # Check to see if the zipcode is invalid or not
        try:
            no_results = driver.find_element_by_class_name(
                'zsg-icon-x-thick').is_displayed()
        except (NoSuchElementException, TimeoutException):
            no_results = False
    return (no_results)


def get_html(driver):
    output = []
    keep_going = True
    while keep_going:
        # Pull page HTML
        try:
            output.append(driver.page_source)
        except TimeoutException:
            pass
        try:
            # Check to see if a "next page" link exists
            keep_going = driver.find_element_by_class_name(
                'zsg-pagination-next').is_displayed()
        except NoSuchElementException:
            keep_going = False
        if keep_going:
            # Test to ensure the "updating results" image isnt displayed.
            # Will try up to 5 times before giving up, with a 5 second wait
            # between each try.
            tries = 5
            try:
                cover = driver.find_element_by_class_name(
                    'list-loading-message-cover').is_displayed()
            except (TimeoutException, NoSuchElementException):
                cover = False
            while cover and tries > 0:
                time.sleep(4)
                tries -= 1
                try:
                    cover = driver.find_element_by_class_name(
                        'list-loading-message-cover').is_displayed()
                except (TimeoutException, NoSuchElementException):
                    cover = False
            # If the "updating results" image is confirmed to be gone
            # (cover == False), click next page. Otherwise, give up on trying
            # to click thru to the next page of house results, and return the
            # results that have been scraped up to the current page.
            if cover == False:
                try:
                    element = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, 'zsg-pagination-next')))
                    element.click()
                    # driver.wait.until(EC.element_to_be_clickable(
                    #     (By.CLASS_NAME, 'zsg-pagination-next'))).click()
                    time.sleep(2)
                except TimeoutException:
                    keep_going = False
            else:
                keep_going = False
    return (output)
