import streamlit as st
from src.engine import SCENARIO_PRESETS

def render_simulator_sidebar():
    """
    Renders the scenario sandbox controls inside the sidebar as a compact control panel.
    Returns (temp_delta, rain_delta, riparian_delta).
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚡ Scenario Simulator")
    st.sidebar.caption("Model climate extremes or interventions against live stream metrics.")

    selected_preset = st.sidebar.selectbox(
        "Quick Scenario Preset:",
        options=list(SCENARIO_PRESETS.keys()),
        index=0,
        key="scenario_preset"
    )

    preset_data = SCENARIO_PRESETS[selected_preset]
    st.sidebar.info(f"{preset_data['desc']}", icon="💡")

    temp_delta = st.sidebar.slider(
        "☀️ Heatwave Spike (°C)",
        min_value=-2.0, max_value=6.0,
        value=float(preset_data["temp_delta"]),
        step=0.5,
        key="temp_delta"
    )
    rain_delta = st.sidebar.slider(
        "🌧️ Storm Runoff (mm/hr)",
        min_value=0.0, max_value=60.0,
        value=float(preset_data["rain_delta"]),
        step=5.0,
        key="rain_delta"
    )
    riparian_delta = st.sidebar.slider(
        "🌿 Buffer Restoration (%)",
        min_value=0.0, max_value=40.0,
        value=float(preset_data["riparian_delta"]),
        step=5.0,
        key="riparian_delta"
    )

    return temp_delta, rain_delta, riparian_delta
