import os, sys, json, requests, pandas as pd

API = "https://codeforces.com/api/user.rating"

def fetch(h):
    r = requests.get(API, params={"handle": h}, timeout=10).json()
    if r.get("status") != "OK":
        raise Exception(f"API error: {r.get('comment')}")
    return r["result"]

def save_raw(h, data):
    os.makedirs("data/raw", exist_ok=True)
    p = f"data/raw/{h}_rating.json"
    with open(p, "w") as f:
        json.dump(data, f, indent=2)
    print("Saved raw JSON →", p)

def save_csv(h, data):
    df = pd.DataFrame(data)
    df["ratingUpdateTimeSeconds"] = pd.to_datetime(df["ratingUpdateTimeSeconds"], unit="s")
    df["delta"] = df["newRating"] - df["oldRating"]
    os.makedirs("data/processed", exist_ok=True)
    p = f"data/processed/{h}_rating.csv"
    df.to_csv(p, index=False)
    print("Saved processed CSV →", p)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python data_pull.py <handle>")
        sys.exit(1)
    handle = sys.argv[1].strip()
    hist = fetch(handle)
    save_raw(handle, hist)
    save_csv(handle, hist)
