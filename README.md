# OneAqua Insight Hub

A personal project built for the **IEEE OneAquaHealth Global Hackathon 2026 (Track 2: Data-to-Insight)**.

The idea behind this dashboard is straightforward: connect urban stream health with public health and climate stress across European cities, rather than looking at water quality in isolation. It brings together open environmental datasets, in-situ sensor telemetry, and citizen science reports into a unified decision-support tool.

The app focuses on 5 official EU pilot catchments:
- **Coimbra, Portugal** (Mondego Basin)
- **Toulouse, France** (Garonne Basin)
- **Benevento, Italy** (Calore Irpino Basin)
- **Gent, Belgium** (Scheldt & Leie Confluence)
- **Oslo, Norway** (Akerselva Basin)

---

## What it does

- **Geospatial Map**: Folium-based map showing stream segments color-coded by water quality, along with IoT sensor stations and crowd-sourced citizen reports.
- **One Health Vitality Score**: A composite metric combining:
  - **Ecological Health Index (EHI)**: Dissolved oxygen, macroinvertebrate indicators, and riparian buffer coverage.
  - **Human Health Risk Index (HHRI)**: Microbial pathogen counts (E. coli) and mosquito vector breeding risks.
  - **Urban Climate Stress Index (UCSI)**: Urban heat island anomalies and stormwater runoff pressures.
- **Scenario Sandbox**: Sliders to test "what-if" situations like summer heatwaves, heavy storm runoff, or adding riparian vegetation to see how the scores react.
- **Time-Series Analytics**: Interactive multi-axis charts comparing temperature vs. dissolved oxygen and precipitation spikes vs. bacterial loads.
- **Policy Brief Exporter**: Generates a clean markdown summary outlining current stream status and suggested mitigation steps.

---

## Data Sources

The project pulls from real open-access European environmental portals:
- **Toulouse**: Hub'Eau API / Naïades (French national water quality database)
- **Gent**: GBIF & VMM (Flanders Environment Agency macroinvertebrate records)
- **Benevento**: ARPAC Campania Open Data Portal (surface water monitoring)
- **Coimbra**: SNIRH (Portuguese national water resources information system)
- **Oslo**: NVE HydAPI (Akerselva Brekkefossen station)

You can re-fetch or update the cached datasets anytime by running:
```bash
python scripts/fetch_all_cities_data.py
```

---

## Project Structure

```text
OneAqua-Insight-Hub/
├── app.py                      # Main Streamlit dashboard
├── src/
│   ├── engine.py               # Composite scoring math and summary generator
│   ├── data_loader.py          # Data loaders and city configurations
│   ├── styles.py               # Custom UI styles (dark theme, cards)
│   └── components/
│       ├── map_view.py         # GIS map component
│       ├── matrix_view.py      # Scorecards and telemetry badges
│       ├── analytics_view.py   # Plotly charts and correlation matrix
│       ├── simulator_view.py   # Sidebar scenario controls
│       └── policy_view.py      # Policy summary and export
├── data/                       # Cached open datasets for the 5 cities
├── scripts/                    # Helper scripts for fetching open data
├── requirements.txt            # Python dependencies
└── README.md
```

---

## Getting Started

### 1. Clone & set up environment
```bash
git clone https://github.com/aliirtaza58/oneaqua-insight-hub.git
cd oneaqua-insight-hub

python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Optional: Add a CARTO map key
If you have a free CARTO basemaps API key, add it to `.streamlit/secrets.toml`:
```toml
MAP_API_KEY = "your_carto_key_here"
```
*(If omitted, the app will fall back to default dark basemaps.)*

### 3. Run the app
```bash
streamlit run app.py
```

---

## License
MIT License.
