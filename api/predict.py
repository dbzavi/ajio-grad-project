from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

@app.route('/api/predict', methods=['POST'])
def predict_size():
    time.sleep(1.5)
    data = request.json
    height_ft = data.get('height_ft', 5)
    height_in = data.get('height_in', 5)
    weight = data.get('weight', 60)
    body_shape = data.get('body_shape', 'pear')
    fit_pref = data.get('fit_pref', 'regular')

    recommended_size = "M"
    confidence = 88
    insight = "Based on 1,204 reviews, this runs slightly large."
    
    total_inches = (height_ft * 12) + height_in
    if total_inches > 68 or weight > 75:
        recommended_size = "L"
        confidence = 91
        if fit_pref == "loose":
            recommended_size = "XL"
            confidence = 85
        insight = "Reviewers with your height/weight mention the sleeves run short. We recommend sizing up for comfort."
    elif total_inches < 62 or weight < 50:
        recommended_size = "S"
        confidence = 94
        if fit_pref == "tight":
            recommended_size = "XS"
        insight = "This jacket has a naturally oversized fit. Based on your profile, sizing down is recommended."
    else:
        recommended_size = "M"
        confidence = 92
        if fit_pref == "loose":
            recommended_size = "L"
            confidence = 89
        insight = "A Medium provides the perfect oversized look for your build without overwhelming your frame."

    return jsonify({
        "recommended_size": recommended_size,
        "confidence_score": confidence,
        "insight_summary": insight
    })
