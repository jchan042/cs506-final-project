# Final Video : https://www.youtube.com/watch?v=NKRH1eM6CK4

# How to Build and Run the Code

## Prerequisites

- Python 3.8 or higher
- `pip` (comes with Python)
- Git

## Setup & Usage

**Step 1: Clone the repo**
```bash
git clone https://github.com/jchan042/cs506-final-project
cd cs506-final-project
```

**Step 2: Install dependencies**
```bash
make install
```

**Step 3: Run all notebooks**
```bash
make run
```

**Clean generated files**
```bash
make clean
```

## Dependencies

All dependencies are listed in `requirements.txt` and installed automatically via `make install`:

| Package | Purpose |
|---|---|
| `pandas` | Data manipulation |
| `numpy` | Numerical computation |
| `scikit-learn` | KNN and cosine similarity models |
| `matplotlib` | Plotting |
| `seaborn` | Statistical visualizations |
| `gdown` | Downloading files from Google Drive |
| `jupyter` | Running notebooks interactively |
| `nbconvert` | Executing notebooks non-interactively |

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

# Feature Engineering
 
Features were derived from the cleaned datasets to provide richer signals for modeling. The table below summarizes every engineered feature, the dataset it came from, and its purpose.
 
| Feature | Dataset | Type | Purpose |
|---|---|---|---|
| `hour` | Streaming History (both users) | Temporal | Captures time-of-day listening patterns |
| `day_of_week` | Streaming History (both users) | Temporal | Captures weekday vs. weekend behavior |
| `month` | Streaming History (both users) | Temporal | Captures seasonal listening trends |
| `year` | Streaming History (both users) | Temporal | Enables longitudinal comparison across years |
| `seconds_played` | User 1 Streaming History | Behavioral | Human-readable form of `ms_played`; used for skip detection |
| `minutes_played` | User 1 Streaming History | Behavioral | Higher-level duration for summary statistics |
| `likely_skipped` | User 1 Streaming History | Behavioral | `True` if play was under 30s; flags implicit skips not captured by the `skipped` field |
| `skip_rate` | User 1 Streaming History | Behavioral | Per-track mean of `likely_skipped`; measures how often a track gets skipped across all plays |
| `play_count` | Streaming History (both users) | Behavioral | Number of times a track was played; proxy for preference strength |
| `is_non_music` | User 2 Streaming Activity | Boolean flag | Marks rows where `Album` is null (podcasts, videos, gaming clips) so models can filter them |
| `duration_s` | Audio Features | Audio | `duration_ms` converted to seconds for consistency |
| `user_id` | Combined Streaming Dataset | Identifier | Labels each play as `'user_1'` or `'user_2'` to preserve user identity after merging |
 
---
 
### Spotify Streaming History 
 
We extracted hour, day of week, month, and year from the timestamp for use in visualizations and as contextual features in modeling. Finally we derived two new columns, skip rate and play count per track, which serve as behavioral features.
 
`skip_rate` is computed as the per-track mean of `likely_skipped` and reflects how frequently a track gets abandoned. `play_count` counts total plays per track and acts as a proxy for preference strength. Both are merged back onto the main DataFrame so every row carries track-level behavioral context.
 
```python
# Time features
df_hist['hour']        = df_hist['ts'].dt.hour
df_hist['day_of_week'] = df_hist['ts'].dt.day_name()
df_hist['month']       = df_hist['ts'].dt.month
df_hist['year']        = df_hist['ts'].dt.year
 
# Behavioral features
df_hist['likely_skipped'] = df_hist['seconds_played'] < 30
 
skip_rate  = df_hist.groupby('track_name')['likely_skipped'].mean().reset_index()
skip_rate.columns = ['track_name', 'skip_rate']
 
play_count = df_hist.groupby('track_name').size().reset_index(name='play_count')
 
df_hist = df_hist.merge(skip_rate,  on='track_name', how='left')
df_hist = df_hist.merge(play_count, on='track_name', how='left')
```
 
---
 
### Streaming Activity
 
We also derived play count per track and extracted the same time features as the first streaming dataset.
 
Because this dataset does not include milliseconds played or a skip field, `skip_rate` and `likely_skipped` cannot be computed and are not present. The shared features (`hour`, `day_of_week`, `month`, `year`, `play_count`) are what allow both users' histories to be combined into a single DataFrame for Model 3.
 
