const API_BASE = 'http://127.0.0.1:5000';
const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

// Init map centered on Chicago
const map = L.map('map').setView([41.85, -87.65], 11);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

let hotspotLayer = null;
let heatLayer = null;

// --- Sliders ---
const hourSlider = document.getElementById('hourSlider');
const monthSlider = document.getElementById('monthSlider');

hourSlider.addEventListener('input', () => {
  document.getElementById('hourValue').textContent = hourSlider.value.padStart(2, '0');
});

monthSlider.addEventListener('input', () => {
  document.getElementById('monthValue').textContent = MONTHS[monthSlider.value - 1];
});

// --- Load Hotspots ---
document.getElementById('loadHotspotsBtn').addEventListener('click', async () => {
  const crimeType = document.getElementById('crimeTypeFilter').value;
  const url = crimeType 
    ? `${API_BASE}/hotspots?crime_type=${encodeURIComponent(crimeType)}`
    : `${API_BASE}/hotspots`;

  try {
    const res = await fetch(url);
    const data = await res.json();

    // Clear existing layers
    if (hotspotLayer) map.removeLayer(hotspotLayer);
    if (heatLayer) map.removeLayer(heatLayer);

    // Build heatmap data
    const heatData = data.features.map(f => [
      f.geometry.coordinates[1],
      f.geometry.coordinates[0],
      Math.min(f.properties.crime_count / 1000, 1.0)
    ]);
    heatLayer = L.heatLayer(heatData, { radius: 35, blur: 25, maxZoom: 13 }).addTo(map);

    // Add circle markers with popups
    hotspotLayer = L.geoJSON(data, {
      pointToLayer: (feature, latlng) => {
        const count = feature.properties.crime_count;
        const radius = Math.min(Math.max(count / 2000, 4), 18);
        return L.circleMarker(latlng, {
          radius,
          fillColor: '#e94560',
          color: '#fff',
          weight: 1,
          opacity: 0.8,
          fillOpacity: 0.7
        });
      },
      onEachFeature: (feature, layer) => {
        const p = feature.properties;
        layer.bindPopup(`
          <strong>${p.crime_type}</strong><br>
          District: ${p.district}<br>
          Incidents: ${p.crime_count.toLocaleString()}
        `);
      }
    }).addTo(map);

  } catch (err) {
    alert('Error loading hotspots: ' + err.message);
  }
});

// --- Predict Risk on Map Click ---
map.on('click', async (e) => {
  const hour = parseInt(hourSlider.value);
  const month = parseInt(monthSlider.value);
  const dayOfWeek = new Date().getDay();
  const isWeekend = (dayOfWeek === 0 || dayOfWeek === 6) ? 1 : 0;

  // Use district 1 as default (no reverse geocoding yet)
  const url = `${API_BASE}/predict?district=1&hour=${hour}&day_of_week=${dayOfWeek}&month=${month}&is_weekend=${isWeekend}`;

  try {
    const res = await fetch(url);
    const data = await res.json();
    showRiskResult(data);

    L.popup()
      .setLatLng(e.latlng)
      .setContent(`
        <strong>Risk Score: ${data.risk_score}</strong><br>
        Level: <span style="color:${data.risk_level === 'HIGH' ? '#e94560' : data.risk_level === 'MEDIUM' ? '#f5a623' : '#4caf50'}">${data.risk_level}</span><br>
        Hour: ${hour}:00 | Month: ${MONTHS[month-1]}
      `)
      .openOn(map);
  } catch (err) {
    console.error(err);
  }
});

// --- Predict Button ---
document.getElementById('predictBtn').addEventListener('click', async () => {
  const hour = parseInt(hourSlider.value);
  const month = parseInt(monthSlider.value);
  const dayOfWeek = new Date().getDay();
  const isWeekend = (dayOfWeek === 0 || dayOfWeek === 6) ? 1 : 0;

  const url = `${API_BASE}/predict?district=11&hour=${hour}&day_of_week=${dayOfWeek}&month=${month}&is_weekend=${isWeekend}`;

  try {
    const res = await fetch(url);
    const data = await res.json();
    showRiskResult(data);
  } catch (err) {
    alert('Error: ' + err.message);
  }
});

// --- Alerts Button ---
document.getElementById('loadAlertsBtn').addEventListener('click', async () => {
  try {
    const res = await fetch(`${API_BASE}/alerts`);
    const data = await res.json();
    
    const panel = document.getElementById('alertsPanel');
    const list = document.getElementById('alertsList');
    panel.classList.remove('hidden');

    if (data.alerts.length === 0) {
      list.innerHTML = '<p style="color:#888;font-size:12px">No high-risk alerts at this hour.</p>';
    } else {
      list.innerHTML = data.alerts.map(a => `
        <div class="alert-item">
          <strong>District ${a.district}</strong> — Score: ${a.risk_score}<br>
          ${a.message}
        </div>
      `).join('');
    }
  } catch (err) {
    alert('Error: ' + err.message);
  }
});

// --- Show Risk Result in Sidebar ---
function showRiskResult(data) {
  document.getElementById('riskResult').classList.remove('hidden');
  document.getElementById('riskScore').textContent = data.risk_score;
  
  const levelEl = document.getElementById('riskLevel');
  levelEl.textContent = data.risk_level;
  levelEl.className = `risk-level ${data.risk_level}`;
  
  document.getElementById('riskInfo').textContent = 
    `District ${data.district} | ${String(data.hour).padStart(2,'0')}:00 | Month ${data.month}`;
}