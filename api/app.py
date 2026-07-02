from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv('../.env')

app = Flask(__name__)
CORS(app)  # allows your Leaflet frontend to call this API

from routes.hotspots import hotspots_bp
from routes.predict import predict_bp
from routes.alerts import alerts_bp

app.register_blueprint(hotspots_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(alerts_bp)

@app.route('/')
def index():
    return {
        "project": "Geospatial Crime Analysis API",
        "version": "1.0",
        "endpoints": ["/hotspots", "/predict", "/alerts"]
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)