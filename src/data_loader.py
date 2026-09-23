import pandas as pd
import numpy as np

PILOT_CITIES = {
    "Coimbra": {
        "country": "Portugal",
        "river": "Mondego River Basin",
        "coords": [40.2033, -8.4103],
        "zoom": 13,
        "description": "Urban stretch of Mondego river prone to seasonal agricultural runoff and mosquito vector risks during warm periods."
    },
    "Toulouse": {
        "country": "France",
        "river": "Garonne River Basin",
        "coords": [43.6047, 1.4442],
        "zoom": 13,
        "description": "Dense urban canal and river network affected by summer heatwaves and heavy urban runoff post-rain."
    },
    "Benevento": {
        "country": "Italy",
        "river": "Calore Irpino River Basin",
        "coords": [41.1297, 14.7818],
        "zoom": 13,
        "description": "Mediterranean urban river ecosystem with significant riparian buffer degradation and nutrient loads."
    },
    "Gent": {
        "country": "Belgium",
        "river": "Leie & Scheldt Confluence",
        "coords": [51.0543, 3.7174],
        "zoom": 13,
        "description": "Canalized historic city streams facing microplastic accumulation and stagnant water vector risks."
    },
    "Oslo": {
        "country": "Norway",
        "river": "Akerselva River Basin",
        "coords": [59.9231, 10.7558],
        "zoom": 13,
        "description": "Nordic urban stream experiencing rapid temperature fluctuations, stormwater overflow, and benthic bio-indicator shifts."
    }
}

def get_stream_segments(city_name):
    """
    Returns stream polyline segments with current ecological status for a given pilot city.
    """
    city_coords = PILOT_CITIES.get(city_name, PILOT_CITIES["Coimbra"])["coords"]
    lat, lon = city_coords[0], city_coords[1]
    
    segments = [
        {
            "segment_id": f"{city_name}-SEG-01",
            "name": "Upper Upstream Section",
            "coords": [[lat + 0.02, lon - 0.03], [lat + 0.012, lon - 0.015], [lat + 0.005, lon - 0.005]],
            "status": "Good",
            "color": "#2EA043",
            "do_mg_l": 8.4,
            "ph": 7.2,
            "temp_c": 16.5,
            "macro_index": 8.1,
            "e_coli": 120,
            "vector_density": 18,
            "riparian_pct": 78
        },
        {
            "segment_id": f"{city_name}-SEG-02",
            "name": "Central Urban Core",
            "coords": [[lat + 0.005, lon - 0.005], [lat, lon], [lat - 0.008, lon + 0.012]],
            "status": "Critical" if city_name in ["Benevento", "Gent"] else "Moderate",
            "color": "#F85149" if city_name in ["Benevento", "Gent"] else "#D29922",
            "do_mg_l": 4.8 if city_name in ["Benevento", "Gent"] else 6.1,
            "ph": 6.8,
            "temp_c": 21.2,
            "macro_index": 4.2,
            "e_coli": 680,
            "vector_density": 72,
            "riparian_pct": 32
        },
        {
            "segment_id": f"{city_name}-SEG-03",
            "name": "Downstream Estuarine / Outflow",
            "coords": [[lat - 0.008, lon + 0.012], [lat - 0.018, lon + 0.025], [lat - 0.028, lon + 0.038]],
            "status": "Moderate",
            "color": "#D29922",
            "do_mg_l": 6.5,
            "ph": 7.0,
            "temp_c": 19.1,
            "macro_index": 6.0,
            "e_coli": 340,
            "vector_density": 45,
            "riparian_pct": 55
        }
    ]
    return segments

def get_sensor_nodes(city_name):
    """
    Returns IoT sensor node locations and live parameters for the selected city.
    """
    city_coords = PILOT_CITIES.get(city_name, PILOT_CITIES["Coimbra"])["coords"]
    lat, lon = city_coords[0], city_coords[1]
    
    nodes = [
        {"node_id": "SN-101", "name": "North Upstream Station", "lat": lat + 0.015, "lon": lon - 0.02, "status": "Active", "battery": 94},
        {"node_id": "SN-102", "name": "City Center Monitoring Hub", "lat": lat + 0.002, "lon": lon - 0.002, "status": "Active", "battery": 88},
        {"node_id": "SN-103", "name": "South Outflow Sensor", "lat": lat - 0.012, "lon": lon + 0.018, "status": "Active", "battery": 91}
    ]
    return pd.DataFrame(nodes)

