# monitor_spider.py

import scrapy
import re
from ..items import MonitorItem


class MonitorSpider(scrapy.Spider):
    name = "assignment2"

    def __init__(self, *args, **kwargs):
        super(MonitorSpider, self).__init__(*args, **kwargs)
        self.base_url = "https://www.flipkart.com/search?q=montiors&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

        self.resolution_pattern = re.compile(r'(\d+\.?\d*)\s?cm\s\(\d+\.?\d*\s?inch\)')
        self.manufacturer_pattern = re.compile(r'^(.*?)(?=\d+\.?\d*\s?cm\s\(\d+\.?\d*\s?inch\))')

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        for page in range(1, 21):
            url = f"{self.base_url}&page={page}"
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        products = response.xpath('//div[@class="cPHDOP col-12-12"]')

        for product in products:
            item = MonitorItem()  # Create an item instance
            name = product.xpath('.//div[@class="KzDlHZ"]/text()').get()
            price = product.xpath('.//div[contains(@class, "Nx9bqj")]/text()').get()
            review_stars = product.xpath('.//span[@class="Y1HWO0"]/div[@class="XQDdHH"]/text()').get()
            if not review_stars:
                review_stars = product.xpath('.//span[@class="Y1HWO0"]/text()').get()

            if name:
                name_text = name.strip()
                resolution_match = self.resolution_pattern.search(name_text)
                manufacturer_match = self.manufacturer_pattern.search(name_text)

                item['Model'] = name_text
                item['Price'] = price.strip() if price else 'N/A'
                item['Resolution'] = resolution_match.group(1).strip() if resolution_match else 'N/A'
                item['Manufacturer'] = manufacturer_match.group(1).strip() if manufacturer_match else 'N/A'
                item['ReviewStars'] = review_stars.strip() if review_stars else 'No Rating'

                yield item
