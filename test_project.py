"""
Basic sanity tests for the Spotify recommendation project.
Tests that data files exist, have expected structure, and models run correctly.
"""

import os
import pytest
import pandas as pd
import numpy as np

DATA_PATH = "code/data"

# 1. Raw data files exist 

def test_raw_files_exist():
    for fname in [
        "spotify_history.csv",
        "spotify_recommendations.csv",
        "My_Streaming_Activity.csv",
        "Spotify_data.xlsx",
    ]:
        assert os.path.exists(os.path.join(DATA_PATH, fname)), \
            f"Missing raw data file: {fname}"

# 2. Cleaned files exist and have expected columns 

def test_cleaned_audio_features():
    path = os.path.join(DATA_PATH, "cleaned_audio_features.csv")
    assert os.path.exists(path), "cleaned_audio_features.csv not found"
    df = pd.read_csv(path)
    expected_cols = [
        "danceability", "energy", "loudness", "speechiness",
        "acousticness", "instrumentalness", "liveness", "valence",
        "tempo", "liked"
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"
    assert len(df) > 0, "cleaned_audio_features.csv is empty"

def test_cleaned_streaming_history():
    path = os.path.join(DATA_PATH, "cleaned_streaming_history.csv")
    assert os.path.exists(path), "cleaned_streaming_history.csv not found"
    df = pd.read_csv(path)
    expected_cols = ["track_name", "artist_name", "ms_played", "hour", "day_of_week"]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"
    assert len(df) > 0, "cleaned_streaming_history.csv is empty"

def test_cleaned_user_behavior():
    path = os.path.join(DATA_PATH, "cleaned_user_behavior.csv")
    assert os.path.exists(path), "cleaned_user_behavior.csv not found"
    df = pd.read_csv(path)
    assert len(df) > 0, "cleaned_user_behavior.csv is empty"

def test_cleaned_streaming_activity():
    path = os.path.join(DATA_PATH, "cleaned_my_streaming_activity.csv")
    assert os.path.exists(path), "cleaned_my_streaming_activity.csv not found"
    df = pd.read_csv(path)
    assert len(df) > 0, "cleaned_my_streaming_activity.csv is empty"

# 3. Data quality checks

def test_audio_features_normalized():
    """All audio feature values should be in [0, 1] after cleaning."""
    df = pd.read_csv(os.path.join(DATA_PATH, "cleaned_audio_features.csv"))
    feature_cols = [
        "danceability", "energy",
        "acousticness", "instrumentalness", "liveness", "valence"
    ]
    for col in feature_cols:
        assert float(df[col].min()) >= 0 and float(df[col].max()) <= 1, \
            f"Column '{col}' has values outside [0, 1]"

def test_liked_column_is_binary():
    """The 'liked' label should only contain 0s and 1s."""
    df = pd.read_csv(os.path.join(DATA_PATH, "cleaned_audio_features.csv"))
    assert set(df["liked"].unique()).issubset({0, 1}), \
        "'liked' column contains values other than 0 and 1"

def test_no_nulls_in_audio_features():
    df = pd.read_csv(os.path.join(DATA_PATH, "cleaned_audio_features.csv"))
    assert df.isnull().sum().sum() == 0, \
        "cleaned_audio_features.csv contains null values"

def test_streaming_history_no_zero_plays():
    """Zero ms_played rows should have been removed in cleaning."""
    df = pd.read_csv(os.path.join(DATA_PATH, "cleaned_streaming_history.csv"))
    assert (df["ms_played"] > 0).all(), \
        "cleaned_streaming_history.csv still contains zero-play rows"

# 4. KNN model runs and produces valid predictions

def test_knn_model_runs():
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split

    df = pd.read_csv(os.path.join(DATA_PATH, "cleaned_audio_features.csv"))
    features = [
        "danceability", "energy", "loudness", "speechiness",
        "acousticness", "instrumentalness", "liveness", "valence", "tempo"
    ]
    X = df[features]
    y = df["liked"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train_scaled, y_train)
    preds = knn.predict(X_test_scaled)

    assert len(preds) == len(X_test), "KNN output length doesn't match test set"
    assert set(preds).issubset({0, 1}), "KNN predictions contain unexpected values"

# 5. Cosine similarity produces valid output

def test_cosine_similarity_runs():
    from sklearn.metrics.pairwise import cosine_similarity

    df = pd.read_csv(os.path.join(DATA_PATH, "cleaned_streaming_history.csv"))

    # Build a tiny user-item matrix from the real data
    df["user_id"] = "user_1"
    matrix = df.groupby(["user_id", "track_name"])["ms_played"].sum().unstack(fill_value=0)

    sim = cosine_similarity(matrix)
    assert sim.shape == (matrix.shape[0], matrix.shape[0]), \
        "Cosine similarity matrix has wrong shape"
    assert float(sim.min()) >= -1 and float(sim.max()) <= 1 + 1e-6, \
        "Cosine similarity values out of expected range"
