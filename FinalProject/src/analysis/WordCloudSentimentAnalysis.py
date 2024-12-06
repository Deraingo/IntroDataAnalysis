import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import seaborn as sns
import nltk
import os

nltk.download('vader_lexicon')

weaponName = "cl40"
# post_update or pre_update
updateVersion = "pre_update"
outputDir = f"output/{updateVersion}"
os.makedirs(outputDir, exist_ok=True)

def filterOpinionsByKeywords(opinions, keywords):
    filteredOpinions = opinions[opinions.str.contains('|'.join(keywords), case=False, na=False)]
    return filteredOpinions

def generateWordCloud(text, title, savePath, extraStopwords=None):
    stopwords = set(STOPWORDS)
    if extraStopwords:
        stopwords.update(extraStopwords)
    wordcloud = WordCloud(
        width=800, height=400, background_color='white', 
        colormap='viridis', stopwords=stopwords
    ).generate(text)
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
    opinionsDf = pd.read_csv(f'../output/{updateVersion}_opinions_{weaponName}.csv')
    keywords = ['weapon', 'damage', 'gun', 'firearm', 'balancing', 'accuracy', 'reload', 
                'ammo', f'{weaponName}', 'nerf', 'medium', 'light', 'over powered', 'one hit', "skill", 
                "effecient", "one", "hit", "heavy", "buff", "recoil", "fire rate", "fire", "rate", "increase", "decrease"]
    print("Filtering opinions...")

    filteredOpinions = filterOpinionsByKeywords(opinionsDf['Opinions'], keywords)
    filteredCsvPath = os.path.join(outputDir, f"{updateVersion}_opinions_{weaponName}.csv")
    filteredOpinions.to_csv(filteredCsvPath, index=False, header=True)

    print(f"Filtered opinions saved to {filteredCsvPath}")

    allFilteredText = " ".join(filteredOpinions.dropna())
    stopwordsToExclude = {"opinion", "analysis", "player", "finals", "the", "a", "is", "and", f"{weaponName}", "mention", "opinions", "text", "please provide specific information", "please provide", "speaker"}
    print("Generating word cloud for filtered opinions...")

    wordcloudPath = os.path.join(outputDir, f"{updateVersion}_{weaponName}_word_cloud.png")
    generateWordCloud(allFilteredText, 
                      title="Word Cloud of Weapon-Related Opinions", 
                      savePath=wordcloudPath, 
                      extraStopwords=stopwordsToExclude)

    print(f"Word cloud saved to {wordcloudPath}")
    print("Analyzing sentiment for filtered opinions...")

    sentimentDf = analyzeSentiment(filteredOpinions)
    filteredOpinionsDf = pd.concat([filteredOpinions.reset_index(drop=True), sentimentDf], axis=1)

    compound_skewness = filteredOpinionsDf['compound'].skew()
    print(f"Skewness of compound sentiment scores: {compound_skewness}")

    histPath = os.path.join(outputDir, f"{updateVersion}_{weaponName}_sentiment_histogram.png")
    plt.figure(figsize=(10, 6))
    sns.histplot(data=filteredOpinionsDf, x="compound", bins=20, kde=True, color='blue')
    plt.title("Sentiment Distribution (Compound Scores) - Weapon Opinions")
    plt.xlabel("Compound Sentiment Score")
    plt.ylabel("Frequency")
    plt.savefig(histPath, format='png')
    plt.close()
    print(f"Sentiment histogram saved to {histPath}")

    boxplotPath = os.path.join(outputDir, f"{updateVersion}_{weaponName}_sentiment_boxplot.png")
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=filteredOpinionsDf[['neg', 'neu', 'pos']])
    plt.title("Sentiment Score Distribution (Negative, Neutral, Positive) - Weapon Opinions")
    plt.ylabel("Score")
    plt.savefig(boxplotPath, format='png')
    plt.close()
    print(f"Sentiment boxplot saved to {boxplotPath}")

if __name__ == "__main__":
    main()
