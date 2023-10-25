import csv
import os
import pandas as pd

def extract_first_n_lines(input_file, output_file, n=10, delimiter=';'):
    # Read the first n lines from the original CSV file
    with open(input_file, 'r') as original_file:
        csv_reader = csv.reader(original_file, delimiter=delimiter)
        lines = [next(csv_reader) for _ in range(n+1)]

    # Write the first n lines to a new CSV file
    with open(output_file, 'w', newline='') as new_file:
        csv_writer = csv.writer(new_file, delimiter=delimiter)
        csv_writer.writerows(lines)

    print(f"The first {n} lines have been saved in '{output_file}'.")




def combine_csv_files(input_files, output_file):
    # Initialize a list to store individual DataFrames
    dataframes = []
    
    # Load CSV files and add DataFrames to the list
    for file in input_files:
        data = pd.read_csv(file, delimiter=';', na_values=['Nuevo', 'N/A'], dtype={'Rating': float})
        
        dataframes.append(data)

    # Concatenate all DataFrames in the list using pandas.concat()
    combined_data = pd.concat(dataframes, ignore_index=True)

    # Sort the combined DataFrame by a specific column in alphabetical order
    combined_data_sorted = combined_data.sort_values(by='Restaurant ID', ascending=True)

    # Save the combined DataFrame with the new column to a new CSV file
    combined_data_sorted.to_csv(output_file, index=False, sep=';')



def keep_selected_csv_files(files_to_keep):
    current_directory = os.getcwd()  # Get the current directory where the script is executed
    files_in_directory = os.listdir(current_directory)  # Get the list of files in the directory
    
    # Filter CSV files in the list
    csv_files = [file for file in files_in_directory if file.endswith('.csv')]
    
    # Determine the CSV files to delete
    files_to_delete = [file for file in csv_files if file not in files_to_keep]
    
    # Delete CSV files that are not in the list of files to keep
    for file in files_to_delete:
        file_to_delete = os.path.join(current_directory, file)
        os.remove(file_to_delete)
        print(f"'{file}' was deleted successfully.")

