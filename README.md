# Project Proposal 
Spotify Recommendation Model

## Description
This project aims to build a personalized playlist generation system that recommends songs to users based on their listening history and preferences. This project will explore whether patterns in listening history can effectively predict songs users will enjoy. 

We will collect real listening histories from around 20-30 survey participants by asking them to download their Spotify streaming history as our data. That data will then have relevant features extracted from their listening patterns and used to train a model to generate personalized playlists. 

Success will be measured by comparing the generated playlists against user preferences and analyzing model performance metrics. 

## Project Timeline
- **Weeks 1-2**: Data collection from participants
- **Week 3**: Data cleaning and exploration
- **Week 4**: Feature extraction
- **Weeks 5-6**: Model training and comparison
- **Week 7**: Evaluation and refinement
- **Week 8**: Final report

## Clear Goals
To build a predictive model that accurately recommends songs to Spotify users by analyzing the relationships between listening behavior, audio features, and explicit user preferences. We aim to:

1. Achieve a recommendation accuracy of at least 75% for each song based on whether the user will like that song based on their listening preferences and history
2. Identify which features (behavioral patterns, audio characteristics, stated preferences, etc.) have the strongest influence on music recommendations
3. Categorize users into distinct listener personas based on their consumption patterns for more targeted recommendation strategies 
4. Build 3 models with different recommendation approaches so that we can compare them and evaluate their respective accuracies

## Data Collection
We will collect the extended streaming history from around 20-30 participants by having them download their Spotify data. 

Their data will contain features such as song name, artist, genre, duration played, skip information, etc. We plan to incorporate existing Spotify-related datasets from Kaggle as well, which will help us analyze overarching patterns and have baseline training data.

We plan to collect the data by creating Google Forms to recruit participants. The form will collect their Spotify username and include instructions on how to download their streaming history. They will then upload their streaming history as JSON files and submit it to us. 

As a backup, we plan on using the Spotify Web API or multiple Kaggle datasets to compare against our own collected data. 

## Data Modeling
We will implement and compare three different recommendation approaches to determine which best generates personalized playlists:

**Model 1: Content-Based Filtering (KNN)**  
Using KNN, we will recommend songs similar to those the user has previously enjoyed based on audio features. These features include energy, danceability, tempo, loudness, key, mode, etc. 

**Model 2: Content-Based Filtering (GMM) **  
Using a Gaussian Mixture Model we will create clusters of users or clusters of songs, based on music preferences or audio features of the songs. By matching the distributions of user's preferences to the distribution of features in a song, we can match and recommend those songs to users and see if there are certain personas or specific clusters that allow for targeted recommendation.

**Model 3: Hybrid Model (XGBoost)**  
By using Gradient Boosting like XGBoost, we will capture both song characteristics and user behavior to recommend songs. Features include user behavior (skip rate, listening frequency, repeat plays), song metadata (popularity, release year), and contextual features (genre diversity in recent listens, mood trajectories). 

**Model 4: Collaborative Filtering (User-User Similarity)**  
We will recommend songs based on what similar users have enjoyed listening to through user-user similarity using cosine similarity. This will calculate similarity between users based on shared listening patterns by finding the top 10 most similar users and then recommend songs to the user that the similar users liked but the base user hasn't listened to. 

### Evaluation Strategy
We will split the data into train, validation, and test sets for the training approach. Evaluation includes using precision, recall, F1 score, and user satisfaction score. 

## Data Visualization
In order to recognize and work with patterns of the data, we will create:
- Bar charts of genre popularity
- Heatmaps for listening frequency (hour, day, month, year)
- Trend analysis comparing individual vs. group listening behavior (when and what someone listens to)




