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
from src.components.simulator_view import render_simulator_view
from src.components.policy_view import render_policy_view

# Streamlit Page Configuration
st.set_page_config(
    page_title="OneAqua Insight Hub | IEEE Hackathon 2026",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Custom CSS Design System
apply_custom_styles()

# Header Banner
st.markdown("""
<div class="glass-header">
    <h1>🌊 OneAqua Insight Hub</h1>
    <p>IEEE OneAquaHealth Global Hackathon 2026 — Track 2: Data-to-Insight | Connecting Urban Freshwater Ecosystems to Human Well-Being</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.markdown("### 🏙️ Pilot City Selection")
selected_city = st.sidebar.selectbox(
    "Choose OneAquaHealth EU Pilot Site:",
    options=list(PILOT_CITIES.keys()),
    index=0
)

city_info = PILOT_CITIES[selected_city]
st.sidebar.markdown(f"**Country:** {city_info['country']}")
st.sidebar.markdown(f"**Basin:** {city_info['river']}")
st.sidebar.caption(city_info["description"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏷️ Track & Challenge Info")
st.sidebar.info("""
**Track 2: Data-to-Insight**  
Transforming citizen observations, IoT sensors, and climate telemetry into decision-grade One Health matrices.
""")

# Load City Datasets
segments = get_stream_segments(selected_city)
sensors_df = get_sensor_nodes(selected_city)
reports_df = get_citizen_reports(selected_city)
time_series_df = get_time_series_data(selected_city)

# Render Scenario Simulator Controls
temp_delta, rain_delta, riparian_delta = render_simulator_view()

# Calculate One Health Composite Indices with Simulator Offsets
indices = calculate_one_health_indices(
    segments_data=segments,
    sim_temp_delta=temp_delta,
    sim_rain_delta=rain_delta,
    sim_riparian_delta=riparian_delta
)

st.write("")

# Render One Health Composite Scorecards
render_matrix_view(indices)

st.write("")

# Main Content Navigation Tabs
tab_map, tab_analytics, tab_citizen, tab_policy = st.tabs([
    "🗺️ Geospatial Map Hub",
    "📈 Temporal Analytics",
    "👥 Citizen Science Verifier",
    "📄 One Health Policy Brief"
])

with tab_map:
    st.markdown("#### 🗺️ Multi-Layer Stream Topology & Sensor Network")
    render_map_view(city_info, segments, sensors_df, reports_df)

with tab_analytics:
    render_analytics_view(time_series_df)

with tab_citizen:
    st.markdown("<div class='section-header'>👥 Citizen Science Observation Feed</div>", unsafe_allow_html=True)
    st.markdown("Verified stream reports submitted by citizen scientists, community volunteers, and eco-patrols.")
    
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        st.dataframe(
            reports_df[["report_id", "category", "severity", "confidence", "notes", "timestamp", "verified"]],
            use_container_width=True,
            hide_index=True
        )
    with col_c2:
        st.markdown("##### 🔍 Data Quality Metrics")
        verified_pct = (reports_df["verified"].sum() / len(reports_df)) * 100
        avg_conf = reports_df["confidence"].mean() * 100
        st.metric("Verified Report Ratio", f"{int(verified_pct)}%", delta="Human-in-the-Loop")
        st.metric("Avg Confidence Score", f"{int(avg_conf)}%", delta="High Reliability")

with tab_policy:
    render_policy_view(selected_city, indices)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #8B949E; font-size: 0.85rem;">
    🌊 <b>OneAqua Insight Hub</b> | IEEE OneAquaHealth Global Hackathon 2026 | Aligned with Horizon Europe OneAquaHealth EU Project
</div>
""", unsafe_allow_html=True)