```python
# Time features
df_myst['hour']        = df_myst['ts'].dt.hour
df_myst['day_of_week'] = df_myst['ts'].dt.day_name()
df_myst['month']       = df_myst['ts'].dt.month
df_myst['year']        = df_myst['ts'].dt.year
 
# Behavioral features
play_count2 = df_myst.groupby('Song').size().reset_index(name='play_count')
df_myst = df_myst.merge(play_count2, on='Song', how='left')
```
 
---
 
### Audio Features + Liked Label Dataset
 
No new features were derived here. Instead, all 13 existing Spotify audio features were normalized to `[0, 1]` using `MinMaxScaler` so they are on a comparable scale for KNN distance calculations. The features and what they measure are:
 
| Feature | What it measures |
|---|---|
| `danceability` | How suitable a track is for dancing (rhythm, tempo stability, beat strength) |
| `energy` | Perceptual intensity and activity level |
| `key` | Estimated musical key (0 = C, 1 = C♯, … 11 = B) |
| `loudness` | Overall loudness in decibels |
| `mode` | Modality: major (1) or minor (0) |
| `speechiness` | Presence of spoken words |
| `acousticness` | Confidence that the track is acoustic |
| `instrumentalness` | Likelihood of no vocal content |
| `liveness` | Probability the track was recorded live |
| `valence` | Musical positivity (high = happy, low = sad/tense) |
| `tempo` | Estimated beats per minute |
| `duration_s` | Track length in seconds |
| `time_signature` | Estimated beats per bar |
| `liked` | **Target variable**: 1 if the user liked the track, 0 if not |

#  Models

## K-Nearest Neighbors (KNN)

### Training Procedure

The KNN model is trained on `spotify_recommendations.csv`, a dataset of 195 songs with Spotify audio features and a binary `liked` label (1 = liked, 0 = not liked). Nine continuous audio features were selected as inputs (danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, and tempo) while non-informative features like key, mode, and time_signature were excluded to keep the feature space clean.

The data was split 70/15/15 into train, validation, and test sets using stratified sampling to achieve the class balance of 100 liked, 95 not liked. All features were standardized using `StandardScaler` before training since KNN is a distance-based model and unscaled features like tempo (0–250 BPM) would dominate other features that sit in the 0–1 range. K was tuned by evaluating F1 score on the validation set ranging from k=1 through 30, with **k=21** selected as optimal (validation F1 = 0.933).

### Model Choice

KNN is a very reasonable model for our project as song preference heavily relies on audio similarity. For example, if a user likes tracks with high danceability and low instrumentalness, the model finds new songs closest to those statistics in feature space. All nine input features are continuous and numeric, which is ideal for distance-based methods. The model also takes a liked song's audio features and fetches the most similar sounding songs by nearest-neighbor distance.

### Evaluation Strategy

The final model is evaluated on the test set of thirty songs using precision, recall, and F1 score rather than accuracy, since the slight class imbalance makes F1 a more reliable measure of performance. The model achieved a precision of 0.81, recall of 0.87, and F1 of 0.84, correctly classifying 25 out of 30 songs. A confusion matrix is then generated to visualize the breakdown of true/false positives and negatives regarding if the song was truly liked or not. Since KNN has no built-in feature weights each feature is shuffled one at a time and the resulting drop in F1 score indicates how much the model relies on it.

### Limitations & Failure Cases

- **Small dataset:** Since we worked with only 195 songs and had thirty songs in the test set, our results may not have generalized reliably to broader listening behaviors.
- **No personalization depth:** The model learns a single user's taste. It fails to distinguish that the user might like a combination of music genres for a variety of different reasons.
- **Cold start:** The recommendation function requires a liked song as an input. It fails to generate song suggestions without a given history.
- **Euclidean distance assumptions:** After scaling, all nine features are treated as equally important. The model fails to understand that a user may prioritize tempo over danceability, for example.


## Cosine Similarity 

### Training Procedure

This model implements a user-user collaborative filtering system built on top of Spotify listening history. It scores based on whether the user actually listened to it or skipped it, giving a clearer picture of what they genuinely like than raw play counts alone. Then, it uses cosine similarity to identify users with similar taste profiles and surface songs they loved that the target user hasn't heard yet.

1. Skip-Adjusted Interaction Weights
Each (user, track) pair is assigned a weight based on listening behavior:

```python
weight = (complete_plays × 2 + non_skip_plays × 1 − skip_plays × 1.5) / total_plays
```

Completed listens are rewarded, skips are penalized, and tracks with only one play are zeroed out. Tracks scoring above 0.5 are labeled as “liked”.

2. User-Item Matrix
Weights are pivoted into a [users × tracks] matrix where each row is one user's preference vector across all tracks.

