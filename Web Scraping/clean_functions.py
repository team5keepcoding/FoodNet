#CleanFunctions
import pandas as pd

def remove_duplicates_csv(input_file, output_file):
    # Read the CSV file with semicolon delimiter and specify the data type of the 'rating' column as str (string)
    # Disable filtering of N/A values to keep them as they are
    df = pd.read_csv(input_file, delimiter=';', dtype={'rating': str}, na_filter=False)

    # Remove duplicate rows based on the 'ID' column
    df_without_duplicates = df.drop_duplicates(subset='Restaurant ID')

    # Save the resulting DataFrame to a new CSV file with semicolon delimiter
    df_without_duplicates.to_csv(output_file, index=False, sep=';')
    print(f"The duplicates in the input file have been deleted and the result has been saved in '{output_file}'.")

import re

def clean_csv_file(input_file, output_file):
    transformed_lines = []

    with open(input_file, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            # Split the line into fields by semicolon
            fields = line.strip().split(';')
            
            transformed_fields = []
            for field in fields:
                # Remove unicode strings
                field = re.sub(r'\\u[0-9A-Fa-f]{4}', '', field)
                # Replace dashes with commas
                field = field.replace('-', ',')
                field = field.replace(';', ',')
                # Remove backslashes (\), line breaks (\n), carriage returns (\r), and tabs (\t)
                field = ''.join(c for c in field if c not in ('\\', '\n', '\r', '\t'))
                # Remove other special characters, except whitespace and commas
                field = re.sub(r'[^\w\s,]', '', field)
                
                # Add the transformed field to the list of transformed fields
                transformed_fields.append(field)
            
            # Join the transformed fields into a new CSV line with semicolon as delimiter
            new_line = ';'.join(transformed_fields)
            
            # Add the transformed line to the list of transformed lines
            transformed_lines.append(new_line)

    # Write the transformed lines to a new CSV file
    with open(output_file, 'w', encoding='utf-8') as output_file:
        for line in transformed_lines:
            output_file.write(line + '\n')


def remove_rows_with_null_lat_long(input_file, output_file):
    # Load the CSV file as a DataFrame
    data = pd.read_csv(input_file, delimiter=';', encoding='utf-8')

    # Count the number of rows before removing null latitude and longitude rows
    total_rows_before = len(data)

    # Remove rows where both latitude and longitude are null
    clean_data = data.dropna(subset=['Latitude', 'Longitude'])

    # Count the number of rows after removing null latitude and longitude rows
    total_rows_after = len(clean_data)

    # Save the clean DataFrame to a new CSV file
    clean_data.to_csv(output_file, index=False, sep=';', encoding='utf-8')

    print(f"The original file had {total_rows_before} rows.")
    print(f"{total_rows_before - total_rows_after} rows with null latitude and longitude have been removed.")
    print(f"The '{output_file}' file has been created with {total_rows_after} rows.")

def filter_by_ids(input_filename, output_filename, ids_filename):
    # Read the CSV file with IDs
    ids_df = pd.read_csv(ids_filename, delimiter=';', encoding='utf-8')

    # Read the original CSV file
    df = pd.read_csv(input_filename, delimiter=';', encoding='utf-8')

    # Filter the original DataFrame using IDs from the second file
    filtered_df = df[df['Restaurant ID'].isin(ids_df['Restaurant ID'])]

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_filename, index=False, sep=';', encoding='utf-8') 