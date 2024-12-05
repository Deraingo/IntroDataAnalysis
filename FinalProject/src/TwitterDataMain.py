import tweepy
import pandas as pd
from datetime import datetime, timedelta
import time
bearerToken = ""
client = tweepy.Client(bearer_token=bearerToken)

def fetchTweetsV2(keyword, startDate, endDate, tweetsPerWeek=10):
    tweets = []
    currentDate = endDate

    while currentDate > startDate:
        weekStart = currentDate - timedelta(days=7)
        weekEnd = currentDate

        print(f"Fetching tweets from {weekStart.date()} to {weekEnd.date()}...")
        query = f'"{keyword}" (weapon OR gun) (buff OR buffed OR buffing OR nerf OR nerfed OR nerfing) lang:en'

        startTime = weekStart.isoformat("T") + "Z"
        endTime = weekEnd.isoformat("T") + "Z"
        response = client.search_recent_tweets(
            query=query,
            start_time=startTime,
            end_time=endTime,
            max_results=tweetsPerWeek,
            tweet_fields=["created_at", "text", "author_id", "public_metrics"]
        )

        if response.data:
            for tweet in response.data:
                tweets.append({
                    "date": tweet.created_at,
                    "user_id": tweet.author_id,
                    "text": tweet.text,
                    "likes": tweet.public_metrics["like_count"],
                    "retweets": tweet.public_metrics["retweet_count"]
                })

        currentDate = weekStart
        time.sleep(3)

    return tweets

def saveTweetsToCsv(tweets, fileName):
    df = pd.DataFrame(tweets)
    df.to_csv(fileName, index=False)
    print(f"Saved {len(tweets)} tweets to {fileName}")

def main():
    keyword = "The Finals"
    startDate = datetime(2023, 1, 1)
    endDate = datetime.now()
    tweetsPerWeek = 10
    outputFileName = "weaponOpinions.csv"
    print("Starting tweet fetch...")
    tweets = fetchTweetsV2(keyword, startDate, endDate, tweetsPerWeek)
    saveTweetsToCsv(tweets, outputFileName)

if __name__ == "__main__":
    main()