3. Cosine Similarity
The model computes pairwise cosine similarity across all user vectors. Users with similar patterns of liked and skipped tracks end up with high similarity scores.

4. Recommendation
For a target user, the top ten most similar users are identified. Tracks they liked that the target hasn't heard are aggregated and ranked based on similarity-weighted score.

### Model Choice 

User-user collaborative filtering is a fit for this project because music taste is inherently social; people with similar listening patterns tend to enjoy similar songs. Cosine similarity is well suited here as it compares the shape of two users' preference vectors rather than their size, meaning a user with 50 plays and one with 500 can still be meaningfully compared. The skip-adjusted weights ensure the data fed into the model reflects what users actually like, not just what they have played.

### Evaluation Strategy
The model is evaluated using a holdout strategy where 20% of each user's liked tracks are hidden before recommendations are generated, then checked against the top 10 results. Precision, Recall, and F1 are reported rather than accuracy, since the goal is ranking and retrieval rather than binary classification. Users with fewer than 5 liked tracks are excluded, as there are not enough songs to construct a meaningful holdout set.

| Metric | Description |
|---|---|
| Precision | How many of the recommended songs were actually in the hidden set |
| Recall | How many of the hidden songs appeared in the recommendations |
| F1 | The average of precision and recall combined into one score |

Running the model on simulated users yielded a precision of 0.47, meaning that nearly half of the recommendations were songs the user liked. Recall was low at 0.027, which is expected given the dataset's 94.6% sparsity, since there were over 16,000 tracks in the catalog. The F1 score of 0.050 reflects this tradeoff between strong precision and limited recall.

### Limitations & Failure Cases
- **Cold start:** users with very few plays lack enough signal to build a meaningful preference vector or holdout set
- **Synthetic users:** the 25 users are partitioned from a single person's history, which inflates similarity scores and reduces the diversity of taste the model is exposed to
- **Sparsity:** most users have only heard a small fraction of all the songs in the dataset, making the user-item matrix sparse and candidate scores noisy
- **Popularity bias:** tracks that appear across many users' histories naturally accumulate higher recommendation scores, regardless of how well they fit the target user specifically

## XGBoost

### Training Procedure

The XGBoost model is trained on `spotify_history.csv`, a dataset of 145,139 plays across 16,342 unique tracks spanning 2013–2024. Rather than predicting song preference directly, the model predicts whether a given play will be skipped, where a play is labeled as skipped if Spotify's `skipped` flag is true or the play ended via the forward or back button (`reason_end ∈ {fwdbtn, backbtn}`). This framing keeps the label and features cleanly disjoint and avoids the target leakage that occurs when track-level engagement statistics like skip rate and completion rate are used both to define the label and as model inputs.

Eleven context features describe the moment each play started — not properties of the track or outcomes of the play. These include cyclical encodings of hour, day-of-week, and month (so wrap-arounds like Sunday-to-Monday are preserved), `is_weekend`, `shuffle`, `minutes_since_last` (time elapsed since the previous play, capped at 24 hours), and the categorical fields `platform` and `reason_start`. Track-level aggregates and outcome-derived columns like `ms_played`, `seconds_played`, and `likely_skipped` are deliberately excluded because they bake the label into the features.

The data is split temporally: plays before January 1, 2024 (135,282 rows) form the training set, and 2024 plays (9,857 rows) form the test set. A temporal split is the honest evaluation choice for time-series data, since a random split would leak future plays into training. Class imbalance is handled with `scale_pos_weight = neg/pos ≈ 1.58`, and categorical features use XGBoost's native handling via `enable_categorical=True` and `tree_method="hist"`. Hyperparameters: 300 trees, max_depth=5, learning_rate=0.05, subsample and colsample_bytree at 0.8.

### Model Choice

XGBoost suits this problem because the features are a mix of continuous (cyclical time encodings, minutes_since_last) and categorical (platform, reason_start), and gradient-boosted trees handle that mix natively without one-hot encoding. The model captures non-linear interactions — for example, the effect of `shuffle=True` on skip probability may differ between mobile and desktop platforms — which a linear model cannot. XGBoost is also robust to feature scaling and tolerant of missing values, which is useful when the data spans eleven years and column conventions may have shifted over time.

### Evaluation Strategy

The model is evaluated on the 2024 holdout set using precision, recall, F1, and ROC AUC, with F1 prioritized over accuracy because of the moderate class imbalance (22% skip rate in test). A confusion matrix shows the breakdown of true and false positives and negatives. To diagnose what the model is actually learning, three ablation variants were trained on identical data:

