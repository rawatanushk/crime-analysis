# Geospatial Crime Analysis & Predictive Alerting System

A full-stack data science project that detects crime hotspots and 
predicts high-risk zones across Chicago using 1.4M+ real incident 
records, PostGIS spatial queries, DBSCAN clustering, and XGBoost.

## Live Features
- Interactive heatmap of crime density across Chicago
- Click any location on the map → real-time risk score
- Time-filter sliders (hour of day, month) to explore patterns
- Live alerts for currently high-risk districts
- Filter hotspots by crime type (Theft, Battery, Narcotics, Criminal Damage)

## Tech Stack
| Layer | Technology |
|---|---|
| Data | Chicago Crime Dataset — 1.4M+ real incidents |
| Database | PostgreSQL + PostGIS (hosted on Supabase) |
| Clustering | DBSCAN (scikit-learn) — 303 hotspots across 4 crime types |
| ML Model | XGBoost classifier |
| API | Flask REST (3 endpoints) |
| Frontend | Leaflet.js + OpenStreetMap |

## Model Performance
| Metric | Score |
|---|---|
| AUC-ROC | **0.8811** |
| Precision | 0.6744 |
| Recall | 0.5681 |
| F1 Score | 0.6167 |

## Key Insights
- **Hour and district** drive 80% of crime risk prediction
- **District 11 (Austin) at 8pm in August** → 95.4 risk score (HIGH)
- Narcotics crimes cluster most tightly (top cluster: 6,860 incidents)
- Crime drops to near zero between 4–6am city-wide

## API Endpoints
```
GET /hotspots          → GeoJSON of crime hotspot clusters
GET /predict           → Risk score for district/hour/month combo
GET /alerts            → Active high-risk districts at current hour
```

## Project Structure
```
crime-analysis/
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_hotspot_detection.ipynb
│   └── 04_prediction_model.ipynb
├── api/
│   ├── app.py
│   ├── db.py
│   └── routes/
│       ├── hotspots.py
│       ├── predict.py
│       └── alerts.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── map.js
├── data/
│   └── geojson/
├── .env.example
└── requirements.txt
```

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/rawatanushk/crime-analysis.git
cd crime-analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Fill in your Supabase DATABASE_URL
```

### 4. Run the API
```bash
cd api
python app.py
```

### 5. Open the dashboard
```bash
cd frontend
python -m http.server 3000
# Open http://127.0.0.1:3000
```

## Dataset
Chicago Crime Dataset —
https://www.kaggle.com/datasets/currie32/crimes-in-chicago

## Author
Anushk Rawat — B.Tech CSE (Data Science), UPES  
GitHub: [@rawatanushk](https://github.com/rawatanushk)