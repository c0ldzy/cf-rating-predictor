from flask import Flask, jsonify
from model.model import predict

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, world! → use /predict/<handle>"

@app.route("/predict/<handle>")
def predict_endpoint(handle):
    try:
        delta = predict(handle)
        return jsonify({
            "handle": handle,
            "predicted_delta": round(delta, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
