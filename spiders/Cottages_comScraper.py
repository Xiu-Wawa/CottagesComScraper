from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from geopy.geocoders import Nominatim
import math
import time
import json
import requests
import csv


class CottagesComScraper():
    API_KEY = 'AIzaSyAS8FhRC3PKt9H89HA8EhXt2yQ8avOoMmE'
    url = 'https://www.cottages.com/search?adult=2&child=0&infant=0&pets=0&range=3&nights=7&accommodationType=cottages&regionId=21696&regionName=Berkshire&destinationURL=%2Fengland%2Fberkshire&page={}&sort=nosort'

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())


    def get_request(self):
        self.driver.get(self.url.format(1))
        time.sleep(5)


    def get_property_links(self):
        wait = WebDriverWait(self.driver, 10)
        max_properties = self.driver.find_element(By.XPATH, '//h2[@class="sc-hbNdxD cVidDa"]/span[1]').text
        pagination = math.ceil(int(max_properties) / 12)
        property_links = []

        for i in range(1, pagination + 1):
            time.sleep(2)
            self.driver.get(self.url.format(i))
            links_loaded = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="sc-iYQWso jxWrMC sc-6b7fb3ce-1 gQXXKB"]/div/div[@class="sc-jFJHMl kVZGba"]/div/ul/li/article/div/div/a')))
            for link in links_loaded:
                property_links.append(link.get_attribute('href'))

        return property_links


    def get_property_details(self):
        property_links = self.get_property_links()
        with open('property_details.csv', mode='w', newline='') as csv_file:
            fieldnames = ['full_address', 'name', 'address1', 'address2', 'address3', 'city', 'county', 'postcode', 'country', 'animal', 'pet_name', 'renewal_date', 'date', 'outward_code', 'url', 'Type of Property', 'Current Manager', 'Mail Preference']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for link in property_links:
                self.driver.get(link)
                time.sleep(3)

                property_name = self.driver.find_element(By.XPATH, '//h1').text
                data = self.driver.find_element(By.XPATH, '//script[@id="__NEXT_DATA__"]').get_attribute('textContent')
                json_data = json.loads(data)

                latitude = json_data['props']['pageProps']['service']['mapDetail']['latitude']
                longitude = json_data['props']['pageProps']['service']['mapDetail']['longitude']

                geolocator = Nominatim(user_agent="my-app")
                location = geolocator.reverse(f"{latitude}, {longitude}")

                address = location.raw['address']

                writer.writerow({
                    'full_address': address,
                    'name': property_name,
                    'address1': '',
                    'address2': '',
                    'address3': '',
                    'city': address.get('city', address.get('town', '')),
                    'county': address.get('county', ''),
                    'postcode': address.get('postcode', ''),
                    'country': 'UK',
                    'animal': '',
                    'pet_name': '',
                    'renewal_date': '',
                    'date': '',
                    'outward_code': address.get('postcode', '').split(' ')[0],
                    'url': link.split('?')[0],
                    'Type of Property': '',
                    'Current Manager': '',
                    'Mail Preference': '',
            })

        self.driver.quit()







if __name__ == '__main__':
    scraper = CottagesComScraper()
    scraper.get_request()
    scraper.get_property_details()

