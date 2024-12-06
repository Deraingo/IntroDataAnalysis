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
redditClientId = "lwmk70nQqTOAST36Z_g11g"
redditClientSecret = "sNySe0wpiHmlDDevTJxJPt98x85eGw"
redditUserAgent = "windows:finalsDataScrape2.0:v1.0 (by /u/Deraingo)"

weaponName = "pike"
# post_update or pre_update
updateVersion = "pre_update"
afterDate = None
beforeDate = None
# Set date to filter posts after a specific timestamp
if updateVersion == "post_update":
    afterDate = int(datetime(2024, 10, 10).timestamp())
    beforeDate = int(datetime(2024, 12, 5).timestamp())
else:
    updateVersion = "pre_update"
    afterDate = int(datetime(2024, 9, 27).timestamp())
    beforeDate = int(datetime(2024, 10, 10).timestamp())
outputDir = f"reddit_output/{updateVersion}/{weaponName}"

reddit = praw.Reddit(
    client_id=redditClientId,
    client_secret=redditClientSecret,
    user_agent=redditUserAgent,
)

def filterTextByKeywords(text, keywords):
    """Keep text containing at least one of the specified keywords."""
    return any(keyword.lower() in text.lower() for keyword in keywords)

keywords = [
    "weapon", "damage", "gun", "firearm", "balancing", "accuracy",
    "reload", "ammo", f"{weaponName}", "nerf", "buff", "increase", "skill",
    "high", "strategy", "medium", "overpowered", "one hit", "good", "bad", "decent",
    "rate", "fire", "fire rate", "rof", "casual", "fun"
]

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
        if afterDate is not None and postData["createdUtc"] < afterDate and beforeDate is not None and beforeDate > postData["createdUtc"]:
            continue

        data.append(postData)

    return pd.DataFrame(data)

def analyzeSentiment(text):
    sentiment = sia.polarity_scores(text)
    return sentiment["compound"]

os.makedirs(outputDir, exist_ok=True)




subredditName = "thefinals"
searchQuery = f"{weaponName}"
limit = 100
postType = "submission"


redditData = fetchRedditData(subredditName, searchQuery, limit, postType, afterDate)

redditData = redditData[
    redditData["selftext"].fillna("").apply(lambda x: filterTextByKeywords(x, keywords)) |
    redditData["title"].fillna("").apply(lambda x: filterTextByKeywords(x, keywords))
]

redditData["sentimentScore"] = redditData["selftext"].fillna("").apply(analyzeSentiment)

redditData["textLength"] = redditData["selftext"].fillna("").apply(len)
redditData["upvotes"] = redditData["upvotes"].fillna(0)

outputFile = os.path.join(outputDir, f"{updateVersion}_{weaponName}_reddit_opinions_filtered.csv")
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
plt.savefig(os.path.join(outputDir, f"{updateVersion}_{weaponName}_correlation_upvotes_sentiment.png"))
plt.close()

plt.figure(figsize=(10, 6))
sns.scatterplot(x=redditData["textLength"], y=redditData["sentimentScore"])
plt.title("Correlation Between Text Length and Sentiment Score")
plt.xlabel("Text Length")
plt.ylabel("Sentiment Score")
plt.savefig(os.path.join(outputDir, f"{updateVersion}_{weaponName}_correlation_length_sentiment.png"))
plt.close()

correlationMatrix = redditData[["upvotes", "textLength", "sentimentScore"]].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlationMatrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix")
plt.savefig(os.path.join(outputDir, f"{updateVersion}_{weaponName}_correlation_matrix.png"))
plt.close()

plt.figure(figsize=(10, 6))
sns.histplot(redditData["sentimentScore"], kde=True, bins=20, color="blue", alpha=0.7)
plt.title("Histogram of Sentiment Scores")
plt.xlabel("Sentiment Score")
plt.ylabel("Frequency")
plt.savefig(os.path.join(outputDir, f"{updateVersion}_{weaponName}_reddit_histogram.png"))
plt.close()

plt.figure(figsize=(8, 5))
sns.boxplot(y=redditData["sentimentScore"], color="cyan")
plt.title("Box Plot of Sentiment Scores")
plt.ylabel("Sentiment Score")
plt.savefig(os.path.join(outputDir, f"{updateVersion}_{weaponName}_reddit_boxplot.png"))
plt.close()

textContent = " ".join(redditData["selftext"].fillna("").values)
filteredWordcloud = WordCloud(
    width=800, height=400, background_color="white"
).generate(textContent)
plt.figure(figsize=(10, 6))
plt.imshow(filteredWordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Filtered Reddit Posts")
plt.savefig(os.path.join(outputDir, f"{updateVersion}_{weaponName}_reddit_cloud_filtered.png"))
plt.close()

print(f"Filtered outputs saved to {outputDir}")

overall_sentiment_score = redditData["sentimentScore"].mean()

print(f"Overall Sentiment Score for '{weaponName}' posts: {overall_sentiment_score}")
