import csv
import re
from selenium import webdriver


def ubication_and_menu_JE(input_file, restaurants_output, products_output):
    # Set up the Selenium driver
    driver = webdriver.Chrome()

    try:
        # Create a new CSV file to write data with new columns (without dishes)
        with open(restaurants_output, mode='w', newline='', encoding='utf-8') as csvfile:
            # Define column names in the new CSV file (without dishes)
            fieldnames = ['Restaurant ID', 'Restaurant Name', 'Menu URL', 'Rating', 'Address', 'Latitude', 'Longitude']

            # Create a CSV writer for the new file with column names (without dishes)
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()  # Write headers in the new CSV file (without dishes)

            # Create a new CSV file to write dish data
            with open(products_output, mode='w', newline='', encoding='utf-8') as csvfile_dishes:
                # Define column names in the dishes CSV file
                fieldnames_dishes = ['Restaurant ID', 'Dish Name', 'Dish Description']

                # Create a CSV writer for the dishes file with column names
                writer_dishes = csv.DictWriter(csvfile_dishes, fieldnames=fieldnames_dishes, delimiter=';')
                writer_dishes.writeheader()  # Write headers in the dishes CSV file

                # Read menu URLs and 'Average Rating' from the original CSV file
                with open(input_file, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=';')
                    for row in reader:
                        # Get the menu URL from the 'Menu URL' column
                        menu_url = row['Menu URL']

                        # Get the restaurant ID and 'Average Rating'
                        restaurant_id = row['Restaurant ID']

                        # Open the URL in the browser using Selenium
                        driver.get(menu_url)

                        # Get the full content of the page
                        page_content = driver.page_source

                        try:
                            # Use regular expressions to find the specific location information fragment
                            match = re.search(r'"location":\{.*?"address":"(.*?)","postCode":"(.*?)","city":"(.*?)","latitude":(.*?),"longitude":(.*?)\}', page_content)
                            if match:
                                address, post_code, city, latitude, longitude = match.groups()
                                # Add location data and 'Average Rating' to the current row (without dishes)
                                row['Address'] = address + ', ' + post_code + ', ' + city
                                row['Latitude'] = latitude
                                row['Longitude'] = longitude

                                # Write the current row to the CSV file without dishes
                                writer.writerow(row)

                            # Use regular expressions to find lines containing "type":"menuitem" to extract menus
                            menu_items = re.findall(r'"type":"menuitem".*?"name":"([^"]+)".*?"description":"(.*?)"', page_content)
                            for name, description in menu_items:
                                name = name.replace(';',',')
                                description = description.replace(';',',')
                                # Write dish data to the dishes CSV file
                                writer_dishes.writerow({'Restaurant ID': restaurant_id,
                                                       'Dish Name': name,
                                                       'Dish Description': description})

                        except Exception as e:
                            print(f"Could not extract information for URL {menu_url}: {e}")

    finally:
        # Close the Selenium driver when finished
        driver.quit()

    return restaurants_output, products_output



