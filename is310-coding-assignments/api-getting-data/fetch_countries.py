import requests
import json

def fetch_and_save_countries_data():
    # Endpoint URL with filtered fields for name and flags
    url = 'https://restcountries.com/v3.1/all?fields=name,flags'
    
    try:
        # Attempt to fetch data from the REST Countries API
        response = requests.get(url)
        
        # If the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Convert the response text (JSON format) into a Python dictionary
            data = response.json()
            
            # Serialize data to a JSON formatted string with indentation for readability
            pretty_data = json.dumps(data, indent=4)
            
            # Print the formatted data to the console
            print(pretty_data)
            
            # Save the formatted data to a JSON file
            with open("countries.json", "w") as file:
                file.write(pretty_data)
                
            print("Data fetched and saved successfully.")
        else:
            # If the request was not successful, print the status code
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    
    except requests.RequestException as e:
        # Catch any errors during the HTTP request (e.g., network issues)
        print(f"Error fetching data: {e}")

# Execute the function
fetch_and_save_countries_data()
