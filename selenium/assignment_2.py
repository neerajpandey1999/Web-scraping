# main.py

import time
import csv
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re
from locators import CLOSE_LOGIN_POPUP_XPATH, SEARCH_INPUT_NAME, PRODUCT_CONTAINER_XPATH, PRODUCT_NAME_XPATH, \
    PRODUCT_PRICE_XPATH, PRODUCT_REVIEW_XPATH, NEXT_PAGE_BUTTON_XPATH

config = configparser.ConfigParser()
config.read('config.ini')

# Browser options
def get_browser_options(browser_name):
    options = None
    if browser_name == 'chrome':
        options = ChromeOptions()
    elif browser_name == 'firefox':
        options = FirefoxOptions()

    if options and config.getboolean('settings', 'headless'):
        options.add_argument("--headless")

    return options

def get_driver(browser_name):
    if browser_name == 'chrome':
        options = get_browser_options('chrome')
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    # elif browser_name == 'firefox':
    #     options = get_browser_options('firefox')
    #     # Explicitly specify the path to geckodriver
    #     return webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', options=options)
    else:
        raise ValueError("Unsupported browser. Please choose 'chrome' or 'firefox'.")


class FlipkartMonitorScraper:

    def __init__(self):
        self.browser = None
        if config.getboolean('settings', 'enable_chrome'):
            self.browser = 'chrome'
        elif config.getboolean('settings', 'enable_firefox'):
            self.browser = 'firefox'
        else:
            raise ValueError(
                "No browser enabled in config.ini. Please enable either 'enable_chrome' or 'enable_firefox'.")

        self.driver = get_driver(self.browser)
        self.base_url = config['urls']['base_url']
        self.resolution_pattern = re.compile(r'(\d+\.?\d*)\s?cm\s\(\d+\.?\d*\s?inch\)')
        self.manufacturer_pattern = re.compile(r'^(.*?)(?=\d+\.?\d*\s?cm\s\(\d+\.?\d*\s?inch\))')

        # Maximize window if specified in config
        if config.getboolean('settings', 'maximize_window'):
            self.driver.maximize_window()

    def open_flipkart_and_search(self):
        self.driver.get(self.base_url)
        time.sleep(3)

        try:
            close_button = self.driver.find_element(By.XPATH, CLOSE_LOGIN_POPUP_XPATH)
            close_button.click()
        except:
            pass

        search_input = self.driver.find_element(By.NAME, SEARCH_INPUT_NAME)
        search_input.send_keys("monitors")
        search_input.send_keys(u'\ue007')
        time.sleep(3)

    def scrape_all_pages(self):
        all_product_data = []

        for page in range(1, 21):
            print(f"Scraping page {page}")
            page_data = self.scrape_products()
            all_product_data.extend(page_data)

            # Go to the next page
            try:
                next_button = self.driver.find_element(By.XPATH, NEXT_PAGE_BUTTON_XPATH)
                next_button.click()
                time.sleep(3)
            except:
                print("No more pages or unable to find the next button")
                break

        return all_product_data

    def scrape_products(self):
        products = self.driver.find_elements(By.XPATH, PRODUCT_CONTAINER_XPATH)
        product_data = []
        for product in products:
            try:
                name = product.find_element(By.XPATH, PRODUCT_NAME_XPATH).text
                price = product.find_element(By.XPATH, PRODUCT_PRICE_XPATH).text
                review_stars = product.find_element(By.XPATH, PRODUCT_REVIEW_XPATH).text

                resolution_match = self.resolution_pattern.search(name)
                manufacturer_match = self.manufacturer_pattern.search(name)

                manufacturer = manufacturer_match.group(1).strip() if manufacturer_match else 'N/A'
                resolution = resolution_match.group(1).strip() if resolution_match else 'N/A'

                product_data.append({
                    'Model': name,
                    'Price': price,
                    'Resolution': resolution,
                    'Manufacturer': manufacturer,
                    'ReviewStars': review_stars
                })
            except Exception as e:
                print(f"Error extracting product: {e}")
                continue

        return product_data

    def save_to_csv(self, data):
        keys = data[0].keys() if data else []
        with open('monitors_data.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

        print("Data saved to monitors_data.csv")

    def run(self):
        try:
            self.open_flipkart_and_search()
            all_data = self.scrape_all_pages()
            self.save_to_csv(all_data)
        finally:
            self.driver.quit()

if __name__ == "__main__":
    scraper = FlipkartMonitorScraper()
    scraper.run()
