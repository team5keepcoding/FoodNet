import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from geopy.geocoders import Nominatim
import re

def get_coordinates(address):
    geolocator = Nominatim(user_agent="my_geocoder")
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print("Error obtaining coordinates for address", address, ":", str(e))
    return None, None

def ubication_and_menu_Glovo(input_file, output_file_1, output_file_2):
    driver = webdriver.Chrome()

    with open(input_file, "r", encoding="utf-8") as csvfile:
        fields_1 = ["Restaurant ID", "Restaurant Name", "Menu URL", "Rating", "Address", "Latitude", "Longitude"]
        csv_writer_1 = csv.writer(open(output_file_1, "w", encoding="utf-8", newline=""), delimiter=';')
        csv_writer_1.writerow(fields_1)

        fields_2 = ["Restaurant ID", "Dish Name", "Dish Description"]
        csv_writer_2 = csv.writer(open(output_file_2, "w", encoding="utf-8", newline=""), delimiter=';')
        csv_writer_2.writerow(fields_2)

        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            restaurant_id = row["Restaurant ID"]
            restaurant_name = row["Restaurant Name"]
            link = row["Menu URL"]
            rating = row['Rating']

            driver.get(link)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            page_source = driver.page_source

            address_match_store_address = re.search(r'address:"(.*?)",', page_source)
            if address_match_store_address:
                address = address_match_store_address.group(1)
            else:
                address_match_address = re.search(r'storeAddress:{text:"(.*?)"', page_source)
                if address_match_address:
                    address = address_match_address.group(1)
                else:
                    address = "Address not found"

            # Obtain geographical coordinates using Geopy
            latitude, longitude = get_coordinates(address)
            products = driver.find_elements(By.CSS_SELECTOR, '.product-row__name span')
            descriptions = driver.find_elements(By.CSS_SELECTOR, '.product-row__info__description span')

            for product, description in zip(products, descriptions):
                dish_name = product.text.replace(';', ',')
                dish_description = description.text.replace(';', ',')
                csv_writer_2.writerow([restaurant_id, dish_name, dish_description])

            csv_writer_1.writerow([restaurant_id, restaurant_name, link, rating, address, latitude, longitude])

    driver.quit()

def try_complete_coordinates(input_file, output_file):
    geolocator = Nominatim(user_agent="my_geocoder")

    def clean_address(address):
        # Remove "de" after "Calle"
        address = re.sub(r'(Calle|C/|Av\.|C\.)\s+de\b', r'\1 ', address)
        # Remove text before "Calle", "C/", "Av" or "C."
        address = re.sub(r'^.*?\b(Calle|C/|Av\.|C\.)\s*', r'\1 ', address)
        # Remove "Prta" and replace with "Puerta"
        address = address.replace('Prta', 'Puerta')
        # Remove "Local + space + number + ","
        address = re.sub(r'Local\s+\d+,', '', address)
        # Remove space + A or B or C or D + ","
        address = re.sub(r' [ABCD],', ',', address)
        # Remove º symbol
        address = address.replace('º', '')
        address.lower()
        return address.strip()

    # Load the CSV file as a DataFrame
    data = pd.read_csv(input_file, delimiter=';', encoding='utf-8')

    # Iterate through the DataFrame and complete the coordinates
    for index, row in data.iterrows():
        if pd.isnull(row['Latitude']) or pd.isnull(row['Longitude']):
            # Clean the address
            cleaned_address = clean_address(row['Address'])
            try:
                # Obtain geographical coordinates using Geopy
                location = geolocator.geocode(cleaned_address)
                if location:
                    data.at[index, 'Latitude'] = location.latitude
                    data.at[index, 'Longitude'] = location.longitude
            except Exception as e:
                print("Error obtaining coordinates for address", cleaned_address, ":", str(e))
    
    # Save the cleaned DataFrame to a new CSV file
    data.to_csv(output_file, index=False, sep=';', encoding='utf-8')


