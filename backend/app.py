from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)

@app.route("/")
def index():
    return app.send_static_file("index.html")

# Comprehensive list matching the SVG map
STATES = [
    "Jammu and Kashmir", "Himachal Pradesh", "Punjab", "Uttarakhand", "Haryana",
    "Rajasthan", "Uttar Pradesh", "Bihar", "Sikkim", "Arunachal Pradesh",
    "Assam", "Nagaland", "Manipur", "Mizoram", "Tripura", "Meghalaya",
    "West Bengal", "Jharkhand", "Odisha", "Chhattisgarh", "Madhya Pradesh",
    "Gujarat", "Maharashtra", "Goa", "Karnataka", "Telangana",
    "Andhra Pradesh", "Kerala", "Tamil Nadu"
]

# Store previous state to simulate realistic trends (Random Walk)
state_data_store = {}

def get_trend_value(current_val, min_val, max_val, volatility=0.1):
    change = random.uniform(-volatility, volatility)
    new_val = current_val + change
    return max(min_val, min(new_val, max_val))

# Initialize store
for s in STATES:
    state_data_store[s] = {
        "wind": random.uniform(5, 20),
        "rain": random.uniform(0, 10),
        "prob": random.uniform(0.1, 0.4)
    }

@app.route("/live-risk")
def live_risk():
    data = []
    
    for state in STATES:
        # Update values with random walk
        prev = state_data_store[state]
        
        # Volatility varies by state (mock logic)
        vol = 0.5
        if state in ["Kerala", "Assam", "Odisha"]: vol = 1.5 # More volatile
        
        new_wind = round(get_trend_value(prev["wind"], 0, 120, vol), 1)
        new_rain = round(get_trend_value(prev["rain"], 0, 300, vol), 1)
        new_prob = round(get_trend_value(prev["prob"], 0.0, 1.0, 0.05), 2)
        
        # Determine Severity based on thresholds
        severity = "LOW"
        reasons = []
        
        if new_prob > 0.7 or (new_wind > 80 and new_rain > 100):
            severity = "HIGH"
            reasons.append("Critical wind speeds predicted")
            reasons.append("Heavy rainfall accumulation")
        elif new_prob > 0.4 or new_wind > 50:
            severity = "MEDIUM"
            reasons.append("Moderate storm capability")
        else:
            reasons.append("Conditions within safety norms")
            
        # Update store
        state_data_store[state] = {
            "wind": new_wind,
            "rain": new_rain,
            "prob": new_prob
        }
        
        data.append({
            "state": state,
            "severity": severity,
            "probability": new_prob,
            "wind_speed": new_wind,
            "rain_mm": new_rain,
            "reason": reasons,
            "last_updated": datetime.now().strftime("%H:%M:%S")
        })

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
