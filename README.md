# Web Scraping Projects

This repository includes code for scraping data from websites using Beautiful Soup, Scrapy, and Selenium. The project consists of two main assignments:

## Assignment 1: Scrape the TFT Website and Generate a Word Document

### Objective
- **Task**: Scrape data from the TFT website.
- **Output**: Generate a Word document containing the scraped data.

### Tools
- **Beautiful Soup**: For parsing HTML and extracting data.
- **Scrapy**: For scraping the website.
- **Python-docx**: For creating the Word document.
- **Selenium**: For dynamic content scraping (if needed).

### Instructions
1. **Using Beautiful Soup**:
   - Create a configuration file to store the URL of the TFT website.
   - Write a script to scrape the data and save it into a Word document.

2. **Using Scrapy**:
   - Create a Scrapy project and define a spider to scrape the TFT website.
   - Export the scraped data to a JSON file.
   - Convert the JSON data into a Word document using a separate script.

3. **Using Selenium** (if needed):
   - Set up Selenium with ChromeDriver.
   - Write a Selenium script to scrape the TFT website if it has dynamic content not handled by Beautiful Soup or Scrapy.

## Assignment 2: Scrape Flipkart/Amazon Website for Monitors and Create a CSV

### Objective
- **Task**: Scrape product details for monitors from Flipkart/Amazon.
- **Output**: Create a CSV file containing the product details of the first 20 pages.

### Details to Scrape
- **Fields**: Model, Price, Resolution, Manufacturer, Review Stars.

### Tools
- **Beautiful Soup**: For parsing HTML and extracting data.
- **Scrapy**: For scraping the website.
- **Pandas** and **Numpy**: For processing and saving data into CSV format.
- **Selenium**: For handling dynamic content and complex page interactions.

### Instructions
1. **Using Beautiful Soup**:
   - Create a configuration file to store the base URL of the Flipkart/Amazon website.
   - Write a script to scrape data from the first 20 pages and save it into a CSV file.

2. **Using Scrapy**:
   - Create a Scrapy project and define a spider to scrape the monitor details.
   - Export the scraped data directly to a CSV file.

3. **Using Selenium**:
   - Set up Selenium with ChromeDriver.
   - Write a Selenium script to scrape the Flipkart/Amazon website, especially if it includes dynamic content or requires user interactions.
   - Save the data into a CSV file.
