import os
import csv
import tkinter as tk
from tkinter import filedialog
import re

def replace_problematic_bytes(text):
    """ Replaces problematic byte sequences with the correct UTF-8 characters """
    replacements = {
        '\x81': 'ü',
        '\x84': 'ä',
        '\x94': 'ö',
        '\xE1': 'ß',
    }
    
    for byte_seq, replacement in replacements.items():
        text = text.replace(byte_seq, replacement)
    
    return text

def replace_consecutive_spaces(text):
    """ Replaces more than two consecutive spaces with an HTML <br> tag """
    return re.sub(r'\s{3,}', '<br>', text)

def open_file_dialog(title):
    """ Opens a file dialog window and returns the path to the selected file """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title=title)
    return file_path

def read_product_numbers_from_csv(file_path):
    """ Reads product numbers from the first column of the CSV file and stores them in a set """
    product_numbers = set()
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            product_number = row[0].lstrip('0')  # Remove leading zeros
            product_numbers.add(product_number)
    return product_numbers

def process_imp_file(imp_file_path, product_numbers, output_file_path):
    """ Processes the .imp file and writes matching product descriptions to a new CSV file """
    with open(imp_file_path, 'r', encoding='latin1', errors='replace') as imp_file, \
            open(output_file_path, 'w', newline='', encoding='utf-16') as output_csv:
        
        writer = csv.writer(output_csv)
        writer.writerow(['Product Number', 'Description'])  # Header
        
        for line in imp_file:
            lang = line[1:4].strip().lstrip('0')
            product_number = line[5:22].strip().lstrip('0')  # Extract the product number, remove leading zeros
            if lang == "1" and product_number in product_numbers:
                description = line[22:3745].strip()  # Extract the description
                description = replace_problematic_bytes(description)
                description = replace_consecutive_spaces(description)
                writer.writerow([product_number, description])  # Write to the CSV file

def main():
    # Step 1: Prompt user to select a CSV file with product numbers
    csv_file_path = open_file_dialog("Please select the CSV file with product numbers:")
    
    # Step 2: Read product numbers from the CSV file
    product_numbers = read_product_numbers_from_csv(csv_file_path)
    
    # Step 3: Get the current user's Desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    output_file_path = os.path.join(desktop_path, 'Product_Descriptions.csv')
    
    # Step 4: Prompt user to select the IMP file
    imp_file_path = open_file_dialog("Please select the IMP file with product data:")
    
    # Step 5: Process the IMP file and write results to the new CSV file
    process_imp_file(imp_file_path, product_numbers, output_file_path)
    
    print(f'The new file has been saved to the Desktop as "Product_Descriptions.csv".')

if __name__ == '__main__':
    main()
