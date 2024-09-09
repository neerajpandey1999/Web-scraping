# import requests
# from bs4 import BeautifulSoup
# import json
# from docx import Document
#
# # Load the URL from config.json
# with open('config.json') as config_file:
#     config = json.load(config_file)
#     url = config['url']
#
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
#
# elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'ul'])
#
# # Create a Word document
# doc = Document()
# doc.add_heading('TFT Website Scraped Data', 0)
#
# for element in elements:
#     # Handle headers (h1-h6)
#     if element.name.startswith('h'):
#         level = int(element.name[1])
#         doc.add_heading(element.text.strip(), level=level)
#         next_sibling = element.find_next_sibling()
#         while next_sibling and next_sibling.name == 'p':
#             doc.add_paragraph(next_sibling.text.strip())
#             next_sibling = next_sibling.find_next_sibling()
#
#     elif element.name == 'span':
#         doc.add_paragraph(element.text.strip())
#
#     elif element.name == 'ul':
#         for li in element.find_all('li'):
#             doc.add_paragraph(f"• {li.text.strip()}", style='List Bullet')
#
# doc.save('tft_scraped_data.docx')
#
# print('Data has been saved to tft_scraped_data.docx')



import requests
from lxml import html
from docx import Document
import json

# Load the URL from config.json
with open('config.json') as config_file:
    config = json.load(config_file)
    url = config['url']

response = requests.get(url)
tree = html.fromstring(response.content)

# XPath queries to get elements
headers = tree.xpath('//h1 | //h2 | //h3 | //h4 | //h5 | //h6')
spans = tree.xpath('//span')
lists = tree.xpath('//ul')

# Create a Word document
doc = Document()
doc.add_heading('TFT Website Scraped Data', 0)

for element in headers:
    level = int(element.tag[1])
    doc.add_heading(element.text.strip(), level=level)
    # Fetch and add the following paragraphs
    next_sibling = element.getnext()
    while next_sibling is not None and next_sibling.tag == 'p':
        doc.add_paragraph(next_sibling.text.strip())
        next_sibling = next_sibling.getnext()

for element in spans:
    doc.add_paragraph(element.text.strip())

for element in lists:
    for li in element.xpath('./li'):
        doc.add_paragraph(f"• {li.text.strip()}", style='List Bullet')

doc.save('tft_scraped_data.docx')

print('Data has been saved to tft_scraped_data.docx')
