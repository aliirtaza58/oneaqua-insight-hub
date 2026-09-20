import streamlit as st

def render_matrix_view(indices):
    """
    Renders One Health composite metric scorecards and status indicators.
    """
    st.markdown("<div class='section-header'>🩺 One Health Composite Matrix</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        ehi_color_class = "kpi-status-good" if indices["EHI_status"] == "Good" else ("kpi-status-warning" if indices["EHI_status"] == "Moderate" else "kpi-status-critical")
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Ecological Health (EHI)</div>
            <div class="kpi-value">{indices['EHI']} <span style="font-size: 1rem; color: #8B949E;">/ 100</span></div>
            <div class="{ehi_color_class}">● {indices['EHI_status']} Status</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        hhri_color_class = "kpi-status-good" if indices["HHRI_status"] == "Low Risk" else ("kpi-status-warning" if indices["HHRI_status"] == "Moderate Risk" else "kpi-status-critical")
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Human Health Risk (HHRI)</div>
            <div class="kpi-value">{indices['HHRI']} <span style="font-size: 1rem; color: #8B949E;">/ 100</span></div>
            <div class="{hhri_color_class}">● {indices['HHRI_status']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        ucsi_color_class = "kpi-status-good" if indices["UCSI_status"] == "Low Stress" else ("kpi-status-warning" if indices["UCSI_status"] == "Moderate Stress" else "kpi-status-critical")
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Urban Climate Stress (UCSI)</div>
            <div class="kpi-value">{indices['UCSI']} <span style="font-size: 1rem; color: #8B949E;">/ 100</span></div>
            <div class="{ucsi_color_class}">● {indices['UCSI_status']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 🔬 Detailed Parameter Breakdown")
    m = indices["metrics"]
    bcol1, bcol2, bcol3, bcol4, bcol5 = st.columns(5)
    
    with bcol1:
        st.metric("Dissolved Oxygen", f"{m['eff_do']} mg/L", delta="Optimal > 7.0")
    with bcol2:
        st.metric("Macroinvertebrate Index", f"{m['eff_macro']} / 10", delta="Bio-indicator")
    with bcol3:
        st.metric("Pathogen Load (E. coli)", f"{m['eff_e_coli']} CFU", delta="Risk > 500", delta_color="inverse")
    with bcol4:
        st.metric("Mosquito Vector Index", f"{m['eff_vector']} / 100", delta="Vector Risk", delta_color="inverse")
    with bcol5:
        st.metric("Riparian Buffer Cover", f"{m['eff_riparian']}%", delta="Target > 65%")
