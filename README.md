# Data Collection

## Data Sources

This project uses 4 datasets from Kaggle, each having a variety of data that differs from the others: 

| Dataset | Source |
|---|---|
| `Spotify_data.xlsx` | [Kaggle: Spotify User Behavior Dataset](https://www.kaggle.com/datasets/meeraajayakumar/spotify-user-behavior-dataset) |
| `spotify_history.csv` | [Kaggle: Spotify Streaming History](https://www.kaggle.com/datasets/sgoutami/spotify-streaming-history) |
| `My_Streaming_Activity.csv` | [Kaggle: Streaming Activity Dataset](https://www.kaggle.com/datasets/thedevastator/streaming-activity-dataset) | 
| `spotify_recommendations.csv` | [Kaggle: Spotify Recommendations Dataset](https://www.kaggle.com/datasets/bricevergnou/spotify-recommendation) | 

---

### 1. Spotify User Behavior Survey
 
A survey dataset capturing self-reported listening behavior across genre preferences, listening habits, mood associations, and podcast behavior. We chose this dataset because it provides the kind of high-level user preference signals that complement raw play history where streaming logs tell us *what* someone listened to and survey responses tell us *why* and *how* they engage with the music.
 
---
 
### 2. Spotify Streaming History 
 
A detailed play-by-play log containing track name, artist, platform, timestamp, milliseconds played, and skip/shuffle behavior. This dataset was chosen because its schema mirrors the native JSON format of Spotify's personal data export.
 
---
 
### 3. Streaming Activity 
 
A real Spotify streaming history from a second user, exported directly from Spotify's "Download Your Data" feature. We included this dataset to enable user-user collaborative filtering, which requires at least two distinct listening profiles. Having this data and these features ensures the similarity modeling reflects authentic behavioral differences between real listeners.
 
---
 
### 4. Audio Features + Liked Label
 
A dataset of 195 songs with Spotify audio features (danceability, energy, tempo, valence, acousticness, and more) paired with a binary liked label (1 = liked, 0 = not liked). We chose a personally labeled dataset over a generic one because the liked/not-liked labels reflect a single user's genuine taste, giving the model a well-defined and consistent preference signal to learn from. The class balance is near-equal (100 liked, 95 not liked), which avoids bias issues without requiring resampling.
 
---

## Data Collection Method

All Kaggle datasets were retrieved programmatically using `gdown` to pull files from a shared Google Drive folder into the Colab runtime.

```python
!pip install gdown -q
import gdown

# Dataset 1: User Behavior Survey
gdown.download('https://drive.google.com/uc?id=1_1gQKDd-2RuQXOVTRBKHcyndxwcCcPrc',
               'Spotify_data.xlsx', quiet=False, fuzzy=True)

# Dataset 2: User 1 Streaming History
gdown.download('https://drive.google.com/uc?id=1vl3YyKYAcazsQmjObePPCoCO5PYoP6J3',
               'spotify_history.csv', quiet=False)

# Dataset 3: User 2 Personal Streaming Activity
gdown.download('https://drive.google.com/uc?id=1Qh0ZoIgrRS0fSooBp7U53cHzm4RL7Vyp',
               'My_Streaming_Activity.csv', quiet=False)

# Dataset 4: Audio Features + Liked Label
gdown.download('https://drive.google.com/uc?id=1LgtifR5DqKPe0PTMbvUlJFU74Rv_uPx2',
               'spotify_recommendations.csv', quiet=False)
```

After download, each file is loaded into a dedicated pandas DataFrame and immediately inspected for shape, column names, duplicate rows, and null counts before any cleaning is applied.

# Data Cleaning
 
In order to see the state of our data, we needed to perform an initial inspection. Below is a summary of what the data looked like initially for each of the 4 respective datasets:

```
Behavior
Columns:  ['Age', 'Gender', 'spotify_usage_period', 'spotify_listening_device', 'spotify_subscription_plan', 'premium_sub_willingness', 'preffered_premium_plan', 'preferred_listening_content', 'fav_music_genre', 'music_time_slot', 'music_Influencial_mood', 'music_lis_frequency', 'music_expl_method', 'music_recc_rating', 'pod_lis_frequency', 'fav_pod_genre', 'preffered_pod_format', 'pod_host_preference', 'preffered_pod_duration', 'pod_variety_satisfaction']
Duplicates:  1
Nulls:  {'preffered_premium_plan': 208, 'fav_pod_genre': 148, 'preffered_pod_format': 140, 'pod_host_preference': 141, 'preffered_pod_duration': 129}

History
Columns:  ['spotify_track_uri', 'ts', 'platform', 'ms_played', 'track_name', 'artist_name', 'album_name', 'reason_start', 'reason_end', 'shuffle', 'skipped']
Duplicates:  1185
Nulls:  {'reason_start': 143, 'reason_end': 117}

My Stream
Columns:  ['index', 'SongID', 'TimeStamp_Central', 'Performer', 'Album', 'Song', 'TimeStamp_UTC']
Duplicates:  0
Nulls:  {'Album': 2559}

Recommendations
Columns:  ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature', 'liked']
Duplicates:  0
Nulls:  None
```
---

## Handling data

As you can see, each dataset had their own unique problems and in the data cleaning process, we went through each dataset and dealt with missing/noisy/inconsistent data. 

### 1. Spotify User Behavior Survey
 
We removed 1 duplicate row to prevent skewed genre and mood distributions. Several column names contained misspellings such as ‘preffered’ and ‘Influencial’ which we standardized for consistency across all notebooks. String values of 'None' were replaced with actual null values so that pandas null-handling functions work correctly downstream. We also stripped whitespace from all string columns to prevent duplicate categories caused by spacing differences.
 
---
 
### 2. Spotify Streaming History 
 
We removed 1,185 duplicate rows which would have inflated play counts and skewed skip rate calculations. The timestamp column was parsed from a string into a datetime object to enable time-based feature extraction. Milliseconds played was converted to seconds and minutes for interpretability. Rows where milliseconds played was 0 were removed as these represent buffering artifacts rather than real listens. We then flagged plays under 30 seconds as likely skipped, since the original skipped column only captures explicit forward-button skips and misses implicit skips where the user simply waited briefly before skipping. Null values in the reason start and reason end columns were filled with the value 'unknown' since a missing reason does not invalidate the play record. 
 
---
 
### 3. Streaming Activity 
 
We dropped 3 redundant columns: a row index, a duplicate timezone timestamp, and a SongID column that was an unparseable concatenation of song name and artist with no separator. The UTC timestamp was parsed as a datetime and renamed to match the first streaming dataset's conventions. Rows with null album values were flagged as non-music content such as videos and gaming clips rather than dropped outright, since they still carry valid listening time information. We stripped whitespace from all string columns and renamed columns to match the first streaming dataset so that both can be combined. Both streaming datasets were then combined into a single dataframe with a user ID column added to distinguish which plays belong to which user, giving us a combined dataset of approximately 208,000 play records across two users.
 
---
 
### 4. Audio Features + Liked Label
 
This dataset required minimal cleaning as it contained no nulls or duplicates. We converted duration from milliseconds to seconds for consistency with the other datasets. The most important processing step was applying MinMax normalization to all 13 audio features, scaling each to a range of 0 to 1. This is necessary because KNN is a distance-based algorithm: without normalization, high-range features like tempo (which sits between 60 and 200 BPM) would dominate the distance calculation over features that naturally sit between 0 and 1 like danceability, causing the model to weight tempo far more heavily than intended.
 
---
