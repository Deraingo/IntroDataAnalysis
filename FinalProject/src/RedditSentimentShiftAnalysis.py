import pandas as pd
import os
import numpy as np
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt

baseDir = "reddit_output"
weapons = ["pike", "cl40", "model 1887", "revolver"]
updateVersions = ["pre_update", "post_update"]

def loadSentimentData(weapon, updateVersion):
    filePath = os.path.join(baseDir, updateVersion, weapon, f"{updateVersion}_{weapon}_reddit_opinions_filtered.csv")
    if os.path.exists(filePath):
        return pd.read_csv(filePath)
    else:
        print(f"File not found: {filePath}")
        return None

results = {}
for weapon in weapons:
    preData = loadSentimentData(weapon, "pre_update")
    postData = loadSentimentData(weapon, "post_update")
    if preData is not None and postData is not None:
        preSentimentAvg = preData["sentimentScore"].mean()
        postSentimentAvg = postData["sentimentScore"].mean()
        sentimentShift = postSentimentAvg - preSentimentAvg
        results[weapon] = {
            "preSentimentAvg": preSentimentAvg,
            "postSentimentAvg": postSentimentAvg,
            "sentimentShift": sentimentShift,
        }

sentimentShifts = [results[weapon]["sentimentShift"] for weapon in weapons]
weaponChanges = [2, 2, 2, 0]

correlation, pValue = pearsonr(sentimentShifts, weaponChanges)

print("Sentiment Analysis Results:")
for weapon, data in results.items():
    print(f"{weapon.capitalize()}: Pre-update Avg Sentiment = {data['preSentimentAvg']:.2f}, Post-update Avg Sentiment = {data['postSentimentAvg']:.2f}, Sentiment Shift = {data['sentimentShift']:.2f}")

print("\nCorrelation Analysis:")
print(f"Correlation between sentiment shifts and weapon changes: {correlation:.2f} (p-value: {pValue:.4f})")


sentimentShiftGraphPath = os.path.join(baseDir, "sentiment_shift_analysis.png")
plt.figure(figsize=(8, 6))
plt.bar(weapons, sentimentShifts, color="skyblue")
plt.xlabel("Weapons")
plt.ylabel("Sentiment Shift")
plt.title("Sentiment Shift for Each Weapon")
plt.savefig(sentimentShiftGraphPath)
plt.show()

pearsonCorr, pearsonP = pearsonr(sentimentShifts, weaponChanges)
spearmanCorr, spearmanP = spearmanr(sentimentShifts, weaponChanges)

print("Correlation Analysis:")
print(f"Pearson Correlation: {pearsonCorr:.2f} (p-value: {pearsonP:.4f})")
print(f"Spearman Correlation: {spearmanCorr:.2f} (p-value: {spearmanP:.4f})")

correlationGraphPath = os.path.join(baseDir, "correlation_sentiment_weapon_changes.png")
plt.figure(figsize=(8, 6))
plt.scatter(weaponChanges, sentimentShifts, color='blue', label="Data Points")
plt.plot(np.unique(weaponChanges), 
         np.poly1d(np.polyfit(weaponChanges, sentimentShifts, 1))(np.unique(weaponChanges)), 
         color='red', label="Trend Line")
plt.xlabel("Weapon Changes")
plt.ylabel("Sentiment Shift")
plt.title("Correlation Between Weapon Changes and Sentiment Shifts")
plt.legend()
plt.grid()
plt.savefig(correlationGraphPath)
plt.show()

print(f"Saved bar chart to: {sentimentShiftGraphPath}")
print(f"Saved correlation graph to: {correlationGraphPath}")
