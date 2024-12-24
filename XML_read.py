import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import csv
import os

try:
    tree = ET.parse('CDAM-2721.xml')  # Replace 'data.xml' with the path to your XML file
    root = tree.getroot()
except FileNotFoundError:
    print("Error: The file 'data.xml' was not found.")
    exit(1)  # Exit the program with an error code


data = []
for item in root.findall('item'):   
    key = item.find('Key').text
    status = item.find('Status').text
    data.append({'Key':key, 'Status':status})


for entry in data:
    print(f"Key: {entry['Key']} -> Status: {entry['Status']}")

with open('status.csv', 'w', newline='') as csvfile:
    fieldnames = ['Key', 'Status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header
    writer.writeheader()
    
    # Write rows
    writer.writerows(data)

print("Data written to output.csv")



