from flask import Blueprint, jsonify
from db import get_connection
from sqlalchemy import text
from datetime import datetime

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/alerts', methods=['GET'])
def get_alerts():
    # Get current hour and day automatically
    now = datetime.now()
    current_hour = now.hour
    current_day = now.weekday()
    current_month = now.month
    
    try:
        with get_connection() as conn:
            query = text("""
                SELECT district, risk_score, hour, day_of_week, month
                FROM district_risk_scores
                WHERE hour = :hour
                AND day_of_week = :day
                AND month = :month
                AND risk_score >= 70
                ORDER BY risk_score DESC
                LIMIT 10
            """)
            
            result = conn.execute(query, {
                "hour": current_hour,
                "day": current_day,
                "month": current_month
            })
            
            rows = result.fetchall()
            
            alerts = []
            for row in rows:
                alerts.append({
                    "district": int(row.district),
                    "risk_score": float(row.risk_score),
                    "risk_level": "HIGH",
                    "hour": int(row.hour),
                    "message": f"District {int(row.district)} has high crime risk at hour {int(row.hour):02d}:00"
                })
            
            return jsonify({
                "timestamp": now.isoformat(),
                "current_hour": current_hour,
                "alert_count": len(alerts),
                "alerts": alerts
            })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    