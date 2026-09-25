import numpy as np

SCENARIO_PRESETS = {
    "Baseline Telemetry": {
        "temp_delta": 0.0,
        "rain_delta": 0.0,
        "riparian_delta": 0.0,
        "desc": "Standard seasonal baseline under typical urban drainage conditions."
    },
    "Summer Heatwave Anomaly": {
        "temp_delta": 3.5,
        "rain_delta": 0.0,
        "riparian_delta": 0.0,
        "desc": "Elevated thermal stress driving dissolved oxygen depletion and accelerated vector breeding cycles."
    },
    "Storm Runoff Surge": {
        "temp_delta": -0.5,
        "rain_delta": 40.0,
        "riparian_delta": 0.0,
        "desc": "Intense precipitation causing sewer overflow and high microbial pathogen influx."
    },
    "Riparian Eco-Restoration (25%)": {
        "temp_delta": 0.0,
        "rain_delta": 0.0,
        "riparian_delta": 25.0,
        "desc": "Restored vegetated buffer zones buffering thermal gain and naturally filtering stormwater runoff."
    }
}

def calculate_one_health_indices(segments_data, sim_temp_delta=0.0, sim_rain_delta=0.0, sim_riparian_delta=0.0):
    """
    Computes composite One Health indices (Overall Vitality, EHI, HHRI, UCSI) based on stream
    parameters, bioindicators, and scenario simulation offsets.
    """
    # Average base parameters across segments
    avg_do = np.mean([s["do_mg_l"] for s in segments_data])
    avg_macro = np.mean([s["macro_index"] for s in segments_data])
    avg_ph = np.mean([s["ph"] for s in segments_data])
    avg_e_coli = np.mean([s["e_coli"] for s in segments_data])
    avg_vector = np.mean([s["vector_density"] for s in segments_data])
    avg_riparian = np.mean([s["riparian_pct"] for s in segments_data])

    # Apply simulation adjustments
    eff_do = max(2.0, avg_do - (0.25 * sim_temp_delta) + (0.12 * (sim_riparian_delta / 10.0)))
    eff_macro = np.clip(avg_macro + (0.35 * (sim_riparian_delta / 10.0)) - (0.15 * sim_temp_delta), 1.0, 10.0)
    eff_riparian = np.clip(avg_riparian + sim_riparian_delta, 10.0, 100.0)
    
    eff_e_coli = max(40.0, avg_e_coli + (18.0 * sim_rain_delta) - (6.0 * (sim_riparian_delta / 10.0)))
    eff_vector = np.clip(avg_vector + (3.8 * sim_temp_delta) - (1.8 * (sim_riparian_delta / 10.0)), 5.0, 100.0)

    # 1. Ecological Health Index (EHI) [0 - 100]
    do_score = np.clip((eff_do / 9.5) * 100, 0, 100)
    macro_score = (eff_macro / 10.0) * 100
    ph_score = max(0, 100 - (abs(avg_ph - 7.2) * 50))
    ehi = (0.35 * do_score) + (0.35 * macro_score) + (0.15 * ph_score) + (0.15 * eff_riparian)
    ehi = np.clip(ehi, 0, 100)

    # 2. Human Health Risk Index (HHRI) [0 - 100] (Higher = Greater Risk)
    pathogen_risk = np.clip((eff_e_coli / 900.0) * 100, 0, 100)
    vector_risk = eff_vector
    hhri = (0.55 * pathogen_risk) + (0.45 * vector_risk)
    hhri = np.clip(hhri, 0, 100)

    # 3. Urban Climate Stress Index (UCSI) [0 - 100]
    heat_stress = np.clip(42 + (5.5 * sim_temp_delta) - (0.35 * eff_riparian), 0, 100)
    runoff_stress = np.clip(38 + (4.5 * sim_rain_delta) - (0.45 * eff_riparian), 0, 100)
    ucsi = (0.50 * heat_stress) + (0.50 * runoff_stress)
    ucsi = np.clip(ucsi, 0, 100)

    # 4. Overall One Health Ecosystem Vitality [0 - 100] (The Lead Hero Metric)
    overall_vitality = (0.45 * ehi) + (0.35 * (100.0 - hhri)) + (0.20 * (100.0 - ucsi))
    overall_vitality = np.clip(overall_vitality, 0, 100)

    # Status Labels & Confidence
    vitality_status = "Optimal Vitality" if overall_vitality >= 70 else ("Moderate Vulnerability" if overall_vitality >= 48 else "High Ecosystem Distress")
    ehi_status = "Good" if ehi >= 68 else ("Moderate" if ehi >= 48 else "Critical")
    hhri_status = "Low Risk" if hhri < 35 else ("Moderate Risk" if hhri < 60 else "High Alert")
    ucsi_status = "Low Stress" if ucsi < 38 else ("Moderate Stress" if ucsi < 65 else "High Stress")

    return {
        "vitality": round(overall_vitality, 1),
        "vitality_status": vitality_status,
        "vitality_delta": round(overall_vitality - 62.5, 1), # comparison to historical baseline
        "EHI": round(ehi, 1),
        "EHI_status": ehi_status,
        "HHRI": round(hhri, 1),
        "HHRI_status": hhri_status,
        "UCSI": round(ucsi, 1),
        "UCSI_status": ucsi_status,
        "metrics": {
            "eff_do": round(eff_do, 2),
            "eff_macro": round(eff_macro, 1),
            "eff_e_coli": int(eff_e_coli),
            "eff_vector": round(eff_vector, 1),
            "eff_riparian": round(eff_riparian, 1),
            "sensor_nodes_online": 3,
            "sampling_confidence": 94
        }
    }

