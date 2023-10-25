import csv
import pandas as pd


def generate_primary_keys_dish(input_file, output_file):
    # Dictionary to keep track of the last primary key for each restaurant
    last_pk_per_restaurant = {}

    # Read the original CSV file and write a new file with primary keys
    with open(input_file, 'r', encoding='utf-8', newline='') as input_file, \
         open(output_file, 'w', newline='', encoding='utf-8') as output_file:
        reader_csv = csv.reader(input_file, delimiter=';')
        writer_csv = csv.writer(output_file, delimiter=';')

        # Write headers to the output file
        headers = next(reader_csv)
        headers.insert(0, 'PK')  # Add header for the primary key
        writer_csv.writerow(headers)

        # Process rows from the CSV file
        for row in reader_csv:
            restaurant_id = row[0]

            # Generate primary key
            if restaurant_id not in last_pk_per_restaurant:
                last_pk_per_restaurant[restaurant_id] = 1
            else:
                last_pk_per_restaurant[restaurant_id] += 1

            primary_key = f'{restaurant_id}{str(last_pk_per_restaurant[restaurant_id]).zfill(4)}'

            # Write row with primary key to the output file
            row.insert(0, primary_key)
            writer_csv.writerow(row)

# Words and their corresponding codes
words_to_codes = {
    'tortilla de maiz' : None, 'tortilla de trigo': None,'tortilla de queso': None, 'samosa': None,
    'sushi': '29',
    'crispy chicken': '1', 'pollo crujiente': '1',
    'tortilla de patatas': '25', 'tortilla francesa': '25', 'omelette': '25',
    'idli': '19',
    'chapati': '12',
    'butter naan': '10', 'naan con mantequilla': '10',
    'chole bhature': '15',
    'kadai paneer': '22', 'paneer kadai': '22',
    'pizza': '28',
    'taquito': '7',
    'chai': '11',
    'hot dog': '4', 'perrito caliente': '4',
    'pakode': '26',
    'kaathi rolls': '21', 'rollos kaathi': '21',
    'chicken curry': '14', 'pollo al curry': '14',
    'donut': '2', 'rosquilla': '2',
    'jalebi': '20',
    'pav bhaji': '27',
    'dal makhani': '16',
    'ice cream': '18', 'helado': '18',
    'taco': '6',
    'momos': '24',
    'baked potato': '0', 'papa al horno': '0', 'patatas al horno': '0', 'patata al horno': '0',
    'sandwich': '5', 'sándwich': '5',
    'masala dosa': '23',
    'apple pie': '8', 'tarta de manzana': '8', 'tarta tatin': '8',
    'cheesecake': '13', 'tarta de queso': '13',
    'fried rice': '17', 'arroz frito': '17', 'yakimeshi' : '17',
    'burger': '9', 'hamburguesa': '9',
    'fries': '3', 'papas fritas': '3', 'patatas fritas': '3'
}


def assign_value(row, words_to_codes):
    dish_name = str(row['Dish Name']).lower() if pd.notnull(row['Dish Name']) else ''
    description = str(row['Dish Description']).lower() if pd.notnull(row['Dish Description']) else ''

    # Search words in the dictionary and return the code if found
    for word in words_to_codes:
        if word in description or word in dish_name:
            return words_to_codes[word]
    return None

def process_file(input_filename, output_filename):
    # Read the CSV file
    df = pd.read_csv(input_filename, delimiter=';', encoding='utf-8')
    df['Dish Description'] = df['Dish Description'].astype(str)
    # Limit maximum length of 'Dish Description' column to 1500 characters and append ' etc.' at the end if it exceeds the limit
    max_description_length = 1500
    df['Dish Description'] = df['Dish Description'].apply(lambda x: x[:max_description_length] + (' etc.' if len(x) > max_description_length else ''))
    # Apply the function to a new column called 'Dish ID'
    df['Dish ID'] = df.apply(lambda x: assign_value(x, words_to_codes), axis=1)
    # Drop rows where 'Dish ID' is None (no matches)
    df = df.dropna(subset=['Dish ID'])
    # Write the modified DataFrame to the output CSV file
    df.to_csv(output_filename, sep=';', index=False, encoding='utf-8')

def add_PK_dish(input_file, output_file):
    # Dictionary to keep track of the last primary key for each restaurant
    last_primary_key_by_restaurant = {}

    # Open the input CSV file for reading and the output CSV file for writing
    with open(input_file, 'r', encoding='utf-8', newline='') as input_file, open(output_file, 'w', newline='', encoding='utf-8') as output_file:
        # Create CSV reader and writer objects
        csv_reader = csv.reader(input_file, delimiter=';')
        csv_writer = csv.writer(output_file, delimiter=';')

        # Read the headers from the input file
        headers = next(csv_reader)
        # Insert 'PK' as the first header in the output file
        headers.insert(0, 'PK')
        # Write headers to the output file
        csv_writer.writerow(headers)

        # Process rows from the input CSV file
        for row in csv_reader:
            restaurant_id = row[0]  # Extract restaurant ID from the current row

            # Check if the restaurant ID is in the dictionary
            if restaurant_id not in last_primary_key_by_restaurant:
                # If not, assign the first primary key (1) to the restaurant
                last_primary_key_by_restaurant[restaurant_id] = 1
            else:
                # If yes, increment the last primary key for the restaurant
                last_primary_key_by_restaurant[restaurant_id] += 1

            # Generate the primary key by combining restaurant ID and a 4-digit number (zero-padded)
            primary_key = f'{restaurant_id}{str(last_primary_key_by_restaurant[restaurant_id]).zfill(4)}'

            # Insert the generated primary key as the first element in the current row
            row.insert(0, primary_key)
            
            # Write the modified row with primary key to the output file
            csv_writer.writerow(row)



def filter_by_ids(input_filename, output_filename, ids_filename):
    # Read the CSV file with IDs
    ids_df = pd.read_csv(ids_filename, delimiter=';', encoding='utf-8')
    
    # Read the original CSV file
    df = pd.read_csv(input_filename, delimiter=';', encoding='utf-8')
    
    # Filter the original DataFrame using IDs from the second file
    filtered_df = df[df['ID'].isin(ids_df['ID'])]
    
    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_filename, index=False, sep=';', encoding='utf-8')
