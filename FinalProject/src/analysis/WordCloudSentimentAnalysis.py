import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import seaborn as sns
import nltk
import os

nltk.download('vader_lexicon')
outputDir = "output"
os.makedirs(outputDir, exist_ok=True)

def filterOpinionsByKeywords(opinions, keywords):
    filteredOpinions = opinions[opinions.str.contains('|'.join(keywords), case=False, na=False)]
    return filteredOpinions

def generateWordCloud(text, title, savePath):
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title, fontsize=16)
    plt.axis("off")
    plt.savefig(savePath, format='png')
    plt.close()

def analyzeSentiment(opinions):
    """Analyzes sentiment and returns a DataFrame with scores."""
    sia = SentimentIntensityAnalyzer()
    sentiments = []

    for opinion in opinions:
        if isinstance(opinion, str):
            sentimentScore = sia.polarity_scores(opinion)
            sentiments.append(sentimentScore)
        else:
            sentiments.append({'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0})

    return pd.DataFrame(sentiments)

def main():
    opinionsDf = pd.read_csv('../output/post_update_opinions_pike.csv')
    keywords = ['weapon', 'damage', 'gun', 'firearm', 'balancing', 'accuracy', 'reload', 'ammo', 'pike', 'nerf', 'medium', 'light', 'over powered', 'one hit']
    print("Filtering opinions...")

    filteredOpinions = filterOpinionsByKeywords(opinionsDf['Opinions'], keywords)
    filteredCsvPath = os.path.join(outputDir, "post_update_opinions_pike.csv")
    filteredOpinions.to_csv(filteredCsvPath, index=False, header=True)

    print(f"Filtered opinions saved to {filteredCsvPath}")

    allFilteredText = " ".join(filteredOpinions.dropna())

    print("Generating word cloud for filtered opinions...")

    wordcloudPath = os.path.join(outputDir, "post_update_pike_word_cloud.png")
    generateWordCloud(allFilteredText, title="Word Cloud of Weapon-Related Opinions", savePath=wordcloudPath)

    print(f"Word cloud saved to {wordcloudPath}")
    print("Analyzing sentiment for filtered opinions...")

    sentimentDf = analyzeSentiment(filteredOpinions)
    filteredOpinionsDf = pd.concat([filteredOpinions.reset_index(drop=True), sentimentDf], axis=1)

    compound_skewness = filteredOpinionsDf['compound'].skew()
    print(f"Skewness of compound sentiment scores: {compound_skewness}")

    sentimentDf = analyzeSentiment(filteredOpinions)
    filteredOpinionsDf = pd.concat([filteredOpinions.reset_index(drop=True), sentimentDf], axis=1)
    histPath = os.path.join(outputDir, "post_update_pike_sentiment_histogram.png")
    plt.figure(figsize=(10, 6))
    sns.histplot(data=filteredOpinionsDf, x="compound", bins=20, kde=True, color='blue')
    plt.title("Sentiment Distribution (Compound Scores) - Weapon Opinions")
    plt.xlabel("Compound Sentiment Score")
    plt.ylabel("Frequency")
    plt.savefig(histPath, format='png')
    plt.close()
    print(f"Sentiment histogram saved to {histPath}")

    boxplotPath = os.path.join(outputDir, "post_update_pike_sentiment_boxplot.png")
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=filteredOpinionsDf[['neg', 'neu', 'pos']])
    plt.title("Sentiment Score Distribution (Negative, Neutral, Positive) - Weapon Opinions")
    plt.ylabel("Score")
    plt.savefig(boxplotPath, format='png')
    plt.close()
    print(f"Sentiment boxplot saved to {boxplotPath}")

if __name__ == "__main__":
    main()
