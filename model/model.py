import requests
import pandas as pd

CF_API_URL = "https://codeforces.com/api/user.rating"
K = 3  # number of past contests to average

def predict(handle: str) -> float:
    """
    Fetch a user's rating history from Codeforces,
    compute contest-to-contest deltas, then return
    the mean of the last K deltas (or overall mean).
    """
    resp = requests.get(f"{CF_API_URL}?handle={handle}")
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "OK":
        comment = data.get("comment", "<no comment>")
        raise ValueError(f"API error for {handle}: {comment}")

    history = data["result"]
    if not history:
        raise ValueError(f"No contests found for {handle}")

    df = pd.DataFrame(history)
    df["delta"] = df["newRating"] - df["oldRating"]
    last_deltas = df["delta"].tail(K)
    return float(last_deltas.mean())
