import requests
from lxml import html
import pandas as pd
import json
import re

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)
base_url = config['base_url']

data = []

# Setup headers with comprehensive details
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
session = requests.Session()
session.headers.update(headers)

# Define regex patterns
resolution_pattern = re.compile(r'(\d+\.?\d*)\s?cm\s\(\d+\.?\d*\s?inch\)')
manufacturer_pattern = re.compile(r'^(.*?)(?=\d+\.?\d*\s?cm\s\(\d+\.?\d*\s?inch\))')

for page in range(1, 21):
    url = f"{base_url}&page={page}"
    response = session.get(url)

    if response.status_code == 403:
        print(f"Access forbidden on page {page}.")
        break  # Exit loop if access is forbidden

    tree = html.fromstring(response.content)

    products = tree.xpath('//div[@class="cPHDOP col-12-12"]')

    for product in products:
        name = product.xpath('.//div[@class="KzDlHZ"]/text()')
        price = product.xpath('.//div[contains(@class, "Nx9bqj")]/text()')
        review_stars = product.xpath('.//span[@class="Y1HWO0"]/div[@class="XQDdHH"]/text()')
        if not review_stars:
            review_stars = product.xpath('.//span[@class="Y1HWO0"]/text()')

        if name:
            name_text = name[0].strip()
            resolution_match = resolution_pattern.search(name_text)
            manufacturer_match = manufacturer_pattern.search(name_text)

            manufacturer = manufacturer_match.group(1).strip() if manufacturer_match else 'N/A'
            resolution = resolution_match.group(1).strip() if resolution_match else 'N/A'

            data.append({
                'Model': name_text,
                'Price': price[0].strip() if price else 'N/A',
                'Resolution(cm)': resolution,
                'Manufacturer': manufacturer,
                'Review Stars': review_stars[0].strip() if review_stars else 'No Rating'
            })

# Convert to DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('monitors_data.csv', index=False)
