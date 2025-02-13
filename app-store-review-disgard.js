// this script doesn't work so well

import { AppStoreClient, Collection, Country } from "app-store-client";

const client = new AppStoreClient();

const appId = "1517783697";

// Use ID
const reviews = await client.reviews({ id: appId, country: Country.US });

const appData = await client.app({ id: appId });

console.log(appData);

// Or use app ID (bundle ID)
// const reviews = await client.reviews({ appId: "com.burbn.barcelona" });

console.log(reviews.length);

// console.log(reviews);
// [
//   {
//     "id": "12012163673",
//     "userName": "Moms deepen",
//     "userUrl": "https://itunes.apple.com/us/reviews/id1727492095",
//     "version": "359.1",
//     "score": 5,
//     "title": "So lucky",
//     "text": "When u home",
//     "url": "https://itunes.apple.com/us/review?id=6446901002&type=Purple%20Software",
//     "updated": "2024-11-30T22:47:31-07:00"
//   },
//   // ... more reviews
// ]
