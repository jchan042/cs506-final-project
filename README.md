# Data Collection

## Data Sources

This project uses 4 datasets from Kaggle, each having a variety of data that differs from the others: 

| Dataset | Source | Size | Purpose |
|---|---|---|---|
| `Spotify_data.xlsx` | [Kaggle – Spotify User Behavior Dataset](https://www.kaggle.com/datasets/meeraajayakumar/spotify-user-behavior-dataset) | 520 rows | Survey data covering genre preferences, listening habits, and mood associations |
| `spotify_history.csv` | [Kaggle – Spotify Streaming History](https://www.kaggle.com/datasets/sgoutami/spotify-streaming-history) | ~150,000 rows | User 1 play-by-play streaming history with timestamps, skip signals, and shuffle info |
| `My_Streaming_Activity.csv` | Personal Spotify data export (User 2, 2017–2021) | ~2,500 rows | Second user's real streaming history; used for user-user collaborative filtering (Model 3) |
| `spotify_recommendations.csv` | Personal labeled audio features | 195 songs | Binary liked/not-liked labels paired with Spotify audio features; primary training data for KNN (Model 1) |

The two Kaggle datasets were selected because their schema mirrors Spotify's native JSON streaming export format, ensuring the pipeline can generalize to real participant data. The personal Spotify export (`My_Streaming_Activity.csv`) provides a second authentic listening profile without requiring additional survey recruitment, enabling cross-user similarity modeling.

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

> **Note:** The Google Drive links above require "Anyone with the link" sharing permissions to be set. The files must remain shared for the download step to succeed in a fresh Colab session.
