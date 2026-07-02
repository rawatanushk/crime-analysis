from flask import Blueprint, jsonify, request
from db import get_connection
from sqlalchemy import text

hotspots_bp = Blueprint('hotspots', __name__)

@hotspots_bp.route('/hotspots', methods=['GET'])
def get_hotspots():
    # Optional filter by crime type
    crime_type = request.args.get('crime_type', None)
    
    try:
        with get_connection() as conn:
            if crime_type:
                query = text("""
                    SELECT crime_type, 
                           AVG(latitude) as center_lat,
                           AVG(longitude) as center_lon,
                           COUNT(*) as crime_count,
                           district
                    FROM crime_incidents
                    WHERE crime_type = :crime_type
                    GROUP BY crime_type, district
                    HAVING COUNT(*) > 100
                    ORDER BY crime_count DESC
                    LIMIT 50
                """)
                result = conn.execute(query, {"crime_type": crime_type})
            else:
                query = text("""
                    SELECT crime_type,
                           AVG(latitude) as center_lat,
                           AVG(longitude) as center_lon,
                           COUNT(*) as crime_count,
                           district
                    FROM crime_incidents
                    GROUP BY crime_type, district
                    HAVING COUNT(*) > 500
                    ORDER BY crime_count DESC
                    LIMIT 100
                """)
                result = conn.execute(query)
            
            rows = result.fetchall()
            
            # Build GeoJSON response
            features = []
            for row in rows:
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(row.center_lon), float(row.center_lat)]
                    },
                    "properties": {
                        "crime_type": row.crime_type,
                        "crime_count": int(row.crime_count),
                        "district": int(row.district) if row.district else None
                    }
                }
                features.append(feature)
            
            return jsonify({
                "type": "FeatureCollection",
                "count": len(features),
                "features": features
            })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500