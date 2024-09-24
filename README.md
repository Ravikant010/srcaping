# Myntra Site Crawler

## Project Overview

The **Myntra Site Crawler** is a Python-based web scraping project developed to automate the extraction of comprehensive data from the Myntra website. This crawler navigates through the entire site, collecting detailed information across multiple categories and brands, allowing for a thorough analysis of the products listed on the platform. It is built using **Selenium** and **Beautiful Soup**, two popular Python libraries for web automation and HTML parsing, respectively.

## Features

- **Category and Brand Crawling**: The crawler systematically explores different categories and brands available on Myntra.
- **Data Extraction**: It extracts product information such as:
  - Product images
  - Specifications
  - User comments and reviews
  - Product prices
  - Ratings
  - Other relevant product details
  - comments
  - more
- **Data Storage**: The scraped data is stored in structured JSON files, with each file named according to its corresponding category for easy access and analysis.
- **Scalability**: Built to handle large-scale e-commerce websites and scrape vast amounts of data efficiently.
  
## Technologies Used

- **Python**: The primary programming language for the crawler.
- **Selenium**: Used for automating browser actions, allowing the crawler to interact with dynamically loaded content.
- **Beautiful Soup**: Used to parse HTML and extract meaningful data from the web pages.
- **JSON**: The format used to store the scraped data.
- **Scrapy**: to crawl websites and extract structured data from their pages

## How It Works

1. **Setup**: The script initializes a Selenium WebDriver (Firefox) to navigate through the Myntra website.
2. **Scraping Process**: For each category and brand, the crawler fetches the product listings and extracts relevant details.
3. **Data Parsing**: Beautiful Soup parses the HTML content and extracts the desired data points.
4. **Data Storage**: The extracted data is stored in separate JSON files, named after the respective categories.

## How to Use

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ravikant010/srcaping
   cd srcaping
   pip install -r requirements.txt
   genrate venv and activate if you can
   cd crawler/crawler/spiders
   scrapy crawl myntra_navbar_spider
   you firefox will open and start doing things auto..
   ```
[Watch Demo](https://drive.google.com/file/d/1rGHyiJg4oWTzR00dDqXrBJ9P2rtl6w3O/view)

   
   
   
   
