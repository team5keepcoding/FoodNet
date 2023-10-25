import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import pandas as pd


def write_csv_JE(data, filename):
    # Check if the file already exists
    file_exists = os.path.isfile(filename)

    # Open the file in 'a' (append) mode to add data
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        # If the file doesn't exist, write headers
        if not file_exists:
            writer.writerow(['Restaurant ID', 'Restaurant Name', 'Menu URL', 'Rating'])

        # Write the data
        for row in data:
            writer.writerow([row['Restaurant ID'], row['Restaurant Name'], row['Menu URL'], row['Rating']])

def scrape_and_save_data_JE(zip_codes, output_file):
    for zip_code in zip_codes:
        # Construct the complete URL with the provided zip code
        url = f'https://www.just-eat.es/area/{zip_code}-madrid/'

        # Set up the Selenium webdriver (browser automation)
        driver = webdriver.Chrome()

        # Open the web page
        driver.get(url)

        # Wait for the page to load
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h3')))

        # Get the content of the page before scrolling
        old_page = driver.page_source

        while True:
            # Execute JavaScript to scroll down (results load as you scroll)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for a random time between scrolls (for loading)
            sleep_time = random.uniform(1, 3)  # You can adjust the range according to your needs
            time.sleep(sleep_time)

            # Explicit wait to detect more results
            try:
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h3')))
            except:
                break

            # Get the content of the page after scrolling
            new_page = driver.page_source

            # Compare content before and after scrolling (to see when there are no more elements)
            if old_page == new_page:
                # If the content is the same, there are no more new items
                break

            # Update the old page to the new content
            old_page = new_page

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # List to store restaurant data
        restaurant_data = []

        # Find all <a> elements with class 'c-restaurantCardContainer'
        processed_restaurant_ids = set()
        for restaurant in soup.find_all('a', class_='c-restaurantCardContainer'):
            # Get the restaurant name
            name = restaurant.find('h3', class_='RestaurantCard_c-restaurantCard-name_1Zwfd').text.strip()

            # Get restaurant ID from 'data-restaurant-id' attribute
            restaurant_id = restaurant.get('data-restaurant-id')

            if restaurant_id not in processed_restaurant_ids:
                # Get the menu URL from 'href' attribute
                menu_url = restaurant['href']

                # Find the element with attribute data-test-id='restaurant-rating'
                rating_element = restaurant.find(attrs={'data-test-id': 'restaurant-rating'})

                # Find the element with attribute data-test-id='restaurant-rating'
                rating_element = restaurant.find(attrs={'data-test-id': 'restaurant-rating'})

                # If the element is found, get the text of the element.
                if rating_element and rating_element.text.strip().replace('.', '', 1).isdigit():
                    # Convertir el rating a un valor de 0 a 100 sin decimales y redondear el resultado
                    rating_value = round(float(rating_element.text.strip()[:3]) * 20)
                else:
                    # No rating available so 'N/A'
                    rating_value = "N/A"

                # If the element is found, get the text of the element. Take the first 4 characters as the text is like '3.10 stars out of 5'
                if rating_element:
                    rating_value = int(float(rating_element.text.strip()[:2]) * 20)

                # Add restaurant data to restaurant_data list only if rating is found
                restaurant_data.append({
                    'Restaurant ID': 'JE' + restaurant_id,
                    'Restaurant Name': name,
                    'Menu URL': "https://www.just-eat.es" + menu_url,
                    'Rating': rating_value
                })
        '''
        #Use this part of the code if it is necessary to know which restaurants accept orders at the time the script is launched, code to extend functionality.
        # Find the message indicating closed restaurants
        closed_restaurants_message = soup.find('span', {'data-test-id': 'offlinerestaurants-count-heading'})
        if closed_restaurants_message:
            closed_restaurants_count = int(closed_restaurants_message.text.split()[0])
        else:
            closed_restaurants_count = 0

        # Filter out open restaurants and their menu URLs
        open_restaurants_data = restaurant_data[:-closed_restaurants_count]

        # Save names of open restaurants (not sure if open restaurants means th)
        write_csv_JE(open_restaurants_data, 'open_restaurants_JE.csv')
        '''
        # Save names of all restaurants
        write_csv_JE(restaurant_data, output_file)

        print(f'Data for zip code {zip_code} has been saved in the corresponding CSV file.')
