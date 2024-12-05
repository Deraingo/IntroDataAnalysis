# Collecting Data
- Twitter API
- YouTube API
- Twitch API
- Zffermans Weapon MAster Sheet 4.0.0 (view updated sheets as well)

## Data Collection:
Collect the data related to The Finals game, such as weapon balancing stats, class pick rates, and influencer feedback.
- Webscrape every thursday from patchnotes
- backfill from old patchnotes
- grab tweet data and transcript data from twitch and youtube

## Text Cleaning:
Clean any text data, such as influencer feedback or patch notes. This might involve removing special characters, converting text to lowercase, and eliminating stopwords (if applicable).

## Text Representation:
If you are dealing with textual data, convert it into numerical representations. For example, use techniques like TF-IDF, bag-of-words, or word embeddings like Word2Vec or BERT for influencer feedback analysis.

## Data Preprocessing:
This step includes:
- Handling missing data.
- Normalizing/standardizing numerical features (such as weapon stats).
- Encoding categorical variables like class types, game modes, etc.
- Feature scaling for numerical data (Min-Max or Z-score scaling).

## Train-Validation-Test Split:
Split dataset into three parts:
- Training Set: For training model (e.g., Random Forest as shown).
- Validation Set: To fine-tune model and avoid overfitting.
- Test Set: For the final evaluation of model performance.

## Model Training:
- Use machine learning models (like Random Forest, as suggested in the diagram) to predict outcomes such as player behavior trends or game balance impacts. 
- Train the model on the training set and validate it using the validation set to optimize hyperparameters.

## Model Testing:
- After training, evaluate the model's performance using the test set to ensure it generalizes well on unseen data.

## Report Performance:
- Finally, calculate performance metrics (accuracy, precision, recall, F1-score, etc.) and report them. Visualize the results, such as showing the effect of buffs/nerfs on player behavior.