# App Review Scraper

## Repository

https://github.com/RayVec/Review-Scraper/blob/main/README.md

## Challenges

The key challenges lie on 

1. How to bypass the anti-scraper limitation google play store and apple app store, where apple’s restriction is much higher, preventing third-party to get more than 500 reviews.
2. How to fetch reviews through a designated time range

## Confirm app id

For targeting apps, see

![image.png](https://file.notion.so/f/f/2d35a5b3-e1b9-4ef8-a9b5-ec820e6f3435/3461afdf-d142-4156-9c30-df9b650ef5ff/image.png?table=block&id=199cac4b-856f-80f3-8c85-ce8565e39355&spaceId=2d35a5b3-e1b9-4ef8-a9b5-ec820e6f3435&expirationTimestamp=1739491200000&signature=yMCF5mdULdyqbWEe-8DdVMDTnQ_v-Cr-5vjo84DxeSI&downloadName=image.png)

the “id=xxxxxx” in the browser address when visiting this app on google play store web page

![image.png](attachment:522197f8-ea6f-480c-ae78-f51bb938509a:image.png)

About apple app store, see “idxxxxxxx” for the id xxxxxxxx in the browser address either.

Let’s take Wysa for instance, the app id is bot.touchkin for google play store and 1166585565 for apple store

## Google play store scraper

Considering google play store has las regulation, google_play_scraper library can be utilized for large bulk review fetching, 

https://github.com/facundoolano/google-play-scraper

it can fetch more than 80,000 reviews through the [play-store-review.py](http://play-store-review.py) script.

In [play-store-review.py](http://play-store-review.py) script:

- Setup & Configuration
    - Imports required libraries (google_play_scraper and pandas)
    - Defines the app ID for Genshin Impact
- App Information
    - Fetches basic app information using app()
    - Prints the app title
- Review Collection
    - Uses reviews_all() to fetch all reviews
    - Parameters set for English language and US region
    - Reviews are sorted by most relevant
- Data Processing
    - Converts the reviews into a pandas DataFrame
    - Organizes the data with specific columns:
        - Review ID, content, score
        - User information
        - Timestamps
        - Reply information
        - App version details
- Data Export into a CSV file

The script should run for a while for large data, refer to play_store_reviews_com.miHoYo.GenshinImpact.csv  for the example output csv file.

## One stop solution

Because of the difficulty to scrape large amount of reviews of apple app store, third-party services could be a better way. They monitored both google and apple app store constantly, thus having the same data as the officials, and they also provided API for access supporting time range.

Appfolow is applied to the current project, but other services are welcome to have a try

[Understand and elevate your app’s reputation](https://appfollow.io/)

### Register an account

After registering, every user can get free 1000 credit for 100 times api usage, we can register for multiple accounts for more usage.

### Get api TOKEN from account dashboard

https://watch.appfollow.io/apps/my-first-workspace/api

![image.png](attachment:4f7a88d9-439c-4d48-8b3f-c5969eca20ac:image.png)

### Apply the TOKEN in the script

In both-store-review.py,

1. Imports essential libraries for HTTP requests, date handling, JSON processing, and data manipulation with pandas
2. Establishes configuration parameters including API authentication token, target app id, region settings, and specific date range for review collection
    1. if using apple store app id, it will fetch reviews from apple store, same for google play, quite simple.
3. Constructs metadata URL and sends API request to AppFollow to retrieve app version information with proper authentication headers (can be dismissed if just wanting review data)
4. Builds reviews URL with date parameters and makes second API request to fetch all reviews within the specified timeframe
5. Validates API response status (200) to ensure successful data retrieval from AppFollow servers
6. Processes JSON response by extracting the reviews list from the nested data structure
7. Transforms raw review data into structured pandas DataFrame for easier manipulation and analysis
8. Exports processed review data to CSV format
9. Provides execution feedback through status messages for both successful export and error conditions

See the reviews_app_1166585565_2021-01-01_to_2021-02-01.csv file for example output.
