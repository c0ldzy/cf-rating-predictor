#!/usr/bin/env python3
import os, glob
import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression

def load_data(processed_dir="data/processed", window_size=10):
    X, y = [], []
    for path in glob.glob(f"{processed_dir}/*_rating.csv"):
        df = pd.read_csv(path)
        if "delta" not in df or len(df) <= window_size:
            continue
        deltas = df["delta"].values
        for i in range(window_size, len(deltas)):
            X.append(deltas[i - window_size:i])
            y.append(deltas[i])
    return np.array(X), np.array(y)

def train_and_save(model_path="model/linreg_model.pkl"):
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    X, y = load_data()
    if len(X) == 0:
        raise RuntimeError("No training data found.")
    print(f"Training on {len(X)} samples...")
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, model_path)
    print(f"Model saved → {model_path}")

if __name__ == "__main__":
    train_and_save()
