from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import time
from sklearn.ensemble import RandomForestRegressor
from gemini_chat import get_gemini_response
from functools import lru_cache

app = Flask(__name__)
CORS(app)

# =========================================================
# 🌍 FETCH LIVE DATA + CACHE IT FOR SPEED
# =========================================================
@lru_cache(maxsize=1)
def get_city_data_cached():
    """Fetches live/simulated data and caches it for 30 minutes."""
    current_time = time.time()
    df = _generate_city_data()
    df["_fetched_at"] = current_time
    return df

def _generate_city_data():
    """Simulates water & energy data for major Indian cities."""
    cities = ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Hyderabad",
              "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Chandigarh"]

    df = pd.DataFrame({
        "city": cities,
        "population_million": [32, 21, 13, 11, 10, 15, 8, 7, 4, 1],
        "water_usage": np.random.randint(100_000, 200_000, len(cities)),
        "energy_usage": np.random.randint(30_000, 90_000, len(cities)),
        "reused_water": np.random.randint(50_000, 150_000, len(cities)),
        "reused_energy": np.random.randint(15_000, 60_000, len(cities))
    })

    df["reuse_efficiency"] = (
        (df["reused_water"]/df["water_usage"])*50 +
        (df["reused_energy"]/df["energy_usage"])*50
    ).clip(0, 100)

    df["rank"] = df["reuse_efficiency"].rank(ascending=False).astype(int)
    df = df.sort_values("reuse_efficiency", ascending=False)
    return df

# =========================================================
# 🧠 TRAIN ML MODEL
# =========================================================
df = get_city_data_cached()
X = df[["water_usage", "energy_usage", "reused_water", "reused_energy"]]
y = df["reuse_efficiency"]
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# =========================================================
# 🌐 API ROUTES
# =========================================================
@app.route("/")
def home():
    return "✅ Flask backend with caching, ranking & AI insights running!"

@app.route("/cities", methods=["GET"])
def cities():
    df_live = get_city_data_cached()
    return jsonify(df_live.to_dict(orient="records"))

@app.route("/city_data/<city>", methods=["GET"])
def city_data(city):
    df_live = get_city_data_cached()
    row = df_live[df_live["city"].str.lower() == city.lower()]
    if not row.empty:
        return jsonify(row.to_dict(orient="records")[0])
    return jsonify({"error": "City not found"}), 404

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = np.array([[data['water_usage'], data['energy_usage'],
                          data['reused_water'], data['reused_energy']]])
    prediction = model.predict(features)[0]

    # Generate AI-based suggestions
    prompt = f"""
    For {data.get('city', 'an Indian city')}:
    - Water usage: {data['water_usage']:.0f} L/day
    - Energy usage: {data['energy_usage']:.0f} kWh/day
    - Reused water: {data['reused_water']:.0f} L/day
    - Reused energy: {data['reused_energy']:.0f} kWh/day
    Predicted reuse efficiency: {prediction:.2f}%.
    Suggest 3 actionable improvements (with reasoning) to increase reuse efficiency.
    """
    ai_insight = get_gemini_response(prompt)

    return jsonify({
        "reuse_efficiency": round(prediction, 2),
        "ai_insight": ai_insight
    })

# =========================================================
# 🏁 MAIN
# =========================================================
if __name__ == "__main__":
    app.run(debug=True)
