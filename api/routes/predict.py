from flask import Blueprint, jsonify, request
from db import get_connection
from sqlalchemy import text
import joblib
import numpy as np
import os

predict_bp = Blueprint('predict', __name__)

# Load model once when server starts
model_path = os.path.join(os.path.dirname(__file__), '../../models/crime_risk_model.pkl')
model = joblib.load(model_path)

@predict_bp.route('/predict', methods=['GET'])
def predict_risk():
    try:
        # Get parameters from request
        district = int(request.args.get('district', 1))
        hour = int(request.args.get('hour', 12))
        day_of_week = int(request.args.get('day_of_week', 0))
        month = int(request.args.get('month', 6))
        is_weekend = int(request.args.get('is_weekend', 0))
        
        # Validate inputs
        if not (0 <= hour <= 23):
            return jsonify({"error": "hour must be 0-23"}), 400
        if not (0 <= day_of_week <= 6):
            return jsonify({"error": "day_of_week must be 0-6"}), 400
        if not (1 <= month <= 12):
            return jsonify({"error": "month must be 1-12"}), 400

        # Make prediction
        features = np.array([[district, hour, day_of_week, month, is_weekend]])
        risk_proba = model.predict_proba(features)[0][1]
        risk_score = round(float(risk_proba) * 100, 1)
        
        # Risk level label
        if risk_score >= 70:
            risk_level = "HIGH"
        elif risk_score >= 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return jsonify({
            "district": district,
            "hour": hour,
            "day_of_week": day_of_week,
            "month": month,
            "is_weekend": bool(is_weekend),
            "risk_score": risk_score,
            "risk_level": risk_level
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500