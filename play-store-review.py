from google_play_scraper import app, reviews_all, Sort
import pandas as pd

# declare app id
app_id = 'com.miHoYo.GenshinImpact'

result = app(
    app_id,
    lang='en',
    country='us'
)

# get app title
print(result["title"])

ehorses_review_result = reviews_all(
    app_id,
    sleep_milliseconds=0,
    lang='en',
    country='us',
    sort=Sort.MOST_RELEVANT,
    filter_score_with=5
)

# Convert reviews to DataFrame
df = pd.DataFrame(ehorses_review_result)

# Reorder columns for better readability
columns_order = [
    'reviewId', 'content', 'score', 'userName', 
    'thumbsUpCount', 'reviewCreatedVersion', 'at', 
    'replyContent', 'repliedAt', 'appVersion'
]

# Select and reorder columns (only include columns that exist in the DataFrame)
existing_columns = [col for col in columns_order if col in df.columns]
df = df[existing_columns]

# Save to CSV
output_file = f"play_store_reviews_{app_id}.csv"
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"Total reviews: {len(ehorses_review_result)}")
print(f"Reviews saved to {output_file}")
