import requests
from datetime import datetime
import json
import pandas as pd

# Adjustable parameters
api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGl2MiIsInN1YiI6MjMyMzU0LCJqdGkiOjYyMTIyLCJzY29wZXMiOiJkcncifQ.D6bcxzi5pd9aLTctJWiCNfn-gfM27YL8q1obgM81qTk"
ext_id = "bot.touchkin"  # App ID example, for the app Wysa, apple store id is 1594474215, and google play store id is  bot.touchkin
country = "us"         # Country code
start_date = "2021-01-01"  # Format: YYYY-MM-DD
end_date = "2021-02-01"    # Format: YYYY-MM-DD

# get app metadata
metadata_url = f"https://api.appfollow.io/api/v2/meta/versions?ext_id={ext_id}&country={country}"

headers = {
    "accept": "application/json",
    "X-AppFollow-API-Token": api_token
}

response = requests.get(metadata_url, headers=headers)
print("Metadata response:", response.status_code)

# get app reviews
reviews_url = f"https://api.appfollow.io/api/v2/reviews?ext_id={ext_id}&from={start_date}&to={end_date}"
response = requests.get(reviews_url, headers=headers)
print("Reviews response:", response.status_code)

if response.status_code == 200:
    data = response.json()
    reviews = data['reviews']['list']
    
    # Convert reviews to DataFrame
    df = pd.DataFrame(reviews)
    
    # Reorder columns for better readability
    columns_order = [
        'review_id', 'date', 'time', 'rating', 'title', 'content',
        'author', 'user_id', 'country', 'lang_detect', 'app_version',
        'store', 'created', 'updated', 'is_deleted', 'was_changed',
        'has_answer', 'answer_text', 'answer_date', 'answer_time',
        'thumbs_up_cnt', 'thumbs_down_cnt', 'internal_id'
    ]
    
    # Select and reorder columns (only include columns that exist in the DataFrame)
    existing_columns = [col for col in columns_order if col in df.columns]
    df = df[existing_columns]
    
    # Save to CSV
    output_file = f"reviews_app_{ext_id}_{start_date}_to_{end_date}.csv"
    df.to_csv(output_file, index=False, encoding='utf-8-sig')  # utf-8-sig for Excel compatibility
    
    print(f"Reviews saved to {output_file}")
else:
    print(f"Error fetching reviews: {response.status_code}")

