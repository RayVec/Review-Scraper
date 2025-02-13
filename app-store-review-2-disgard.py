# this script doesn't work well


import os
import csv
import json
import time
import random
import requests
import warnings

warnings.filterwarnings("ignore", category=Warning)

next_url = None

review_path = 'reviews'
if not os.path.exists(review_path):
    os.mkdir(review_path)

# Direct configuration
config = {
    "max_page": 5,
    "ids": ["414478124"],
    "headers": {
        "User-Agent": "你自己的",
        "Authorization": "你自己的"
    },
    "intervals": [1, 2]  # Changed to list for random.uniform()
}

pending_queue = config['ids']
max_page = config['max_page']
headers = config['headers']
intervals = config['intervals']

# Send request to get the response
def get_response(app_id, page):
    time.sleep(random.uniform(intervals[0], intervals[1]))  # Randomized delay
    try:
        url = 'https://amp-api.apps.apple.com/v1/catalog/cn/apps/' + app_id + '/reviews?l=zh-Hans-CN&offset=' + str(page * 10) + '&platform=web&additionalPlatforms=appletv%2Cipad%2Ciphone%2Cmac'
        r = requests.get(url, headers=headers)
        
        if r.status_code == 429:  # Rate limit exceeded
            print("Rate limit exceeded. Retrying in 60 seconds...")
            time.sleep(60)  # Wait for 60 seconds
            return get_response(app_id, page)  # Retry

        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return None

# Parse response to extract review data
def parse_response(r):
    global next_url
    if "next" in r.keys():
        next_url = r['next']
    else:
        next_url = None

    for item in r['data']:
        yield {
            "id": item['id'],
            "type": item['type'],
            "title": item['attributes']['title'],
            "userName": item['attributes']['userName'],
            "isEdited": item['attributes']['isEdited'],
            "review": item['attributes']['review'],
            "rating": item['attributes']['rating'],
            "date":  item['attributes']['date']
        }

# Write review data to CSV
def write_to_file(app_id, item):
    with open(f'{review_path}/{app_id}.csv', 'a', encoding='utf-8-sig', newline='') as csv_file:
        fieldnames = ['id', 'type', 'title', 'userName', 'isEdited', 'review', 'rating', 'date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow(item)

# Main function to handle review fetching
def main():
    while len(pending_queue):
        cur_id = pending_queue.pop()
        print(f'开始爬取 {cur_id}')
        for i in range(0, max_page):
            r = get_response(cur_id, i)
            if r is None:  # Skip iteration if there is no response
                continue
            print(f"第 {i+1} 页评论已获取")
            for item in parse_response(r):
                write_to_file(cur_id, item)
            print(f'第 {i} 页评论已存储')
            if not next_url:
                break
        print(f'结束爬取 {cur_id}')

if __name__ == '__main__':
    main()
