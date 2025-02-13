import requests
import json

# Function to fetch app reviews from Apple App Store
def fetch_app_reviews(app_id, country="us", max_pages=3):
    base_url = f"https://itunes.apple.com/{country}/rss/customerreviews/page={{}}/id={app_id}/sortby=mostrecent/json"
    all_reviews = []

    for page in range(1, max_pages + 1):
        url = base_url.format(page)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if "feed" in data and "entry" in data["feed"]:
                reviews = data["feed"]["entry"]
                if isinstance(reviews, list):
                    for review in reviews:
                        if "im:rating" in review and "content" in review:
                            all_reviews.append({
                                "rating": review["im:rating"]["label"],
                                "title": review["title"]["label"],
                                "author": review["author"]["name"]["label"],
                                "content": review["content"]["label"],
                                "date": review["updated"]["label"]
                            })
            else:
                print(f"No more reviews found on page {page}.")
                break
        else:
            print(f"Failed to fetch page {page}: {response.status_code}")
            break

    return all_reviews

# Example Usage: Fetch reviews for Instagram (App ID: 389801252)
app_id = "389801252"  # Replace with your desired app's ID
reviews = fetch_app_reviews(app_id, max_pages=10)

# Print fetched reviews
for i, review in enumerate(reviews[:10]):  # Display first 10 reviews
    print(f"{i+1}. ⭐ {review['rating']} - {review['title']} by {review['author']}")
    print(f"   {review['content']}")
    print(f"   [Date: {review['date']}]\n")
