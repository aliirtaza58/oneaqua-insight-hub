import streamlit as st
import pandas as pd

from src.styles import apply_custom_styles
from src.data_loader import (
    PILOT_CITIES,
    get_stream_segments,
    get_sensor_nodes,
    get_citizen_reports,
    get_time_series_data
)
from src.engine import calculate_one_health_indices
from src.components.map_view import render_map_view
from src.components.matrix_view import render_matrix_view
from src.components.analytics_view import render_analytics_view
from src.components.simulator_view import render_simulator_sidebar
from src.components.policy_view import render_policy_view

# Page Config
st.set_page_config(
    page_title="OneAqua Insight Hub | IEEE OneAquaHealth Hackathon 2026",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply UX/UI Design System
apply_custom_styles()

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.markdown("### 🏙️ EU Pilot Site")
selected_city = st.sidebar.selectbox(
    "Select Pilot City:",
    options=list(PILOT_CITIES.keys()),
    index=0
)

city_info = PILOT_CITIES[selected_city]
st.sidebar.markdown(f"**Country:** {city_info['country']}")
st.sidebar.markdown(f"**River Basin:** `{city_info['river']}`")
st.sidebar.caption(city_info["description"])

# Scenario simulator lives in sidebar — controls flow
temp_delta, rain_delta, riparian_delta = render_simulator_sidebar()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Track Alignment")
st.sidebar.info(
    "**Track 2: Data-to-Insight**\n\n"
    "Bridging citizen observations, IoT stream sensors, and climate stress "
    "indicators into actionable decision matrices for public health & resilience."
)

# ── Data ─────────────────────────────────────────────────────────────────────
segments    = get_stream_segments(selected_city)
sensors_df  = get_sensor_nodes(selected_city)
reports_df  = get_citizen_reports(selected_city)
time_series_df = get_time_series_data(selected_city)

indices = calculate_one_health_indices(
    segments_data=segments,
    sim_temp_delta=temp_delta,
    sim_rain_delta=rain_delta,
    sim_riparian_delta=riparian_delta
)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand-header">
    <div class="brand-title-group">
        <h1>🌊 OneAqua Insight Hub</h1>
        <p>IEEE OneAquaHealth Global Hackathon 2026 — Track 2: Data-to-Insight<br>
        Harmonizing Telemetry &amp; Citizen Science into One Health Intelligence</p>
    </div>
    <div class="live-beacon">
        <span class="pulse-dot"></span> Live Telemetry Active
    </div>
</div>
""", unsafe_allow_html=True)

# ── Band 1 + 2: Hero metric & scorecards ─────────────────────────────────────
render_matrix_view(indices)

st.write("")

# ── Band 3: Main Workspace Tabs ───────────────────────────────────────────────
tab_map, tab_analytics, tab_citizen, tab_policy = st.tabs([
    "🗺️ Geospatial Intelligence Map",
    "📈 Temporal Analytics & Correlation",
    "👥 Citizen Science Stream Watch",
    "📄 Executive One Health Policy Brief"
])

with tab_map:
    st.markdown(
        "<div class='ui-section-title'>🗺️ Multi-Layer Stream Topology & Telemetry Network</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "Interactive GIS map showing stream reach health, automated IoT monitoring nodes, "
        "and crowd-sourced citizen alerts."
    )
    render_map_view(city_info, segments, sensors_df, reports_df)

with tab_analytics:
    render_analytics_view(time_series_df)

with tab_citizen:
    st.markdown(
        "<div class='ui-section-title'>👥 Citizen Science Stream Watch Feed</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "Empowering local communities to validate stream water quality, report algae "
        "blooms, and track biodiversity."
    )

    col_c1, col_c2 = st.columns([3, 2])
    with col_c1:
        st.markdown("##### 📋 Verified Field Reports")
        st.dataframe(
            reports_df[[
                "report_id", "reporter", "category", "severity",
                "confidence", "timestamp", "notes", "verified"
            ]],
            use_container_width=True,
            hide_index=True
        )
    with col_c2:
        st.markdown("##### ➕ Submit New Field Observation")
        with st.form("citizen_report_form"):
            rep_category = st.selectbox(
                "Observation Category:",
                ["Algal Bloom Alert", "Macroinvertebrate Survey",
                 "Plastic Waste", "Unusual Odor / Foam", "Fish Distress"]
            )
            rep_severity = st.select_slider(
                "Severity Level:",
                options=["Low", "Medium", "High"],
                value="Medium"
            )
            rep_notes = st.text_input(
                "Sensory Description:",
                "Observed cloudy water with slight sulfur odor near footbridge."
            )
            submit_report = st.form_submit_button("🚀 Submit Citizen Report")
            if submit_report:
                st.success(
                    "✅ Observation logged! Automated AI validation confidence: 91% "
                    "(Flagged for municipal eco-patrol)."
                )

with tab_policy:
    render_policy_view(selected_city, indices)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center;
            color:#64748B; font-size:0.82rem; flex-wrap:wrap; gap:8px;">
    <div>🌊 <b>OneAqua Insight Hub</b> | IEEE OneAquaHealth Global Hackathon 2026</div>
    <div>EU Horizon Europe • Coimbra · Toulouse · Benevento · Gent · Oslo</div>
</div>
""", unsafe_allow_html=True)
