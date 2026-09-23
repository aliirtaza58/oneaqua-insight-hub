import streamlit as st

def render_matrix_view(indices):
    """
    Renders the primary dashboard metrics following data-dashboard skill standards:
    - Band 1: Hero Lead Metric (Overall Ecosystem Vitality)
    - Band 2: Three Distinct Composite Pillars with embedded meter tracks
    - Band 3: Monospace telemetry readouts with directional context
    """
    v = indices["vitality"]
    v_status = indices["vitality_status"]
    v_delta = indices["vitality_delta"]
    delta_sign = "+" if v_delta >= 0 else ""
    delta_color = "#10B981" if v_delta >= 0 else "#F43F5E"

    # Band 1: Hero Lead Metric Card
    v_chip_class = "chip-good" if v >= 70 else ("chip-warn" if v >= 48 else "chip-danger")
    
    st.markdown(f"""
    <div class="hero-lead-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
            <div>
                <div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #94A3B8; margin-bottom: 6px;">
                    Lead Indicator • Overall Freshwater Ecosystem Vitality
                </div>
                <div style="display: flex; align-items: baseline; gap: 16px;">
                    <div class="hero-score-badge">{v}</div>
                    <div style="font-size: 1.2rem; color: #64748B; font-weight: 600;">/ 100</div>
                    <span class="{v_chip_class}">● {v_status}</span>
                </div>
                <div style="color: #94A3B8; font-size: 0.88rem; margin-top: 8px;">
                    Baseline Delta: <span style="color: {delta_color}; font-weight: 700; font-family: 'JetBrains Mono', monospace;">{delta_sign}{v_delta} pts</span> vs. European Seasonal Baseline
                </div>
            </div>
            <div style="text-align: right; background: rgba(11, 14, 20, 0.6); padding: 12px 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                <div style="color: #64748B; font-size: 0.72rem; text-transform: uppercase; font-weight: 600;">Telemetry Reliability</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.3rem; font-weight: 700; color: #00F2FE;">
                    {indices['metrics']['sampling_confidence']}% Conf.
                </div>
                <div style="font-size: 0.75rem; color: #10B981; font-weight: 500;">● {indices['metrics']['sensor_nodes_online']} Nodes Online</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Band 2: Three Composite Pillars
    col1, col2, col3 = st.columns(3)

    with col1:
        ehi = indices["EHI"]
        ehi_fill_class = "meter-fill-good" if ehi >= 68 else ("meter-fill-warn" if ehi >= 48 else "meter-fill-danger")
        ehi_chip_class = "chip-good" if ehi >= 68 else ("chip-warn" if ehi >= 48 else "chip-danger")
        st.markdown(f"""
        <div class="pillar-card">
            <div class="pillar-header">
                <span>Ecological Health Index (EHI)</span>
                <span class="{ehi_chip_class}">{indices['EHI_status']}</span>
            </div>
            <div class="pillar-value">{ehi} <span style="font-size: 1rem; color: #64748B;">/ 100</span></div>
            <div class="meter-track">
                <div class="{ehi_fill_class}" style="width: {ehi}%;"></div>
            </div>
            <div style="color: #94A3B8; font-size: 0.8rem; margin-top: 6px;">
                Dissolved oxygenation, macroinvertebrate diversity & buffer integrity.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        hhri = indices["HHRI"]
        hhri_fill_class = "meter-fill-good" if hhri < 35 else ("meter-fill-warn" if hhri < 60 else "meter-fill-danger")
        hhri_chip_class = "chip-good" if hhri < 35 else ("chip-warn" if hhri < 60 else "chip-danger")
        st.markdown(f"""
        <div class="pillar-card">
            <div class="pillar-header">
                <span>Human Health Risk Index (HHRI)</span>
                <span class="{hhri_chip_class}">{indices['HHRI_status']}</span>
            </div>
            <div class="pillar-value">{hhri} <span style="font-size: 1rem; color: #64748B;">/ 100</span></div>
            <div class="meter-track">
                <div class="{hhri_fill_class}" style="width: {hhri}%;"></div>
            </div>
            <div style="color: #94A3B8; font-size: 0.8rem; margin-top: 6px;">
                Microbial pathogen concentration & mosquito vector density.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        ucsi = indices["UCSI"]
        ucsi_fill_class = "meter-fill-good" if ucsi < 38 else ("meter-fill-warn" if ucsi < 65 else "meter-fill-danger")
        ucsi_chip_class = "chip-good" if ucsi < 38 else ("chip-warn" if ucsi < 65 else "chip-danger")
        st.markdown(f"""
        <div class="pillar-card">
            <div class="pillar-header">
                <span>Urban Climate Stress Index (UCSI)</span>
                <span class="{ucsi_chip_class}">{indices['UCSI_status']}</span>
            </div>
            <div class="pillar-value">{ucsi} <span style="font-size: 1rem; color: #64748B;">/ 100</span></div>
            <div class="meter-track">
                <div class="{ucsi_fill_class}" style="width: {ucsi}%;"></div>
            </div>
            <div style="color: #94A3B8; font-size: 0.8rem; margin-top: 6px;">
                Thermal anomaly delta & urban stormwater retention vulnerability.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Band 3: Monospace telemetry metrics
    # Band 3: Monospace telemetry metrics formatted as clean stat badges
    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    m = indices["metrics"]
    
    bcol1, bcol2, bcol3, bcol4, bcol5 = st.columns(5)
    
    with bcol1:
        st.metric(
            label="Dissolved Oxygen",
            value=f"{m['eff_do']} mg/L",
            delta="Optimal > 7.0",
            delta_color="normal" if m['eff_do'] >= 7.0 else "inverse"
        )
    with bcol2:
        st.metric(
            label="Benthic Bio-Index",
            value=f"{m['eff_macro']} / 10",
            delta="Target > 6.5",
            delta_color="normal" if m['eff_macro'] >= 6.5 else "inverse"
        )
    with bcol3:
        st.metric(
            label="Pathogen (E. coli)",
            value=f"{m['eff_e_coli']} CFU",
            delta="Safe < 400",
            delta_color="normal" if m['eff_e_coli'] < 400 else "inverse"
        )
    with bcol4:
        st.metric(
            label="Vector Density",
            value=f"{m['eff_vector']} / 100",
            delta="Safe < 50",
            delta_color="normal" if m['eff_vector'] < 50 else "inverse"
        )
    with bcol5:
        st.metric(
            label="Riparian Buffer",
            value=f"{m['eff_riparian']}%",
            delta="Goal > 60%",
            delta_color="normal" if m['eff_riparian'] >= 60 else "inverse"
        )
