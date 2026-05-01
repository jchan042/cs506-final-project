# Data Collection

## Data Sources

This project uses 4 datasets from Kaggle, each having a variety of data that differs from the others: 

| Dataset | Source | Size |
|---|---|---|
| `Spotify_data.xlsx` | [Kaggle: Spotify User Behavior Dataset](https://www.kaggle.com/datasets/meeraajayakumar/spotify-user-behavior-dataset) | 520 rows |
| `spotify_history.csv` | [Kaggle: Spotify Streaming History](https://www.kaggle.com/datasets/sgoutami/spotify-streaming-history) | ~150,000 rows |
| `My_Streaming_Activity.csv` | [Kaggle: Streaming Activity Dataset](https://www.kaggle.com/datasets/thedevastator/streaming-activity-dataset) | ~2,500 rows |
| `spotify_recommendations.csv` | [Kaggle: Spotify Recommendations Dataset](https://www.kaggle.com/datasets/bricevergnou/spotify-recommendation) | 195 songs |

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

All datasets were retrieved programmatically using `gdown` to pull files from a shared Google Drive folder into the Colab runtime. This is implemented in **Section 2** of [`data_cleaning.ipynb`](data_cleaning.ipynb):

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
