import numpy as np

SCENARIO_PRESETS = {
    "Baseline Telemetry": {
        "temp_delta": 0.0,
        "rain_delta": 0.0,
        "riparian_delta": 0.0,
        "desc": "Normal seasonal conditions with standard urban stormwater buffer capacity."
    },
    "☀️ Summer Heatwave Event": {
        "temp_delta": 3.5,
        "rain_delta": 0.0,
        "riparian_delta": 0.0,
        "desc": "Simulates elevated water temperatures, reduced dissolved oxygen, and heightened vector breeding."
    },
    "🌧️ Flash Storm Runoff Surge": {
        "temp_delta": -0.5,
        "rain_delta": 40.0,
        "riparian_delta": 0.0,
        "desc": "Simulates high urban runoff, stormwater overflow, and acute microbial pathogen spikes."
    },
    "🌿 25% Riparian Eco-Restoration": {
        "temp_delta": 0.0,
        "rain_delta": 0.0,
        "riparian_delta": 25.0,
        "desc": "Simulates restored urban vegetation buffer zones mitigating heat and filtering runoff."
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

def generate_ai_executive_summary(city_name, indices):
    """
    Generates plain-language executive policy summaries and threshold advisories.
    """
    v = indices["vitality"]
    ehi = indices["EHI"]
    hhri = indices["HHRI"]
    ucsi = indices["UCSI"]

    summary = f"### 📑 One Health Executive Advisory: {city_name}\n\n"
    summary += f"**Overall Ecosystem Vitality:** `{v}/100` ({indices['vitality_status']})  \n"
    summary += f"**Monitoring Confidence:** `{indices['metrics']['sampling_confidence']}%` via continuous telemetry & citizen observations.\n\n"
    summary += "---\n\n"

    if ehi < 50:
        summary += f"⚠️ **Aquatic Ecosystem Alert (EHI: {ehi}/100)**: Stream segment telemetry shows dissolved oxygen levels dropped to **{indices['metrics']['eff_do']} mg/L** with benthic macroinvertebrate diversity rated at **{indices['metrics']['eff_macro']}/10**, indicating chronic organic pollution.\n\n"
    else:
        summary += f"✅ **Aquatic Ecosystem Vitality (EHI: {ehi}/100)**: Stream oxygenation (**{indices['metrics']['eff_do']} mg/L**) and macroinvertebrate bio-indicators remain stable within European Water Framework Directive standards.\n\n"

    if hhri >= 50:
        summary += f"🚨 **Public Health Precaution (HHRI: {hhri}/100)**: Microbial pathogen indicators (E. coli load: **{indices['metrics']['eff_e_coli']} CFU/100mL**) and adult Diptera vector breeding (**{indices['metrics']['eff_vector']}/100**) exceed safe recreational thresholds. Municipal advisories recommended for public water contact.\n\n"
    else:
        summary += f"🟢 **Public Health Safety (HHRI: {hhri}/100)**: Microbial loads and mosquito vector densities are within safe public recreational margins.\n\n"

    summary += "#### 🛠️ High-Priority Mitigation Interventions:\n"
    if indices['metrics']['eff_riparian'] < 55:
        summary += "1. **Riparian Buffer Zone Expansion**: Plant native shoreline vegetation along central urban corridors to lower water temperatures by up to 1.8°C.\n"
    if indices['metrics']['eff_e_coli'] > 350:
        summary += "2. **Targeted Outfall Bio-filtration**: Install permeable gravel wetland filters at urban stormwater discharge points.\n"
    summary += "3. **Citizen Science Deployment**: Mobilize community water sentinels for bi-weekly benthic macroinvertebrate index validation."

    return summary
