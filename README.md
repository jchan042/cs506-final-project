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
 
### 3. Personal Streaming Activity 
 
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

## Data Cleaning
 
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
