import requests
import json

def fetch_and_save_countries_data():
    # Endpoint URL with filtered fields for name, flags, continent, and languages
    url = 'https://restcountries.com/v3.1/all?fields=name,flags,continent,languages'
    
    try:
        # Attempt to fetch data from the REST Countries API
        response = requests.get(url)
        
        # If the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Convert the response text (JSON format) into a Python dictionary
            data = response.json()
            
            # Serialize data to a JSON formatted string with indentation for readability
            pretty_data = json.dumps(data, indent=4)
            
            # Initialize an empty list to store combined data of all countries
            combined_data = []
            
            # Process each country data
            for country_data in data:
                # Get continent and primary language
                continent = get_continent(country_data)
                primary_language = get_primary_language(country_data)
                
                # Add continent and primary language to the country data
                country_data['continent'] = continent
                
                # Append the updated country data to the combined data list
                combined_data.append(country_data)
            
            # Save the combined data to a JSON file
            with open("countries.json", "w") as file:
                json.dump(combined_data, file, indent=4)
                
            print("Data fetched and saved successfully.")
        else:
            # If the request was not successful, print the status code
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    
    except requests.RequestException as e:
        # Catch any errors during the HTTP request (e.g., network issues)
        print(f"Error fetching data: {e}")

def get_continent(country_data):
    return country_data.get('continent')



