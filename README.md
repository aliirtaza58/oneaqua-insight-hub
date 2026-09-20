# 🌊 OneAqua Insight Hub
> **IEEE OneAquaHealth Global Hackathon 2026 Submission**  
> **Track 2: Data-to-Insight**

![OneAquaHealth Alignment](https://img.shields.io/badge/IEEE%20Hackathon-OneAquaHealth-00F2FE?style=for-the-badge)
![Track Alignment](https://img.shields.io/badge/Track-Data--to--Insight-blueviolet?style=for-the-badge)
![Python Streamlit](https://img.shields.io/badge/Built%20With-Streamlit%20%7C%20Folium%20%7C%20Plotly-00C853?style=for-the-badge)

---

## 📌 Executive Summary

**OneAqua Insight Hub** is a decision-support and geospatial analytics platform built for the **IEEE OneAquaHealth Global Hackathon 2026**. It harmonizes citizen science observations, environmental sensor streams, and urban climate data into actionable **One Health insights** linking urban freshwater ecosystem health directly to human and community well-being.

Aligned with the Horizon Europe [OneAquaHealth Project](https://www.oneaquahealth.eu/), the platform features empirical monitoring frameworks across **5 European Pilot Cities**:
1. **Coimbra** (Portugal)
2. **Toulouse** (France)
3. **Benevento** (Italy)
4. **Gent** (Belgium)
5. **Oslo** (Norway)

---

## 🎯 Key Features

- 🗺️ **Geospatial Intelligence Map**: Multi-layer GIS rendering stream segment polylines, water quality sensor nodes, mosquito vector risk heatmaps, and citizen observation reports.
- 🩺 **One Health Composite Matrix**: Real-time evaluation of:
  - **Ecological Health Index (EHI)**: Dissolved oxygen, pH, benthic macroinvertebrates, and riparian buffer index.
  - **Human Health Risk Index (HHRI)**: Pathogen/E. coli load, Diptera/Mosquito vector density, and cyanobacteria bloom alerts.
  - **Urban Climate Stress Index (UCSI)**: Urban heat island delta and stormwater runoff capacity.
- 🤖 **Automated AI Policy Synthesizer**: Generates plain-language executive summaries and threshold-triggered risk advisories for municipal authorities and researchers.
- ⚡ **"What-If" Climate & Resilience Simulator**: Interactive scenario sandbox allowing users to model extreme rainfall, heatwave spikes, and green infrastructure restoration.
- 📄 **Executive Policy Brief Exporter**: One-click downloadable One Health policy reports.

---

## 🏗️ Repository Architecture

```text
OneAqua-Insight-Hub/
├── .streamlit/
│   └── config.toml         # Dark slate theme & port settings
├── src/
│   ├── styles.py           # Custom CSS injection (glassmorphism UI)
│   ├── data_loader.py      # Stream segments & sensor telemetry loader
│   ├── engine.py           # Composite index models & narrative generator
│   └── components/
│       ├── map_view.py     # Interactive Folium map renderer
│       ├── matrix_view.py  # One Health scorecards & KPI widgets
│       ├── analytics_view.py # Plotly time-series analytics
│       ├── simulator_view.py # "What-If" scenario sandbox
│       └── policy_view.py  # Policy brief exporter
├── app.py                  # Main Streamlit application entry point
├── requirements.txt        # Python dependency manifest
└── README.md               # Project documentation & setup guide
```

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
- Python 3.10 or higher
- Git

### Installation
```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/oneaqua-insight-hub.git
cd oneaqua-insight-hub

# 2. Create and activate virtual environment
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch application
streamlit run app.py
```

---

## 📊 One Health Mathematical Framework

$$EHI = 0.35 \cdot DO_{\text{norm}} + 0.25 \cdot \text{BioIndex} + 0.20 \cdot \text{pH}_{\text{norm}} + 0.20 \cdot \text{RiparianBuffer}$$

$$HHRI = 0.40 \cdot \text{PathogenRisk} + 0.35 \cdot \text{VectorDensity} + 0.25 \cdot \text{CyanobacteriaAlert}$$

---

## 📜 License
This project is developed for the **IEEE OneAquaHealth Global Hackathon 2026** under the MIT License.