| Variant | Features removed | F1 | AUC |
|---|---|---|---|
| Full | none | 0.846 | 0.955 |
| No reason_start | `reason_start` | 0.861 | 0.948 |
| Pure context | `reason_start`, `minutes_since_last` | 0.385 | 0.582 |

The pure context variant — keeping only time, platform, and shuffle — collapses to near-random performance, revealing that the headline AUC is driven almost entirely by a single autoregressive feature (`minutes_since_last`). This is reported as the model's primary finding rather than buried: skip behavior is bursty (clustered in time) rather than habitual (tied to specific contexts).

### Limitations & Failure Cases

- **Single-feature dominance:** removing `minutes_since_last` collapses AUC from 0.95 to 0.58, meaning the model is functionally a session-momentum detector rather than a behavioral model
- **Skip ≠ dislike:** skipping is a noisy proxy for preference, since users skip songs they love when in a hurry and let songs they dislike finish when distracted
- **Concept drift:** train skip rate (39%) is much higher than test skip rate (22%), indicating substantial behavioral change between the training and evaluation periods
- **Single-user data:** n=1 limits any claims about generalization; the model captures one person's patterns and cannot transfer to other users
- **No track features:** without audio properties like genre, energy, or tempo, the model cannot explain why skips occur, only that they cluster in time
- **Misleading feature importance:** `reason_start` scored 28% importance in the full model but its removal slightly improved F1, showing that XGBoost's importance metric counts split frequency rather than predictive contribution

#  Visualizations 

1. Genre Distribution (Bar Chart)
A count plot of fav_music_genre ranked by frequency reveals which genres dominate listener preferences across the survey population. This distribution is used to weight genre recommendations; genres with higher representation are surfaced more confidently, while niche genres signal an opportunity for deeper catalog exploration.
Key insight: Listener preferences are rarely uniform. A long tail of minority genres typically appears, suggesting that a one-size-fits-all genre filter would exclude a meaningful portion of users.

2. Stream Frequency Heatmap by Calendar Date
Streaming history is aggregated by year, month, and day of month, then rendered as a calendar heatmap (months on the Y-axis, days on the X-axis). Each cell's color intensity represents how many tracks were played on that date.
Key insight: Listening volume is highly uneven across the year. Dense clusters of activity often correspond to periods of commuting, travel, or seasonal habits (e.g., summer months or holiday breaks). Sparse regions indicate low-engagement periods where recommendations may need to be more proactive or contextually prompted.

3. Listening Habits Facet Grid (Hour × Day of Week, by Month)
This is the most granular temporal visualization. Streaming history is broken into month-level heatmaps, each showing day of week (rows) vs. hour of day (columns), colored by stream count using the magma palette.
Key insight: Listeners exhibit strong daily and weekly rhythms. Common patterns include:

Morning peaks on weekday commutes (7–9 AM, Monday–Friday)
Evening wind-down listening (9–11 PM, particularly on weekdays)
Extended weekend sessions on Saturday and Sunday afternoons
Monthly variation : certain months show compressed, high-intensity listening while others are diffuse

These patterns can directly inform when to push recommendations: a curated "Monday morning" playlist is more contextually relevant than a generic weekly digest.

4. Audio Feature Radar Chart
The seven Spotify audio features are averaged across all tracks in df_audio and plotted on a polar radar chart. The resulting polygon is the listener's acoustic fingerprint : a signature of what they tend to listen to at a feature level.
Key insight: The shape of the radar reveals taste at a glance. A listener with high valence and energy gravitates toward upbeat, euphoric music. High acousticness and low energy points to a preference for quiet, intimate recordings. High speechiness suggests spoken-word content or rap. This fingerprint is used as a similarity target when ranking candidate tracks for recommendation.


5. Mood Map (Energy vs. Valence Scatter Plot)
Tracks in df_audio are plotted as points on a two-dimensional mood space: valence (sad → happy) on the X-axis and energy (calm → intense) on the Y-axis. Points are colored by the liked field. Dashed reference lines at 0.5 on each axis divide the space into four quadrants:
QuadrantCharacterHigh valence, high energyEuphoric / partyHigh valence, low energyPeaceful / contentLow valence, high energyAngry / tenseLow valence, low energyMelancholic / reflective
Key insight: The distribution of liked vs. unliked tracks across quadrants reveals the listener's emotional comfort zone. If liked tracks cluster in the high-energy, high-valence quadrant, the recommender should prioritize tracks in that region. Tracks in quadrants with few or no liked points can be deprioritized or used for deliberate mood contrast.
