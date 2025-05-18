import os, requests, pandas as pd, numpy as np, joblib

CF_API_URL = "https://codeforces.com/api/user.rating"
MODEL_PATH = os.path.join(os.path.dirname(__file__), "linreg_model.pkl")
_model = None

def _load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("No model found. Run train/train_model.py")
        _model = joblib.load(MODEL_PATH)
    return _model

def predict(handle: str) -> float:
    r = requests.get(f"{CF_API_URL}?handle={handle}")
    r.raise_for_status()
    js = r.json()
    if js.get("status") != "OK":
        raise ValueError(js.get("comment", "API error"))
    hist = js["result"]
    if not hist:
        raise ValueError("No contests for that handle")
    df = pd.DataFrame(hist)
    df["delta"] = df["newRating"] - df["oldRating"]
    deltas = df["delta"].values
    if len(deltas) >= 10:
        X = deltas[-10:].reshape(1, -1)
        return float(_load_model().predict(X)[0])
    else:
        return float(pd.Series(deltas).mean())
