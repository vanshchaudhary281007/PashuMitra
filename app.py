from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import time
import os

app = Flask(__name__, static_folder='.')
CORS(app)



MODEL_PATH = "best.pkl"   
model      = None
le_target  = None


print("[MODEL] Running in DEMO MODE — real model not loaded")
print("[SERVER] PashuMitra backend starting...")




DISEASE_DATA = {
    "Mastitis_Clinical": {
        "severity": "Critical",
        "urgency": "Call vet immediately",
        "action": "Isolate milk from main supply. Begin CMT test on all quarters. Intramammary antibiotic treatment required.",
        "color": "red"
    },
    "Foot_and_Mouth": {
        "severity": "Critical",
        "urgency": "Call vet immediately",
        "action": "Isolate animal from herd. Check vaccination records. Notify local animal husbandry department.",
        "color": "red"
    },
    "Bloat": {
        "severity": "Moderate",
        "urgency": "Act within 2 hours",
        "action": "Restrict green fodder. Walk the animal slowly. Insert stomach tube if severe. Call vet if not relieved in 30 min.",
        "color": "orange"
    },
    "Milk_Fever": {
        "severity": "Critical",
        "urgency": "Call vet immediately",
        "action": "IV calcium infusion required. Keep animal warm. Avoid stress. Vet must administer treatment.",
        "color": "red"
    },
    "Pneumonia": {
        "severity": "Moderate",
        "urgency": "Vet visit within 24 hours",
        "action": "Move animal to dry, ventilated shelter. Antibiotic treatment required. Monitor temperature every 4 hours.",
        "color": "orange"
    },
    "Ketosis_Clinical": {
        "severity": "Moderate",
        "urgency": "Vet visit within 24 hours",
        "action": "Oral propylene glycol 300ml twice daily. Increase energy-dense feed. Reduce milking frequency temporarily.",
        "color": "orange"
    },
    "Diarrhea": {
        "severity": "Mild",
        "urgency": "Monitor closely",
        "action": "Provide oral rehydration solution. Withhold feed for 12 hours. Offer clean fresh water. Call vet if persists over 48 hours.",
        "color": "yellow"
    },
    "Heat_Stress": {
        "severity": "Mild",
        "urgency": "Act today",
        "action": "Ensure shade and cool water. Install fans or sprinklers. Reduce concentrate feed. Reschedule milking to cooler hours.",
        "color": "yellow"
    },
    "Healthy": {
        "severity": "None",
        "urgency": "No action needed",
        "action": "Animal appears healthy. Continue regular feeding and milking schedule. Next checkup in 7 days.",
        "color": "green"
    },
    "Internal_Parasites": {
        "severity": "Mild",
        "urgency": "Within this week",
        "action": "Administer Albendazole as per body weight. Repeat after 3 months. Improve pasture hygiene.",
        "color": "yellow"
    }
}

SYMPTOM_DISEASE_MAP = {
    ("sym_swollen_udder", "sym_abnormal_milk", "sym_low_milk"): "Mastitis_Clinical",
    ("sym_limping", "sym_nasal_discharge", "sym_not_eating"):   "Foot_and_Mouth",
    ("sym_bloating", "sym_restless"):                           "Bloat",
    ("sym_not_eating", "sym_weight_loss", "sym_low_milk"):      "Ketosis_Clinical",
    ("sym_coughing", "sym_nasal_discharge", "sym_fever"):       "Pneumonia",
    ("sym_diarrhea",):                                          "Diarrhea",
    ("sym_restless", "sym_fever"):                              "Heat_Stress",
}




def demo_predict(data):
    time.sleep(1.2)

   
    predicted = "Mastitis_Clinical"

    disease_info = DISEASE_DATA[predicted]

    return {
        "predicted_disease": predicted,
        "confidence": 0.92,
        "severity": disease_info["severity"],
        "urgency": disease_info["urgency"],
        "recommended_action": disease_info["action"],
        "color": disease_info["color"],
        "top3": [
            {"disease": "Mastitis_Clinical", "probability": 0.92},
            {"disease": "Healthy", "probability": 0.05},
            {"disease": "Internal_Parasites", "probability": 0.03},
        ],
        "model_mode": "DEMO",
        "symptoms_detected": 3
    }
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status":     "running",
        "model":      "DEMO MODE" if model is None else "LOADED",
        "model_path": MODEL_PATH,
        "version":    "1.0.0"
    })


@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400

        

        result = demo_predict(data)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/milk-predict', methods=['POST'])
def milk_predict():
    try:
        data = request.get_json()
        # Demo: simple formula-based estimate
        base       = 8.5
        feed_bonus = (data.get('feed_quantity_kg', 12) - 12) * 0.3
        dim_factor = 1.0 if data.get('days_in_milk', 60) < 120 else 0.85
        predicted  = round(max(0, (base + feed_bonus) * dim_factor + random.uniform(-0.5, 0.5)), 1)

        return jsonify({
            "predicted_yield_L": predicted,
            "confidence": round(random.uniform(0.78, 0.91), 2),
            "model_mode": "DEMO"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("[SERVER] Starting on http://localhost:5000")
    app.run(debug=True, port=5000)
