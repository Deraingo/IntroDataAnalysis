import praw
import pandas as pd
import os
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
from scipy.stats import pearsonr

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

# Reddit API credentials
redditClientId = ""
redditClientSecret = ""
redditUserAgent = ""

reddit = praw.Reddit(
    client_id=redditClientId,
    client_secret=redditClientSecret,
    user_agent=redditUserAgent,
)

def fetchRedditData(subredditName, searchQuery, limit=100, postType="submission", afterDate=None):
    data = []
    subreddit = reddit.subreddit(subredditName)
    if postType == "submission":
        results = subreddit.search(searchQuery, limit=limit)
    else:
        results = subreddit.comments(limit=limit)

    for item in results:
        if postType == "submission":
            postData = {
                "title": item.title,
                "selftext": item.selftext,
                "upvotes": item.score,
                "url": item.url,
                "createdUtc": item.created_utc,
            }
        else:
            postData = {
                "body": item.body,
                "upvotes": item.score,
                "createdUtc": item.created_utc,
                "submissionUrl": item.submission.url,
            }
        if afterDate is not None and postData["createdUtc"] < afterDate:
            continue

        data.append(postData)

    return pd.DataFrame(data)

def analyzeSentiment(text):
    sentiment = sia.polarity_scores(text)
    return sentiment["compound"]

outputDir = "reddit_output/pre_update"
os.makedirs(outputDir, exist_ok=True)
# Change date to look for date specific data i.e. look for data after date
afterDate = int(datetime(2024, 9, 27).timestamp())

subredditName = "thefinals"
searchQuery = "cl40 OR grenade launcher"
limit = 100
postType = "submission"


redditData = fetchRedditData(subredditName, searchQuery, limit, postType, afterDate)
redditData["sentimentScore"] = redditData["selftext"].fillna("").apply(analyzeSentiment)


redditData["textLength"] = redditData["selftext"].fillna("").apply(len) 
redditData["upvotes"] = redditData["upvotes"].fillna(0)


outputFile = os.path.join(outputDir, "pre_update_cl40_reddit_opinions.csv")
redditData.to_csv(outputFile, index=False)


correlation_upvotes, p_upvotes = pearsonr(redditData["upvotes"], redditData["sentimentScore"])
correlation_length, p_length = pearsonr(redditData["textLength"], redditData["sentimentScore"])

print(f"Correlation between Upvotes and Sentiment Score: {correlation_upvotes} (p-value: {p_upvotes})")
print(f"Correlation between Text Length and Sentiment Score: {correlation_length} (p-value: {p_length})")


plt.figure(figsize=(10, 6))
sns.scatterplot(x=redditData["upvotes"], y=redditData["sentimentScore"])
plt.title("Correlation Between Upvotes and Sentiment Score")
plt.xlabel("Upvotes")
plt.ylabel("Sentiment Score")
plt.savefig(os.path.join(outputDir, "cl40_correlation_upvotes_sentiment.png"))
plt.close()

plt.figure(figsize=(10, 6))
sns.scatterplot(x=redditData["textLength"], y=redditData["sentimentScore"])
plt.title("Correlation Between Text Length and Sentiment Score")
plt.xlabel("Text Length")
plt.ylabel("Sentiment Score")
plt.savefig(os.path.join(outputDir, "cl40_correlation_length_sentiment.png"))
plt.close()


correlation_matrix = redditData[["upvotes", "textLength", "sentimentScore"]].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix")
plt.savefig(os.path.join(outputDir, "cl40_correlation_matrix.png"))
plt.close()


plt.figure(figsize=(10, 6))
sns.histplot(redditData["sentimentScore"], kde=True, bins=20, color="blue", alpha=0.7)
plt.title("Histogram of Sentiment Scores")
plt.xlabel("Sentiment Score")
plt.ylabel("Frequency")
plt.savefig(os.path.join(outputDir, "pre_update_cl40_reddit_histogram.png"))
plt.close()


plt.figure(figsize=(8, 5))
sns.boxplot(y=redditData["sentimentScore"], color="cyan")
plt.title("Box Plot of Sentiment Scores")
plt.ylabel("Sentiment Score")
plt.savefig(os.path.join(outputDir, "pre_update_cl40_reddit_boxplot.png"))
plt.close()


textContent = " ".join(redditData["selftext"].fillna("").values)
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(textContent)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Reddit Posts")
plt.savefig(os.path.join(outputDir, "pre_update_cl40_reddit_cloud.png"))
plt.close()

print(f"All outputs saved to {outputDir}")
