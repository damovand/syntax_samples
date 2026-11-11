import pandas as pd
import numpy as np
import requests

from pprint import pprint
import requests
from dotenv import load_dotenv
import os

# Example DataFrame
search_data = {
    'Title': ['12 Monkeys', 'About A Boy', 'Casanova', 'Corner Office'],
    'Released_Year': [np.nan, np.nan, np.nan, np.nan],
}
df = pd.DataFrame(search_data)

OMDB_expected_fields = ["Title", "Year", "Genre", "Director", "Actors", "imdbRating"]
# API endpoint (replace with your actual API URL)
API_URL = "http://www.omdbapi.com/"
load_dotenv()

api_key = '3dfc9c89'

# Function to test OMDb API response
def omdb_movie_details(movie_title):
    """
    Calls the OMDb API for a given movie title and validates the returned data.
    """
    base_url = "http://www.omdbapi.com/"
    params = {
        "t": movie_title,  # Search by title
        "apikey": api_key
    }

    try:
        # Make the API request
        response = requests.get(base_url, params=params, timeout=5)

        # Check HTTP status
        if response.status_code != 200:
            print(f"❌ HTTP Error: {response.status_code}")
            return False

        # Parse JSON
        data = response.json()
        #print(" Returned DAta from API ", data)
        # Check if API returned an error
        if data.get("Response") == "False":
            print(f"❌ API Error: {data.get('Error')}")
            return False

        # Validate expected fields
        #OMDB_expected_fields = ["Title", "Year", "Genre", "Director", "Actors", "imdbRating"]
        missing_fields = [field for field in OMDB_expected_fields if field not in data]

        if missing_fields:
            print(f"❌ Missing fields in response: {missing_fields}")
            return False

        # Print validated data
        print("✅ API call successful and data validated:")
        key_to_check = "Title"
        omdb_title = data.get(key_to_check)

        for field in OMDB_expected_fields:
           print(f"{field}: {data[field]}")
        # Populate dictionary based on JSON type
        
        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False


# Iterate over rows where 'name' is NaN
for idx, row in df[df['Released_Year'].isna()].iterrows():
    Movie_title = df.at[idx, 'Title']
    print (" ===== Look For: ",idx, "  ", Movie_title)
    
    new_value = omdb_movie_details(Movie_title)
    
    if new_value:
        print(" ==== Done ===")  
        #movie_detail_array[idx] = movie_dict
    else:
        print(f"No value retrieved for ID {row['Title']}")
    
# Final DataFrame

print("\nDetails from OMDB:")
print(movie_dict)