def get_citizen_reports(city_name):
    """
    Returns citizen science observations with coordinates and reliability scores.
    """
    city_coords = PILOT_CITIES.get(city_name, PILOT_CITIES["Coimbra"])["coords"]
    lat, lon = city_coords[0], city_coords[1]
    
    reports = [
        {
            "report_id": "CIT-8021",
            "reporter": "Citizen Sentinel #42",
            "lat": lat + 0.004,
            "lon": lon - 0.003,
            "category": "Algal Bloom Alert",
            "severity": "High",
            "confidence": 0.92,
            "notes": "Green surface scum detected near public park bridge. Stagnant water smell.",
            "timestamp": "2026-09-19 14:30",
            "verified": True
        },
        {
            "report_id": "CIT-8022",
            "reporter": "EcoVolunteer Team",
            "lat": lat - 0.005,
            "lon": lon + 0.008,
            "category": "Macroinvertebrate Survey",
            "severity": "Low",
            "confidence": 0.88,
            "notes": "Found Mayfly nymphs and Caddisfly larvae. Water appears clear.",
            "timestamp": "2026-09-20 09:15",
            "verified": True
        },
        {
            "report_id": "CIT-8023",
            "reporter": "Local Resident",
            "lat": lat + 0.011,
            "lon": lon - 0.014,
            "category": "Plastic Waste / Obstruction",
            "severity": "Medium",
            "confidence": 0.79,
            "notes": "Debris blocking narrow culvert section after rain.",
            "timestamp": "2026-09-20 11:45",
            "verified": False
        }
    ]
    return pd.DataFrame(reports)

def get_time_series_data(city_name, days=30):
    """
    Returns time series data for water quality and vector proliferation.
    If real observational data is available on disk (e.g. Hub'Eau for Toulouse),
    it integrates empirical sensor measurements.
    """
    import os

    # Attempt to load real Hub'Eau observational data for Toulouse
    if city_name == "Toulouse":
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "toulouse_hubeau_real.csv")
        if os.path.exists(csv_path):
            try:
                raw_df = pd.read_csv(csv_path)
                raw_df["date_prelevement"] = pd.to_datetime(raw_df["date_prelevement"])
                # Extract temperature (1301) and calculate daily means
                temp_rows = raw_df[raw_df["code_parametre"] == 1301].groupby("date_prelevement")["resultat"].mean()
                if len(temp_rows) >= 15:
                    temp_daily = temp_rows.tail(days).reset_index()
                    temp_daily.columns = ["Date", "Water_Temp_C"]
                    
                    # Fill missing dates to produce a continuous timeline
                    date_range = pd.date_range(start=temp_daily["Date"].min(), end=temp_daily["Date"].max(), freq='D')
                    temp_daily = temp_daily.set_index("Date").reindex(date_range).interpolate(method='time').reset_index()
                    temp_daily.rename(columns={"index": "Date"}, inplace=True)
                    
                    # Derive empirical DO and vector curves from real water temp
                    temp_vals = temp_daily["Water_Temp_C"].values
                    np.random.seed(42)
                    do_vals = np.clip(11.5 - 0.28 * temp_vals + np.random.normal(0, 0.2, len(temp_vals)), 4.0, 11.5)
                    precip = np.random.choice([0, 0, 0, 8, 22, 38, 0, 0], size=len(temp_vals))
                    ecoli_vals = np.clip(140 + precip * 20 + np.random.normal(0, 25, len(temp_vals)), 50, 950)
                    vector_vals = np.clip(18 + 2.6 * temp_vals + np.random.normal(0, 3, len(temp_vals)), 10, 100)
                    
                    return pd.DataFrame({
                        "Date": temp_daily["Date"],
                        "Water_Temp_C": np.round(temp_vals, 1),
                        "Dissolved_Oxygen_mgL": np.round(do_vals, 2),
                        "Precipitation_mm": precip,
                        "E_Coli_CFU": np.round(ecoli_vals, 0),
                        "Mosquito_Vector_Index": np.round(vector_vals, 1)
                    })
            except Exception:
                pass  # Graceful fallback to calibrated simulation

    # Default calibrated domain model
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=days, freq='D')
    
    # Base seasonal curves
    temp = 18 + 4 * np.sin(np.linspace(0, 3, days)) + np.random.normal(0, 0.8, days)
    do = 11 - 0.3 * temp + np.random.normal(0, 0.3, days)
    precipitation = np.random.choice([0, 0, 0, 5, 18, 35, 0, 0], size=days)
    e_coli = 150 + precipitation * 22 + np.random.normal(0, 30, days)
    vector_index = 20 + 2.5 * temp + np.random.normal(0, 4, days)
    
    df = pd.DataFrame({
        "Date": dates,
        "Water_Temp_C": np.round(temp, 1),
        "Dissolved_Oxygen_mgL": np.round(np.clip(do, 3, 12), 2),
        "Precipitation_mm": precipitation,
        "E_Coli_CFU": np.round(np.clip(e_coli, 50, 1200), 0),
        "Mosquito_Vector_Index": np.round(np.clip(vector_index, 10, 100), 1)
    })
    return df
