import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from ..items import pd_base
import logging
import time
import json
import os
import re

class MyntraNavbarSpider(scrapy.Spider):
    name = "myntra_navbar_spider"
    allowed_domains = ["www.myntra.com"]
    start_urls = ["https://www.myntra.com/"]
    base_url = "https://www.myntra.com"
    PAGE_LIMIT = 5
    nav_bar_links = []
    crawler_count = 0
    next_count = 0
    driver = webdriver.Firefox()
    data = []

    def link_opener(self, nav_link):
        if self.crawler_count < 6:
            self.driver.get(self.base_url + nav_link)
            time.sleep(2)
            self.crawl_pages()
            self.next_count = 0
            self.crawler_count += 1
            return self.link_opener(self.nav_bar_links[self.crawler_count])
        else:
            self.driver.quit()

    def crawl_pages(self):
        while self.next_count < 6 and self.crawler_count < self.PAGE_LIMIT:
            time.sleep(2)
            if self.next_count < 2:
                self.parse_page(self.driver.page_source)
                self.get_next_link(self.driver)
                time.sleep(2)
            self.next_count += 1

    def parse(self, response):
        self.nav_bar_links = response.xpath(
            "//nav[@class='desktop-navbar']//ul[@class='desktop-navBlock']/li/a/@href"
        ).extract()
        self.link_opener(self.nav_bar_links[self.crawler_count])

    def parse_page(self, page_source):
        page_source = BeautifulSoup(page_source, "html.parser")
        print(page_source.prettify())
        logging.debug("Processing page content...")
        product_base_container = page_source.find("ul", class_="results-base")
        product_base = product_base_container.find_all("li", class_="product-base")
        time.sleep(3)

        if product_base:
            for pd in product_base:
                _pd_base = pd_base()
                try:
                    _pd_base['brand'] = pd.find('h3', class_='product-brand').get_text()
                except AttributeError:
                    _pd_base['brand'] = None
                try:
                    _pd_base['product'] = pd.find('h4', class_='product-product').get_text()
                except AttributeError:
                    _pd_base['product'] = None
                try:
                    _pd_base["pd_picture"] = pd.select_one('div.product-sliderContainer img.img-responsive')["src"]
                except (KeyError, TypeError):
                    _pd_base["pd_picture"] = None
                try:
                    _pd_base["dscnt_price"] = pd.find('span', class_='product-discountedPrice').get_text()
                except AttributeError:
                    _pd_base["dscnt_price"] = None
                try:
                    _pd_base["pd_strike"] = pd.find('span', class_='product-strike').get_text()
                except AttributeError:
                    _pd_base["pd_strike"] = None
                try:
                    _pd_base["pd_dscnt_price"] = pd.find('span', class_='product-discountPercentage').get_text()
                except AttributeError:
                    _pd_base["pd_dscnt_price"] = None

                a_tag = pd.find('a')
                href = a_tag.get('href')
                full_url = self.base_url+"/"+ href
                self.driver.get(full_url)
                page_source = BeautifulSoup(self.driver.page_source, "html.parser")
                items_pics_flex_container = page_source.find("div", class_ = "image-grid-container common-clearfix")
                image_grid_images= items_pics_flex_container.find_all('div', class_ ='image-grid-image')
                url_pattern = re.compile(r'url\("([^"]+)"\)')
                image_urls = []
                product_id = page_source.find("span", class_ ="supplier-styleId").get_text()

                seller = page_source.find('span', class_ = "supplier-productSellerName").get_text()


                for div in image_grid_images:
                    style = div.get('style')
                    if style:
                        match = url_pattern.search(style)
                        if match:
                            image_urls.append(match.group(1))

                print(image_grid_images)
                product_title = page_source.find('h1', class_='pdp-title').get_text()
                price = page_source.find('span', class_='pdp-price').get_text()
                ratings = page_source.find('div', class_='index-overallRating').get_text()
                ratings_count = page_source.find('div', class_='index-ratingsCount').get_text()
                sizes_container = page_source.find_all('p', class_ = 'size-buttons-unified-size')
                sizes = [size.get_text(strip=True) for size in sizes_container]
                product_description = page_source.find('p', class_ = 'pdp-product-description-content').get_text()
                pdp_size_fit = page_source.find('p', class_ = 'pdp-sizeFitDescContent pdp-product-description-content').get_text()
                pd_material = page_source.find('p', 'pdp-sizeFitDescContent ', class_ = 'pdp-product-description-content').get_text()
                print(pdp_size_fit, "pdp_size_fit",pd_material)
                print(product_description, sizes, seller)
                try:
                    button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[1]/main/div[2]/div[2]/div[3]/div/div[4]/div[2]"))
                    )
                    button.click()
                except TimeoutException:
                    pass  # Do nothing if the button is not available
                except Exception as e:
                    print("An error occurred:", e)
                time.sleep(2)
                divs = page_source.find_all('div', class_='index-row')
                print(divs)
                key_value_pairs = {}

                for div in divs:
                    key = div.find('div', class_='index-rowKey').text.strip()
                    value = div.find('div', class_='index-rowValue').text.strip()
                    key_value_pairs[key] = value

                print(key_value_pairs)

                try:
                    a_link = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[1]/main/div[2]/div[2]/main/div/div/a"))
                        )
                    a_link.click()
                except TimeoutException:
                    print("Link not found within the specified time")
                except Exception as e:
                    print("An error occurred:", e)
                
                time.sleep(2)

                comments = BeautifulSoup(self.driver.page_source, "html.parser")
                comments_container = comments.find_all('div', class_='user-review-userReviewWrapper')
                comments_dict = []

                for comment in comments_container:
                    print('Comment:', comment.prettify())
                    text_comment = comment.find('div', class_ = "user-review-reviewTextWrapper").get_text()
                    images = comment.find_all('img', class_='image-thumb-wrapper-image')
                    image_sources = [image['src'] for image in images]
                    user_review_left_div = comment.find('div', class_='user-review-left')
                    name_span = user_review_left_div.find('span').get_text()
                    date_span = user_review_left_div.find_all('span')[1].get_text()
                    comment_dict = {"comment": text_comment, "images": image_sources, "user_name": name_span, "date":  date_span}

                    comments_dict.append(comment_dict)
                
                print(comments_dict)

                # _pd_base['comments'] = comments_dict
                _pd_base['item_spec'] = key_value_pairs if key_value_pairs else None
                _pd_base['image_urls'] = image_urls if image_urls else None
                _pd_base['comments'] = comments_dict if comments_dict else None
                _pd_base['product_id'] = product_id if product_id else None
                _pd_base['seller_name'] = seller if seller else None
                _pd_base['sizes'] = sizes if sizes else None
                _pd_base['product_desc'] = product_description if product_description else None
             
                try:
                    _pd_base["product_title"] = product_title
                except AttributeError:
                    _pd_base["product_title"] = None
                try:
                    _pd_base["price"] = price
                except AttributeError:
                    _pd_base["price"] = None
                try:
                    _pd_base['ratings']  =  ratings
                except AttributeError:
                    _pd_base["price"] = None
                try:
                    _pd_base['rating_count'] = ratings_count
                except AttributeError:
                    _pd_base['rating_count'] = None
                

                self.data.append(dict(_pd_base))


    def json_dump(self, nav_link):
        file_name = f"{nav_link.replace('/', '_')}.json"
        file_path = os.path.join(os.getcwd(), file_name)
        with open(file_path, "w") as json_file:
            json.dump(self.data, json_file, indent=2)

    def get_next_link(self, driver):
        try:
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.pagination-container li.pagination-next a'))
            )
            next_button.click()
            return driver

        except Exception as e:
            logging.warning(f"Error while getting next link: {e}")
            return None

    def closed(self, reason):
        self.json_dump(self.nav_bar_links[self.crawler_count - 1])  # Dump data when spider is closed
