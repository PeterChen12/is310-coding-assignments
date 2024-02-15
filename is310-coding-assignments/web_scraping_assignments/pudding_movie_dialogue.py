import requests
from bs4 import BeautifulSoup
import csv

#read original CSV
with open('cleaned_pudding_data.csv', mode='r', newline='', encoding='utf-8') as inputFile:
    reader = csv.DictReader(inputFile)
    
    #open output CSV file
    with open('pudding_movie_dialogue.csv', mode='w', newline='', encoding='utf-8') as outputFile:
        output_fieldnames = reader.fieldnames + ['script_sample']
        writer = csv.DictWriter(outputFile, fieldnames = output_fieldnames)
    # Write the headers
        writer.writeheader()
    
    #loop through original CSV
        for row in reader:
            script_url = row['link']
            response = requests.get(script_url)
            soup = BeautifulSoup(response.text, "html.parser")
            script_text = soup.get_text()[:1000]

            row['script_sample'] = script_text
            writer.writerow(row)

print ("complete")