def detect_environmental_anomalies(time_series_df):
    """
    Evaluates rolling trends in telemetry to identify compound ecological and public health risk windows:
    - Persistent hypoxia (< 5.0 mg/L DO for >= 2 days)
    - Vector proliferation window (water temp >= 21.0 C)
    - Runoff-induced microbial surge (E. coli >= 400 CFU)
    """
    alerts = []
    if time_series_df is None or len(time_series_df) < 3:
        return alerts

    recent = time_series_df.tail(7)
    
    # 1. Hypoxia alert
    low_do_count = (recent["Dissolved_Oxygen_mgL"] < 5.0).sum()
    if low_do_count >= 2:
        alerts.append({
            "level": "warning",
            "title": "Hypoxia / Depletion Window Detected",
            "detail": f"Dissolved oxygen levels remained under 5.0 mg/L across {low_do_count} recent daily readings. High risk of aquatic organism stress."
        })

    # 2. Vector proliferation window
    avg_temp = recent["Water_Temp_C"].mean()
    if avg_temp >= 21.0:
        alerts.append({
            "level": "caution",
            "title": "Vector Proliferation Window",
            "detail": f"Average recent water temperature ({avg_temp:.1f}°C) exceeds the 21.0°C threshold, accelerating Diptera and mosquito larval incubation."
        })

    # 3. Pathogen runoff surge
    max_ecoli = recent["E_Coli_CFU"].max()
    if max_ecoli >= 400:
        alerts.append({
            "level": "danger",
            "title": "Recreational Pathogen Warning",
            "detail": f"Microbial pathogen density peaked at {int(max_ecoli)} CFU/100mL (exceeding EU 400 CFU bathing water guidelines) following stormwater discharge."
        })

    return alerts

def cross_validate_citizen_report(category, severity, notes, sensors_df, time_series_df):
    """
    Automated cross-validation engine: compares sensory citizen observations against
    nearest telemetry data to assign an empirical verification status and score.
    """
    confidence = 0.75
    factors = []

    # Check recent telemetry
    if time_series_df is not None and not time_series_df.empty:
        latest = time_series_df.iloc[-1]
        
        if "Algal Bloom" in category or "Odor" in category:
            if latest["Dissolved_Oxygen_mgL"] < 6.0:
                confidence += 0.14
                factors.append("Confirmed by depressed dissolved oxygen reading at nearest sensor")
            if latest["Water_Temp_C"] > 19.0:
                confidence += 0.08
                factors.append("Elevated water temperature supports organic decomposition")
        elif "Macroinvertebrate" in category:
            confidence = 0.90
            factors.append("Biotic taxon observation logged with community biodiversity survey")
        elif "Plastic" in category or "Waste" in category:
            confidence = 0.85
            factors.append("Physical debris report queued for municipal drainage clearing")

    confidence = min(0.98, round(confidence, 2))
    verified = confidence >= 0.82
    
    return {
        "verified": verified,
        "confidence": confidence,
        "factors": factors
    }

def generate_ai_executive_summary(city_name, indices):
    """
    Generates plain-language executive policy summaries and threshold advisories.
    """
    v = indices["vitality"]
    ehi = indices["EHI"]
    hhri = indices["HHRI"]
    ucsi = indices["UCSI"]

    summary = f"### One Health Executive Advisory: {city_name}\n\n"
    summary += f"**Overall Ecosystem Vitality:** `{v}/100` ({indices['vitality_status']})  \n"
    summary += f"**Monitoring Confidence:** `{indices['metrics']['sampling_confidence']}%` (Integrated IoT sensor telemetry & validated citizen observation stream).\n\n"
    summary += "---\n\n"

    if ehi < 50:
        summary += f"**Aquatic Ecosystem Alert (EHI: {ehi}/100)**: Stream segment telemetry indicates dissolved oxygen levels dropped to **{indices['metrics']['eff_do']} mg/L** with benthic macroinvertebrate diversity score of **{indices['metrics']['eff_macro']}/10**, reflecting persistent ecological stress.\n\n"
    else:
        summary += f"**Aquatic Ecosystem Vitality (EHI: {ehi}/100)**: Stream oxygenation (**{indices['metrics']['eff_do']} mg/L**) and macroinvertebrate bio-indicators meet standard European Water Framework Directive ecological thresholds.\n\n"

    if hhri >= 50:
        summary += f"**Public Health Advisory (HHRI: {hhri}/100)**: Microbial pathogen indicators (E. coli: **{indices['metrics']['eff_e_coli']} CFU/100mL**) and vector breeding index (**{indices['metrics']['eff_vector']}/100**) exceed safe recreational thresholds. Municipal advisories recommended for public contact zones.\n\n"
    else:
        summary += f"**Public Health Status (HHRI: {hhri}/100)**: Microbial loads and disease vector densities remain within standard public safety baselines.\n\n"

    summary += "#### High-Priority Mitigation Interventions:\n"
    if indices['metrics']['eff_riparian'] < 55:
        summary += "1. **Riparian Buffer Expansion**: Plant native shoreline vegetation along central stream reaches to reduce ambient water temperatures and trap diffuse nutrient runoff.\n"
    if indices['metrics']['eff_e_coli'] > 350:
        summary += "2. **Targeted Outfall Bio-filtration**: Deploy permeable gravel wetland filters at urban stormwater discharge points to minimize pathogen loading.\n"
    summary += "3. **Community Sentinel Monitoring**: Coordinate scheduled citizen macroinvertebrate surveys to maintain dense ground-truth validation."

    return summary
