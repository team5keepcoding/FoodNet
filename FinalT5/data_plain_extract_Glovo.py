import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_and_save_data_Glovo(base_url, output_file):
    # Set up the Selenium webdriver (browser automation)
    driver = webdriver.Chrome()
    # List to store restaurant data
    restaurants_data = []

    # Build the URL for the first page
    url = base_url + '1'

    # Open the web page
    driver.get(url)

    # Wait for the page to load completely
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="modal-overlay"]')))

    # Find the maximum number of pages
    total_pages_element = driver.find_element(By.CSS_SELECTOR, 'span.current-page-text[data-v-27400e54]')
    max_pages = int(total_pages_element.text.split(' de ')[1].strip())

    # Iterate over the pages
    current_page = 1

    while current_page <= max_pages:
        # Get all restaurant elements
        restaurants = driver.find_elements(By.CSS_SELECTOR, '[data-test-id="category-store-card"]')

        # Iterate over restaurant elements and extract data
        for restaurant in restaurants:
            # Extract restaurant data
            restaurant_id = restaurant.get_attribute('id')
            name = restaurant.find_element(By.CSS_SELECTOR, '[data-test-id="store-card-title"]').text
            link = restaurant.find_element(By.CSS_SELECTOR, '[data-test-id="store-item"]').get_attribute('href')
            rating = restaurant.find_element(By.CSS_SELECTOR, '[data-test-id="store-rating-label"]').text
            #Rating transformations
            rating = rating.replace('%','')
            rating = rating.replace('--', 'N/A')

            # Add restaurant data to the list
            restaurants_data.append({
                'Restaurant ID': 'G' + restaurant_id,
                'Restaurant Name': name,
                'Menu URL': link,
                'Rating': rating,
            })

        # Go to the next page
        current_page += 1

        # If it's not the last page, load the next page
        if current_page <= max_pages:
            next_page_url = base_url + str(current_page)
            driver.get(next_page_url)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="modal-overlay"]')))

    # Close the browser after collecting the data
    driver.quit()

    # Remove duplicates based on the 'ID' column
    seen_ids = set()
    restaurants_data = [restaurant for restaurant in restaurants_data if restaurant['Restaurant ID'] not in seen_ids and not seen_ids.add(restaurant['Restaurant ID'])]

    # Save the data to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        # Set the delimiter as a semicolon
        csvwriter = csv.DictWriter(csvfile, fieldnames=restaurants_data[0].keys(), delimiter=';')

        # Write the CSV header
        csvwriter.writeheader()

        # Write restaurant data to the CSV
        csvwriter.writerows(restaurants_data)

    return restaurants_data





