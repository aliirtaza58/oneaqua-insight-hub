import numpy as np

def calculate_one_health_indices(segments_data, sim_temp_delta=0.0, sim_rain_delta=0.0, sim_riparian_delta=0.0):
    """
    Computes composite One Health indices (EHI, HHRI, UCSI) based on stream segment
    parameters and optional simulation offsets.
    """
    # Average base parameters across segments
    avg_do = np.mean([s["do_mg_l"] for s in segments_data])
    avg_macro = np.mean([s["macro_index"] for s in segments_data])
    avg_ph = np.mean([s["ph"] for s in segments_data])
    avg_e_coli = np.mean([s["e_coli"] for s in segments_data])
    avg_vector = np.mean([s["vector_density"] for s in segments_data])
    avg_riparian = np.mean([s["riparian_pct"] for s in segments_data])

    # Apply simulation adjustments
    eff_do = max(2.0, avg_do - (0.2 * sim_temp_delta) + (0.1 * (sim_riparian_delta / 10.0)))
    eff_macro = np.clip(avg_macro + (0.3 * (sim_riparian_delta / 10.0)) - (0.1 * sim_temp_delta), 1.0, 10.0)
    eff_riparian = np.clip(avg_riparian + sim_riparian_delta, 10.0, 100.0)
    
    eff_e_coli = max(50.0, avg_e_coli + (15.0 * sim_rain_delta) - (5.0 * (sim_riparian_delta / 10.0)))
    eff_vector = np.clip(avg_vector + (3.0 * sim_temp_delta) - (1.5 * (sim_riparian_delta / 10.0)), 5.0, 100.0)

    # 1. Ecological Health Index (EHI) [0 - 100]
    do_score = np.clip((eff_do / 10.0) * 100, 0, 100)
    macro_score = (eff_macro / 10.0) * 100
    ph_score = 100 - (abs(avg_ph - 7.2) * 40)
    ehi = (0.35 * do_score) + (0.35 * macro_score) + (0.15 * ph_score) + (0.15 * eff_riparian)
    ehi = np.clip(ehi, 0, 100)

    # 2. Human Health Risk Index (HHRI) [0 - 100] (Higher = Greater Health Risk)
    pathogen_risk = np.clip((eff_e_coli / 1000.0) * 100, 0, 100)
    vector_risk = eff_vector
    hhri = (0.50 * pathogen_risk) + (0.50 * vector_risk)
    hhri = np.clip(hhri, 0, 100)

    # 3. Urban Climate Stress Index (UCSI) [0 - 100]
    heat_stress = np.clip(40 + (5.0 * sim_temp_delta) - (0.3 * eff_riparian), 0, 100)
    runoff_stress = np.clip(35 + (4.0 * sim_rain_delta) - (0.4 * eff_riparian), 0, 100)
    ucsi = (0.50 * heat_stress) + (0.50 * runoff_stress)
    ucsi = np.clip(ucsi, 0, 100)

    # Determine status labels
    ehi_status = "Good" if ehi >= 70 else ("Moderate" if ehi >= 50 else "Critical")
    hhri_status = "Low Risk" if hhri < 35 else ("Moderate Risk" if hhri < 65 else "High Risk")
    ucsi_status = "Low Stress" if ucsi < 40 else ("Moderate Stress" if ucsi < 70 else "High Stress")

    return {
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
            "eff_riparian": round(eff_riparian, 1)
        }
    }

def generate_ai_executive_summary(city_name, indices):
    """
    Generates plain-language executive policy summaries and threshold advisories.
    """
    ehi = indices["EHI"]
    hhri = indices["HHRI"]
    ucsi = indices["UCSI"]

    summary = f"### 📑 One Health Executive Summary: {city_name}\n\n"

    if ehi < 55:
        summary += f"⚠️ **Ecological Status Alert**: The **Ecological Health Index ({ehi}/100)** in {city_name} indicates significant aquatic ecosystem distress. Reduced dissolved oxygen ({indices['metrics']['eff_do']} mg/L) and low benthic macroinvertebrate diversity suggest high urban pollution loads.\n\n"
    else:
        summary += f"✅ **Ecological Status**: The ecosystem exhibits baseline vitality with an **EHI of {ehi}/100**.\n\n"

    if hhri >= 55:
        summary += f"🚨 **Public Health Advisory**: The **Human Health Risk Index ({hhri}/100)** is elevated due to pathogen runoff (E. coli: {indices['metrics']['eff_e_coli']} CFU/100mL) and vector density ({indices['metrics']['eff_vector']}). Citizens should avoid primary water contact in central urban stream segments.\n\n"
    else:
        summary += f"🟢 **Public Health Risk**: Human risk parameters remain within safe recreational margins (**HHRI: {hhri}/100**).\n\n"

    summary += "#### 💡 Recommended Policy Actions:\n"
    if indices['metrics']['eff_riparian'] < 50:
        summary += "- **Restore Riparian Vegetation**: Expand stream buffer zones by at least 15% to buffer runoff and reduce water temperatures.\n"
    if indices['metrics']['eff_e_coli'] > 400:
        summary += "- **Stormwater Outfall Inspection**: Deploy rapid microbial screening near urban overflow points following rain events.\n"
    summary += "- **Community Stewardship**: Engage citizen science teams for weekly macroinvertebrate sampling and trash clearance."

    return summary
