import os
import xml.etree.ElementTree as ET
import csv
import re
import json


def process_xml_file(file_name, data):
    """
    Parses an XML file, extracts 'Key' and 'Status' data, and appends it to the data list.
    If a child XML file is referenced, the function calls itself recursively.
    """
    
    file_path = os.path.join(folder_path, file_name)
    print(f"Processing XML file: {file_path}")
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return
    except ET.ParseError:
        print(f"Error: Failed to parse the file '{file_path}'.")
        return

    for item in root.findall('item'):
        key = item.find('Key').text if item.find('Key') is not None else "Unknown"
        status = item.find('Status').text if item.find('Status') is not None else "Unknown"
        title = item.find('title').text if item.find('title') is not None else "No Title"
        clean_title  = re.sub(r'\[.*?\]','',title).strip() 
        parent = item.find('parent').text if item.find('parent') is not None else ""
        parent_title = ""
        parent_status = ""
        
        if parent != "":
            parent_file_name = parent + '.xml'
            parent_data = []
            process_xml_file(parent_file_name, parent_data)
            for i in parent_data:
                parent_obj = parent_data.pop(0)
                print('This is a obj from the data: ',parent_obj)
                parent_title =parent_obj['Title']
                parent_status = parent_obj['Status']
           
        data.append({
            'Key': key, 
            'Status': status,
            'Title': clean_title,
            'Parent': parent,
            'parent_title': parent_title,
            'parent_Status': parent_status
            })
        

def process_all_xml_files_in_folder(folder_path, output_csv):
    """
    Processes all XML files in the specified folder, extracts data, and writes it to a CSV file.
    """
    data = []
    files = []
    
    # Iterate through files in the folder
    for file_name in os.listdir(folder_path):
        print('file name is: ',file_name)
        if file_name.endswith('.xml'):
            process_xml_file(file_name, data)

    # Write data to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Key', 'Status','Title','Parent','parent_title','parent_Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()
        
        # Write rows
        writer.writerows(data)

    print(f"Data written to {output_csv}")

# Example Usage
folder_path = r'C:\Users\Aryan Mhatre\Python'  # Replace with the folder containing your XML files
output_csv = 'status.csv'
process_all_xml_files_in_folder(folder_path, output_csv)
