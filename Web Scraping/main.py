
from data_plain_extract_JE import *
from data_deep_extract_JE import ubication_and_menu_JE
from data_plain_extract_Glovo import scrape_and_save_data_Glovo
from data_deep_extract_Glovo import ubication_and_menu_Glovo, try_complete_coordinates
from data_enrichment import process_file, words_to_codes, process_file, add_PK_dish
from clean_functions import remove_duplicates_csv, clean_csv_file, remove_rows_with_null_lat_long, filter_by_ids
from other_test_functions import extract_first_n_lines, keep_selected_csv_files, combine_csv_files

#Just Eat Variables
# Test Zipcodes
#zip_codes = ['28037', '28038', '28039', '28040', '28041', '28042', '28043', '28044', '28045', '28046', '28047', '28048', '28049', '28050', '28051', '28052', '28053', '28054', '28055']
#zip_codes = ['28001', '28002', '28003', '28004', '28005', '28006', '28007', '28008', '28009', '28010', '28011', '28012', '28013', '28014', '28015', '28016', '28017', '28018']
#zip_codes = ['28001', '28002']
#zip_codes = ['28055','28054']
#All Madrid zip codes, except those unique to TV1, TV2, Antena 3, Correos, etc.
zip_codes = ['28001', '28002', '28003', '28004', '28005', '28006', '28007', '28008', '28009', '28010', '28011', '28012', '28013', '28014', '28015', '28016', '28017', '28018','28019', '28020', '28021', '28022', '28023', '28024', '28025', '28026', '28027', '28028', '28029', '28030', '28031', '28032', '28033', '28034', '28035', '28036','28037', '28038', '28039', '28040', '28041', '28042', '28043', '28044', '28045', '28046', '28047', '28048', '28049', '28050', '28051', '28052', '28053', '28054', '28055']
input_file = 'Restaurants_JE_Phase1.csv'
output_file = 'Restaurants_JE_Phase1.csv'
restaurants_JE_output_1 = 'Restaurants_JE_Phase2.csv'
products_JE_output = 'Products_JE_Phase1.csv'

#Just Eat scrap functions
scrape_and_save_data_JE(zip_codes,output_file)
remove_duplicates_csv(input_file, output_file)
#test
#extract_first_n_lines(input_file, output_file)
ubication_and_menu_JE(input_file, restaurants_JE_output_1, products_JE_output)

#Glovo variables
base_url = 'https://glovoapp.com/es/es/madrid/restaurantes_1/?page='
output_file = 'Restaurants_Glovo_Phase1.csv'
input_file = 'Restaurants_Glovo_Phase1.csv'
output_file1 = "Restaurants_Glovo_Phase2.csv"
products_Glovo_output = "Products_Glovo_Phase1.csv"
restaurants_Glovo_output1 = "Restaurants_Glovo_Phase3.csv"

#Glovo scrap functions
#Basic extract
scrape_and_save_data_Glovo(base_url, output_file)
#Restaurant info
ubication_and_menu_Glovo(input_file, output_file1, products_Glovo_output)
#Some modifications that try to standardize some addresses to get more results.
try_complete_coordinates(output_file1, restaurants_Glovo_output1)

#Common variables
input_files_restaurants = [restaurants_Glovo_output1,restaurants_JE_output_1]
input_files_products = [products_Glovo_output,products_JE_output]
restaurants_output1 = 'Restaurants2.csv'
restaurants_output2 = 'Restaurants3.csv'
restaurants_output3 = 'Restaurants.csv'
products_output = 'Products1.csv'
products_output2 = 'Products2.csv'
products_output3 = 'Products3.csv'
products_output4 = 'Products4.csv'
products_output5 = 'Products.csv'

#Append
combine_csv_files(input_files_restaurants,restaurants_output1)
combine_csv_files(input_files_products,products_output)

#Clean
#We only clean 'products' as 'restaurants' does not have fields susceptible to errors.
clean_csv_file(products_output,products_output2)


#delete restaurantes wich not have latitude/longitude (critical data)
remove_rows_with_null_lat_long(restaurants_output1, restaurants_output2)

#As the number of restaurants has reduced, the number of available products should also be reduced
filter_by_ids(products_output2,products_output3,restaurants_output2)


#Enrichment
#clasiffy 
process_file(products_output3,products_output4)
#dish PK generator
filter_by_ids(restaurants_output2, restaurants_output3, products_output4)
add_PK_dish(products_output4,products_output5)
#DANGER: IT WILL DELETE ALL THE CSV FILES EXCEPT THE LAST ONES (ready to upload files).
files_to_keep = [restaurants_output3, products_output5]
keep_selected_csv_files(files_to_keep)

